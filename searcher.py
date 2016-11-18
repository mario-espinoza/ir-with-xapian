#!/usr/bin/env python
from decimal import *
from fractions import Fraction
import json, logging, sys, xapian, re

def log_matches(querystring, offset, pagesize, matches):
    logger = logging.getLogger("xapian.search")
    logger.info(
        "[%i:%i] = %s",
        offset,
        offset + pagesize,
        ' '.join(str(docid) for docid in matches),
        )

andFile = open('andRankingsFinal.csv','w+')
orFile = open('orRankingsFinal.csv','w+')
analysis = open('analysisFinal.txt','w+')
### Start of Search.
andRankings = []
orRankings = []
lengths = []
classes=[]
dbpath='DB'
offset=0
pagesize=10

def search(title, clase,titleId):
    # offset - defines starting point within result set
    # pagesize - defines number of records to retrieve
    
    print 'LINE: {}'.format(titleId)
    print 'TITLE: {}'.format(title)
    regex = re.findall(r'\w+', title.lower())
    queryAND = ' AND '.join(regex)
    queryOR = ' OR '.join(regex)
    print 'REGEX: {}'.format(regex)
    length = len(regex)
    lengths.append(length)
    queries = [queryAND,queryOR]

    andQuery = True

    for querystring in queries:
        print 'QUERY: {}'.format(querystring)
        db = xapian.Database(dbpath)

        if andQuery:
            of = andFile;
        else: 
            of = orFile

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
            toDecode = match.document.get_data();
            fields = json.loads(toDecode.decode('utf-8', 'ignore'))
            matchTitle = fields.get('TITLE', u'')
            matchRank=match.rank + 1
            docid = match.docid
            docClass=fields.get('CLASS', u'')
            
            # if matchRank>1 and title == matchTitle :
                # print '\n *** \n'
                # print title
                # print matchTitle
                # print 'matchRank: {}\n'.format(matchRank)
                # # print 'MRR: {}\n'.format(1/matchRank)
                # print '\n *** \n'

            # print(u"%(rank)i: #%(docid)3.3i \n %(id)s \n TITLE: %(title)s \n %(body)s \n %(class)s" % {
                    # 'rank': matchRank,
                    # 'docid': docid,
                    # 'id': fields.get('ID', u''),
                    # 'title': matchTitle,
                    # 'body': fields.get('BODY', u''),
                    # 'class': fields.get('CLASS', u'')
                    # })
            matches.append(match.docid)
            # MRR=1/matchRank
        # print 'MRR: {}\n'.format(MRR)
        # Finally, make sure we log the query and displayed results
        print(matches)
        if titleId in matches:
            ranking = matches.index(titleId)+1
            print 'INDEX :{}'.format(ranking)
            of.write('{},{},{}\n'.format(ranking,length,clase))
            if andQuery:
                andRankings.append(ranking)
                
            else: 
                orRankings.append(ranking)
                
        else:
            of.write('0, {},{}\n'.format(length,clase))
            print 'not found'
            if andQuery:
                andRankings.append(0)
                
            else: 
                orRankings.append(0)
                

        andQuery = not andQuery
        log_matches(querystring, offset, pagesize, matches)
    
### End of example code.

logging.basicConfig(level=logging.INFO)
with open('titles.txt','rU') as titleFile:
    lines = titleFile.readlines()
    for (i,line) in enumerate(lines):
        print(line)
        data=line.split('|');
        title=data[0].strip();
        clase=data[1].replace('\n','').strip();
        classes.append(clase);

        search(title,clase,i+1)
        # search('DB', querystring = " ".join(title))
    andFile.close
    orFile.close
    print('\nLENGHTS')
    print(lengths)
    print('\nCLASSES')
    print(classes)
    print('\nAND')
    print(andRankings)
    andRR=[]
    
    for i in andRankings:
        if i>0:
            andRR.append(Fraction(1,i))
        else:
            andRR.append(0)
    print(andRR)
    andMRR=(reduce(lambda x, y: x + y, andRR) / len(andRR))+0.0000
    # print '{:0.6f}'.format(andMRR)
    print(andMRR+0.0000)
    analysis.write('AND: {}\n'.format(andMRR))
    print('\nOR')
    print(orRankings)
    orRR=[]
    for i in orRankings:
        if i>0:
            orRR.append(Fraction(1,i))
        else:
            orRR.append(0)
    print(orRR)
    orMRR=(reduce(lambda x, y: x + y, orRR) / len(orRR))+0.0000
    # print '{:0.6f}'.format(orMRR)
    print(orMRR)
    analysis.write('OR: {}\n'.format(orMRR))
    print('\n')
