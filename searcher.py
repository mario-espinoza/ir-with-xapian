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
def search(dbpath, title, offset=0, pagesize=10):
    # offset - defines starting point within result set
    # pagesize - defines number of records to retrieve
    
    print 'TITLE: {}'.format(title)
    regex = re.findall(r'\w+', title.lower())
    queryAND = ' AND '.join(regex)
    queryOR = ' OR '.join(regex)
    print 'REGEX: {}'.format(regex)
    queries = [queryAND,queryOR]

    for querystring in queries:
        print 'QUERY: {}'.format(querystring)
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
        MRR=0
        for match in enquire.get_mset(offset, pagesize):
            toDecode = match.document.get_data();
            fields = json.loads(toDecode.decode('utf-8', 'ignore'))
            matchTitle = fields.get('TITLE', u'')
            matchRank=match.rank + 1
            # if matchRank>1 and title == matchTitle :
                # print '\n *** \n'
                # print title
                # print matchTitle
                # print 'matchRank: {}\n'.format(matchRank)
                # # print 'MRR: {}\n'.format(1/matchRank)
                # print '\n *** \n'

            print(u"%(rank)i: #%(docid)3.3i \n %(id)s \n TITLE: %(title)s \n %(body)s \n %(class)s" % {
                    'rank': matchRank,
                    'docid': match.docid,
                    'id': fields.get('ID', u''),
                    'title': matchTitle,
                    'body': fields.get('BODY', u''),
                    'class': fields.get('CLASS', u'')
                    })
            matches.append(match.docid)
            MRR=1/matchRank
        print 'MRR: {}\n'.format(MRR)
        # Finally, make sure we log the query and displayed results
        log_matches(querystring, offset, pagesize, matches)
    print '\n'
### End of example code.

logging.basicConfig(level=logging.INFO)
with open('titles.txt','rU') as titleFile:
    titles = titleFile.readlines()
    for title in titles:
        print '{}'.format(title)
        search('DB', title.strip())
        # search('DB', querystring = " ".join(title))