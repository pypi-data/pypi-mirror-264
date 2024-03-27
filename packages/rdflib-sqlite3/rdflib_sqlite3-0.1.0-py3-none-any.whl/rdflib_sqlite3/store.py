# SPDX-FileCopyrightText: 2024 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2024 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from rdflib.store import Store
from rdflib.graph import _TripleType, _ContextType, _TriplePatternType, Graph
import rdflib.plugins.stores.memory

import sqlite3
import rdflib_rdfcbor.term

from operator import itemgetter


CREATE_RDF_TERM_TABLE = """
CREATE TABLE IF NOT EXISTS rdf_term (
   id INTEGER PRIMARY KEY,
   term BLOB UNIQUE
);
"""

CREATE_RDF_TRIPLE_TABLE = """
CREATE TABLE IF NOT EXISTS rdf_triple (
   subject INTEGER NOT_NULL REFERENCES rdf_term ON DELETE RESTRICT,
   predicate INTEGER NOT_NULL REFERENCES rdf_term ON DELETE RESTRICT,
   object INTEGER NOT_NULL REFERENCES rdf_term ON DELETE RESTRICT
);
"""

CREATE_RDF_TRIPLE_INDEX_SPO = """
CREATE UNIQUE INDEX IF NOT EXISTS rdf_triple_spo on rdf_triple (
   subject,
   predicate,
   object );
"""

CREATE_RDF_TRIPLE_INDEX_S = """
CREATE INDEX IF NOT EXISTS rdf_triple_s on rdf_triple (
   subject
);
"""

CREATE_RDF_TRIPLE_INDEX_P = """
CREATE INDEX IF NOT EXISTS rdf_triple_p on rdf_triple (
   predicate
);
"""

CREATE_RDF_TRIPLE_INDEX_O = """
CREATE INDEX IF NOT EXISTS rdf_triple_o on rdf_triple (
   object
);
"""

CREATE_RDF_TRIPLE_INDEX_SP = """
CREATE INDEX IF NOT EXISTS rdf_triple_sp on rdf_triple (
   subject,
   predicate
);
"""

CREATE_RDF_TRIPLE_INDEX_SO = """
CREATE INDEX IF NOT EXISTS rdf_triple_so on rdf_triple (
   subject,
   object
);
"""

CREATE_RDF_TRIPLE_INDEX_PO = """
CREATE INDEX IF NOT EXISTS rdf_triple_po on rdf_triple (
   predicate,
   object
);
"""


