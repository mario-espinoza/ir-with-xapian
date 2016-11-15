#!/usr/bin/env python

import json, logging, sys, xapian, re

def log_matches(querystring, offset, pagesize, matches):
    logger = logging.getLogger("xapian.search")
    logger.info(
        "'%s'[%i:%i] = %s",
        querystring,
        offset,
        offset + pagesize,
        ' '.join(str(docid) for docid in matches),
        )

### Start of Search.
def search(dbpath, title,  offset=0, pagesize=10):
    print '{}'.format(title)
    regex = re.findall(r'\w+', title.lower())
    print 'REGEX: {}'.format(regex)
    queryAND = ' AND '.join(regex)
    queryOR = ' OR '.join(regex)
    for querystring in [queryAND.encode('utf-8'),queryOR.encode('utf-8')]:
        print 'QUERY: {}'.format(querystring)
        # offset - defines starting point within result set
        # pagesize - defines number of records to retrieve

        # Open the database we're going to search.
        db = xapian.Database(dbpath)

        # Set up a QueryParser with a stemmer and suitable prefixes
        queryparser = xapian.QueryParser()
        queryparser.set_stemmer(xapian.Stem("en"))
        queryparser.set_stemming_strategy(queryparser.STEM_SOME)
        # Start of prefix configuration.
        queryparser.add_prefix("TITLE", "T")
        queryparser.add_prefix("BODY", "B")
        queryparser.add_prefix("ID", "I")
        queryparser.add_prefix("CLASS", "C")
        # End of prefix configuration.

        # And parse the query
        query = queryparser.parse_query(querystring)

        # Use an Enquire object on the database to run the query
        enquire = xapian.Enquire(db)
        enquire.set_query(query)

        # And print out something about each match
        matches = []
        for match in enquire.get_mset(offset, pagesize):
            fields = json.loads(match.document.get_data())
            # if title == fields.get('TITLE', u''):
            #     print 'This is \n'
            print(u"%(rank)i: #%(docid)3.3i \n %(id)s \n %(title)s \n %(body)s \n %(class)s \n" % {
                'rank': match.rank + 1,
                'docid': match.docid,
                'id': fields.get('ID', u''),
                'title': fields.get('TITLE', u''),
                'body': fields.get('BODY', u''),
                'class': fields.get('CLASS', u'')
                })
            matches.append(match.docid)

        # Finally, make sure we log the query and displayed results
        log_matches(querystring, offset, pagesize, matches)
### End of example code.

logging.basicConfig(level=logging.INFO)
with open('titles.txt','rU') as titleFile:
    titles = titleFile.readlines()
    for title in titles:
        search('DB', title.encode('utf-8'))
        # search('DB', querystring = " ".join(title))