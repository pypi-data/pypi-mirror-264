# SPDX-FileCopyrightText: 2024 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2024 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import rdflib

__version__ = "0.1.0"

rdflib.plugin.register(
    "SQLite3",
    rdflib.store.Store,
    "rdflib_sqlite3.store",
    "SQLite3",
)
