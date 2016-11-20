#!/usr/bin/env python

import json, sys, xapian, csv
from collections import defaultdict

columns = defaultdict(list)

def parse_csv_file(datapath):
    with open(datapath) as fd:
        reader = csv.DictReader(fd)
        for row in reader:
            yield row

def index(datapath, dbpath):
    db = xapian.WritableDatabase(dbpath, xapian.DB_CREATE_OR_OPEN)
    termgenerator = xapian.TermGenerator()
    termgenerator.set_stemmer(xapian.Stem("en"))

    for fields in parse_csv_file(datapath):
        title = fields.get('TITLE', u'')
        body = fields.get('BODY', u'')
        textClass = fields.get('CLASS', u'')
        identifier = fields.get('ID', u'')
        print '{}'.format(title)
        print '{}'.format(body)

        doc = xapian.Document()
        termgenerator.set_document(doc)

        termgenerator.index_text(textClass, 1, 'C')
        termgenerator.index_text(body, 1, 'B')
        termgenerator.index_text(identifier, 1, 'I')

        termgenerator.index_text(textClass)
        termgenerator.increase_termpos()
        termgenerator.index_text(body)
        termgenerator.increase_termpos()
        termgenerator.index_text(identifier)

        doc.set_data(json.dumps(fields, ensure_ascii=False, encoding="utf-8"))

        idterm = u"Q" + identifier
        doc.add_boolean_term(idterm)
        db.replace_document(idterm, doc)

if len(sys.argv) != 3:
    print("Usage: %s DATAPATH DBPATH" % sys.argv[0])
    sys.exit(1)

index(datapath = sys.argv[1], dbpath = sys.argv[2])