class SQLite3(Store):
    """SQLite-backed RDFLib store

    Triples are stored in a SQLite store in following tables:

    - `rdf_terms`: A mapping from RDF terms to integer identifiers.
    - `rdf_type`: Asserted rdf:type statements
    - `rdf_triples`: Asserted non rdf:type statements
    """

    def __init__(self):
        super(SQLite3, self).__init__()

        # Use an in-memory graph for namespaces. This is quite a hack
        # but allows us to use the rdflib implementation with a stable
        # API.
        self.__namespace_store = rdflib.plugins.stores.memory.Memory()

    def __len__(self, context):
        """
        Returns number of statements in store.
        """
        if self.db:
            c = self.db.cursor()
            c.execute("SELECT COUNT(*) FROM rdf_triple;")
            (count,) = c.fetchone()
            return count
        else:
            return 0

    # Database Connection & Management

    def _enable_pragmas(self):
        c = self.db.cursor()
        c.execute("PRAGMA foreign_keys = ON;")

    def open(self, configuration: str, create: bool = True):
        """
        Open the SQLite database. The configuration string is a
        """
        self.db = sqlite3.connect(configuration, uri=True)

        self._enable_pragmas()

        if create:
            c = self.db.cursor()

            c.execute(CREATE_RDF_TERM_TABLE)
            c.execute(CREATE_RDF_TRIPLE_TABLE)

            c.execute(CREATE_RDF_TRIPLE_INDEX_SPO)
            c.execute(CREATE_RDF_TRIPLE_INDEX_S)
            c.execute(CREATE_RDF_TRIPLE_INDEX_P)
            c.execute(CREATE_RDF_TRIPLE_INDEX_O)
            c.execute(CREATE_RDF_TRIPLE_INDEX_SP)
            c.execute(CREATE_RDF_TRIPLE_INDEX_SO)
            c.execute(CREATE_RDF_TRIPLE_INDEX_PO)

    def close(self, commit_pending_transaction: bool = False) -> None:
        """
        This closes the database connection. The commit_pending_transaction
        parameter specifies whether to commit all pending transactions before
        closing (if the store is transactional).
        """
        if commit_pending_transaction:
            self.db.commit()
        self.db.close()

    def destroy(self, configuration: str) -> None:
        """
        This destroys the instance of the store identified by the
        configuration string.
        """
        raise NotImplementedError

    def gc(self) -> None:
        """
        Allows the store to perform any needed garbage collection
        """
        # TODO: clear unused terms
        pass

    # RDF APIs

    ## Terms

    def locate_term(self, term):
        """Locate or insert a term in the terms table and return its
        id. If term is not present -1 is returned."""

        encoded = rdflib_rdfcbor.term.dumps(term)
        c = self.db.cursor()

        # Attempt to fetch id if term already exists
        res = c.execute("SELECT id FROM rdf_term where term = ?", (encoded,))
        row = res.fetchone()
        if row:
            return row[0]
        else:
            return -1

    def insert_term(self, term):
        """Insert term if not already present and return identifier."""
        existing_term_id = self.locate_term(term)

        if 0 <= existing_term_id:
            return existing_term_id
        else:
            # Insert term
            encoded = rdflib_rdfcbor.term.dumps(term)
            c = self.db.cursor()
            res = c.execute("INSERT INTO rdf_term(term) VALUES(?)", (encoded,))
            return c.lastrowid

    def locate_triple_terms(self, triple):
        """Locate terms appearing in triple and return ids."""
        s, p, o = triple

        s_id = self.locate_term(s)
        p_id = self.locate_term(p)
        o_id = self.locate_term(o)

        return (s_id, p_id, o_id)

    def insert_triple_terms(self, triple):
        s, p, o = triple

        s_id = self.insert_term(s)
        p_id = self.insert_term(p)
        o_id = self.insert_term(o)

        return (s_id, p_id, o_id)

    def extract_term(self, id):
        """Return term for given id"""
        c = self.db.cursor()

        res = c.execute("SELECT term FROM rdf_term where id = ?", (id,))
        row = res.fetchone()
        if row:
            return rdflib_rdfcbor.term.loads(row[0])
        else:
            return None

    def extract_triple_terms(self, triple_id):
        """Return triple of RDF terms for the given triple of term identifiers."""
        (s_id, p_id, o_id) = triple_id
        triple = (
            self.extract_term(s_id),
            self.extract_term(p_id),
            self.extract_term(o_id),
        )
        return triple

    def add(
        self,
        triple: _TripleType,
        context: _ContextType,
        quoted: bool = False,
    ) -> None:
        """
        Adds the given statement to the store.
        """

        triple_term_ids = self.insert_triple_terms(triple)

        c = self.db.cursor()

        # Attempt to fetch triple
        res = c.execute(
            "SELECT rowid FROM rdf_triple WHERE ( subject = ? AND predicate = ? AND object = ?);",
            triple_term_ids,
        )

        row = res.fetchone()
        if row:
            return
        else:
            c.execute(
                "INSERT INTO rdf_triple(subject, predicate, object) VALUES(?,?,?);",
                triple_term_ids,
            )
            return

    def remove(
        self,
        triple: _TriplePatternType,
        context=None,
    ) -> None:
        """Remove the set of triples matching the pattern from the store"""
        # the super method dispatches an event
        super(SQLite3, self).remove(self, triple, context)

    def triples(self, triple_pattern: _TriplePatternType, context=None):
        """
        A generator over all the triples matching the pattern. Pattern can
        include any objects for used for comparing against nodes in the store,
        for example, REGEXTerm, URIRef, Literal, BNode, Variable, Graph,
        QuotedGraph, Date? DateRange?

        :param context: A conjunctive query can be indicated by either
                        providing a value of None, or a specific context can be
                        queries by passing a Graph instance (if store is context aware).
        """
        (s, p, o) = triple_pattern

        where_clauses = []

        if s is not None:
            s_id = self.locate_term(s)
            where_clauses.append(("subject = ?", s_id))

        if p is not None:
            p_id = self.locate_term(p)
            where_clauses.append(("predicate = ?", p_id))

        if o is not None:
            o_id = self.locate_term(o)
            where_clauses.append(("object = ?", o_id))

        if where_clauses:
            stmt = (
                "SELECT subject, predicate, object FROM rdf_triple WHERE ("
                + " AND ".join(map(itemgetter(0), where_clauses))
                + ");"
            )
        else:
            stmt = "SELECT subject, predicate, object FROM rdf_triple;"

        values = list(map(itemgetter(1), where_clauses))

        c = self.db.cursor()

        for row in c.execute(stmt, values):
            yield (self.extract_triple_terms(row), None)

    # Namespace methods
    #
    # We re-use the methods provided in rdflib.memory.Memory

    def bind(self, prefix, namespace, override=True):
        return self.__namespace_store.bind(prefix, namespace, override=override)

    def namespace(self, prefix: str):
        return self.__namespace_store.namespace(prefix)

    def prefix(self, namespace):
        return self.__namespace_store.prefix(namespace)

    def namespaces(self):
        yield from self.__namespace_store.namespaces()

    # Optional Transactional methods

    transaction_aware = True

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()
