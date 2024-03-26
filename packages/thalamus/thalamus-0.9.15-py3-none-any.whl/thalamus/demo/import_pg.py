#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2017-2024 GNU Solidario <health@gnusolidario.org>
# SPDX-FileCopyrightText: 2017-2024 Luis Falcón <falcon@gnuhealth.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import psycopg2
import logging


# Modify to meet your needs
PG_URI = "postgresql:///federation"

try:
    conn = psycopg2.connect(PG_URI)
except Exception as err:
    logging.error(f"Exception {err=}, {type(err)=}")

people_file = open('people.json', 'r')
people_data = json.load(people_file)

pols_file = open('pols.json', 'r')
pols_data = json.load(pols_file)

personal_docs_file = open('personal_docs.json', 'r')
personal_docs_data = json.load(personal_docs_file)


doc_file = open('newborn.jpg', 'rb')
document = doc_file.read()


doc_id = "8789981f-4e31-48d5-8eb8-1774dac8b8f6"
cur = conn.cursor()


for person in people_data:
    id = person['id']
    print("Inserting", id)
    cur.execute(
        "INSERT INTO people (ID, DATA) VALUES (%(id)s, \
        %(data)s) ON CONFLICT DO NOTHING",
        {'id': id, 'data': json.dumps(person)})
    conn.commit()


for pol in pols_data:
    id = pol['id']
    book = pol['book']
    print("Inserting", id, book)
    cur.execute(
        "INSERT INTO pols (ID, BOOK, DATA) VALUES (%(id)s, \
        %(book)s, %(data)s) ON CONFLICT DO NOTHING",
        {'id': id, 'book': book, 'data': json.dumps(pol)})
    conn.commit()


# Insert personal document for Ana Betz
for doc in personal_docs_data:
    print("Importing PERSONAL DOCS...", doc)
    id = doc['id']
    fedacct = doc['fedacct']
    pol = doc['pol']
    cur.execute(
                "INSERT INTO personal_docs (ID, FEDACCT, POL, DATA) \
                VALUES (%(id)s, %(fedacct)s, %(pol)s, %(data)s)  \
                ON CONFLICT DO NOTHING",
                {'id': id, 'fedacct': fedacct, 'pol': pol,
                 'data': json.dumps(doc)})
    conn.commit()


# Update specific personal doc from demo newborn picture
cur.execute(
    "UPDATE personal_docs SET document = %s where id = %s",
    (document, doc_id))

conn.commit()
