# RDFLib-SQLite3

An [SQLite](https://www.sqlite.org/)-backed [RDFLib](https://rdflib.dev/) store.

RDFLib-SQLite3 allws RDFLib RDF graphs to be persisted in an SQLite database. Furthermore it allows full-text and Geospatial indexing: Using the SQLite [FTS5](https://www.sqlite.org/fts5.html) and [R*Tree](https://sqlite.org/rtree.html).

## Usage

```
from rdflib import Graph
import rdflib_sqlite3


# Create a Graph backed by an SQLite database
g = Graph("SQLite3")
# Open and create the database. See https://www.sqlite.org/uri.html for the URI format.
g.open("file:my-rdf.sqlite", create=True)

# do stuff with the graph...
```

## Goals

RDFLib-SQLite3 is primary goal is stability. RDFLib-SQLite3 should be usable with minimal maintainance in many year and the data format should be desigend for long-term readability.

SQLite is a suitable backend as it uses a [stable file format](https://sqlite.org/fileformat2.html), offers [long term support](https://sqlite.org/lts.html) is [well tested](https://sqlite.org/testing.html) and [widely used](https://sqlite.org/mostdeployed.html). RDFLib-SQLite3 uses the SQLite bindings that are [provided as part of the Python 3 standard library](https://docs.python.org/3/library/sqlite3.html), which will most likely be included in future versions of Python 3.

## Database Schema

The RDF graphs is peristed in the SQLite database using two tables:

- `rdf_term`:

	```
	CREATE TABLE IF NOT EXISTS rdf_term (
		id INTEGER PRIMARY KEY,
		term BLOB UNIQUE
	);
	```

	This is a mapping from RDF terms encoded using [RDF/CBOR](https://openengiadina.codeberg.page/rdf-cbor/) to integer identifiers.
	
- `rdf_triple`:

	```
	CREATE_RDF_TRIPLE_TABLE = """
	CREATE TABLE IF NOT EXISTS rdf_triple (
		subject INTEGER NOT_NULL REFERENCES rdf_term ON DELETE RESTRICT,
		predicate INTEGER NOT_NULL REFERENCES rdf_term ON DELETE RESTRICT,
		object INTEGER NOT_NULL REFERENCES rdf_term ON DELETE RESTRICT
	);
	```
	
	Holds triples with triple elements being identifiers as stored in the `rdf_term` table. Additional indices are defined on the `rdf_triple` table for efficient querying (and ensuring uniquness of triples).
	
## Limitations

- No support for Quads
- No support for `REGEXTerm`, `Date?`, `DateRagen?` queries

## TODOs

- [ ] Triple removal
- [ ] Tests
- [ ] Database destruction (`destroy` method)
- [ ] Database garbage collection (`gc` method)
- [ ] Full-text search
- [ ] Geospatial queries
- [ ] Make SPARQL queries more efficient. RDFLib provides [a SPARQL implementation](https://rdflib.readthedocs.io/en/stable/intro_to_sparql.html) that works with RDFLib-SQLite3. Unfortunately, performance is very limited as the SPARQL implementation does everyhing in Python. It would make much more efficient to offload query optimization, joins and even recursive queries to SQLite. This amounts to writing an SPARQL implementation that knows how to take advantage of SQLite.

## Related Software

- [rdflib-sqlite](https://github.com/RDFLib/rdflib-sqlite): Abandoned and no longer maintained.
- [rdflib-sqlalchemy](https://github.com/RDFLib/rdflib-sqlalchemy): No longer maintained and uses a legacy version of [SQLAlchemy](https://www.sqlalchemy.org/)
  - There also seems to be [an issue where long URIs cause large databases](https://github.com/RDFLib/rdflib-sqlalchemy/issues/66). 

## Publishing to PyPi

Make sure version is set propertly in [`pyproject.toml`](./pyproject.toml) and [`rdflib_sqlite3/__init__.py`](./rdflib_sqlite3/__init__.py).

```
pip install build twine

# Build the package
python -m build

# Upload using twine
twine upload dist/*
```
  
## Acknowledgments

This software was initially developed as part of the SNSF-Ambizione funded research project ["Computing the Social. Psychographics and Social Physics in the Digital Age"](https://data.snf.ch/grants/grant/201912).

## License

[AGPL-3.0-or-later](COPYING)
