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

# andRankings = []
# orRankings = []
# andPrecisionAt1=[]
# andPrecisionAt2=[]
# andPrecisionAt5=[]
# andPrecisionAt10=[]
# andRecalls=[]
# orPrecisionsAt1=[]
# orPrecisionsAt2=[]
# orPrecisionsAt5=[]
# andPrecisionAt10=[]
# orRecalls=[]

DATA = {
    'OR':{
        'rankings':[],
        'recalls':[],
        'precisionsAt1':[],
        'precisionsAt2':[],
        'precisionsAt5':[],
        'precisionsAt10':[]
    },
    'AND': {
        'rankings':[],
        'recalls':[],
        'precisionsAt1':[],
        'precisionsAt2':[],
        'precisionsAt5':[],
        'precisionsAt10':[]
    }
}

lengths = []
classes=[]

dbpath='DBMine'
offset=0
pagesize=10
relevantTotal=1
# def addData(obj)

def search(title, clase,categoria,titleId):
    # offset - defines starting point within result set
    # pagesize - defines number of records to retrieve
    
    # print 'LINE: {}'.format(titleId)
    # print 'TITLE: {}'.format(title)
    regex = re.findall(r'\w+', title.lower())
    queryAND = ' AND '.join(regex)
    queryOR = ' OR '.join(regex)
    # print 'REGEX: {}'.format(regex)
    length = len(regex)
    lengths.append(length)
    queries = [queryAND,queryOR]
    andQuery = True

    for querystring in queries:
        # print 'QUERY: {}'.format(querystring)
        db = xapian.Database(dbpath)

        if andQuery:
            of = andFile;
            data = DATA['AND']
        else: 
            data = DATA['OR']

        queryparser = xapian.QueryParser()
        queryparser.set_stemmer(xapian.Stem("en"))
        queryparser.set_stemming_strategy(queryparser.STEM_SOME)
        queryparser.add_prefix("TITLE", "T")
        queryparser.add_prefix("BODY", "B")
        queryparser.add_prefix("ID", "I")
        queryparser.add_prefix("CLASS", "C")
        query = queryparser.parse_query(querystring)
        enquire = xapian.Enquire(db)
        enquire.set_query(query)
        matches = []

        totalMatches = len(enquire.get_mset(offset, 650))
        # print 'TOTAL: {}'.format(totalMatches) 
        enquires = enquire.get_mset(offset, pagesize)
        # print 'ESTIMATED : {}'.format(enquires.get_matches_estimated())
        
        for match in enquires:
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
        # print(matches)

        if titleId in matches:
            ranking = matches.index(titleId)+1
            # print 'INDEX :{}'.format(ranking)
            of.write('{},{},{},{},1\n'.format(ranking,length,clase,categoria))
            # if andQuery:
            #     andRankings.append(ranking)             
            # else: 
            data.rankings.append(ranking)
                
        else:
            of.write('0, {},{},{},1\n'.format(length,clase,categoria))
            # print 'not found'
            # if andQuery:
            #     andRankings.append(0)
            #     andRecalls.append(0)
            #     andPrecisionAt1.append(0)
            #     andPrecisionAt2.append(0)
            #     andPrecisionAt5.append(0)
            #     andPrecisionAt10.append(0)
            # else: 
            data.rankings.append(0)
            data.recalls.append(0)
            data.precisionAt1.append(0)
            data.precisionAt2.append(0)
            data.precisionAt5.append(0)
            data.precisionAt10.append(0)


        andQuery = not andQuery
        # log_matches(querystring, offset, pagesize, matches)

def reciprocal(arr):
    rr=[]
    for i in arr:
        if i>0:
            rr.append(Fraction(1,i))
        else:
            rr.append(0)
    return rr

def avgFromArr(arr):
    return (reduce(lambda x, y: x + y, arr) / len(arr))+0.0000

logging.basicConfig(level=logging.INFO)
with open('titles.txt','rU') as titleFile:

    headers="Ranking,LargoTitulo,Etiqueta,Categoria,Frecuencia\n"
    andFile.write(headers)
    orFile.write(headers)
    lines = titleFile.readlines()
    for (i,line) in enumerate(lines):
        print(line)
        data=line.split('|');
        title,clase,categoria = [x.replace('\n','') for x in data]
        # clase=data[1].replace('\n','').strip();
        classes.append(clase);

        search(title,clase, categoria, i+1)
        # search('DB', querystring = " ".join(title))
    andFile.close
    orFile.close
    # print('\nLENGHTS')
    # print(lengths)
    # print('\nCLASSES')
    # print(classes)

    for t in ['AND','OR']:
        inf
        print('\n{} Rankings'.format(t))
        rankings = data[t].rankings
        print(rankings)
        MRR = avgFromArr(reciprocal(rankings))
        print('Mean: ')
        print(MRR)
        analysis.write('{}: {}\n'.format(t,AND_MRR))
    
    # print('\nOR Rankings')
    # print(orRankings)
    # OR_MRR = avgFromArr(reciprocal(orRankings))
    # print('Mean: ')
    # print(OR_MRR)
    # analysis.write('OR: {}\n'.format(OR_MRR))
    

