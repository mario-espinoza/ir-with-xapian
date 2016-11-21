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

atributes = ['ReciprocalRanking','Recall','Precision@1','Precision@2','Precision@5','Precision@10','F1-Score']

DATA={};
for KEY in ['AND','OR']:
    DATA[KEY]={};
    for ATTR in atributes:
        DATA[KEY][ATTR]=[];

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
            of = orFile;
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

            # print(u"%(rank)i: #%(docid)3.3i \n %(id)s \n TITLE: %(title)s \n %(body)s \n %(class)s" % {
                    # 'rank': matchRank,
                    # 'docid': docid,
                    # 'id': fields.get('ID', u''),
                    # 'title': matchTitle,
                    # 'body': fields.get('BODY', u''),
                    # 'class': fields.get('CLASS', u'')
                    # })
            matches.append(match.docid)
            
        lenMatches = len(matches)
        ranking=0;
        reciprocalRanking=0;
        recall=0;
        precisionAt1=0;
        precisionAt2=0;
        precisionAt5=0;
        precision=0;
        f1Score=0;

        if titleId in matches:
            ranking = matches.index(titleId)+1
            # print 'INDEX :{}'.format(ranking)
            reciprocalRanking=Fraction(1,ranking);
            precision = Fraction(1,lenMatches)
            
            if ranking < 2:
                precisionAt1=precision;      
            if ranking < 3:
                precisionAt2=precision;      
            if ranking < 6:
                precisionAt5=precision
            recall=Fraction(1,1)
            f1Score=2*(precision*recall)/(precision+recall)
            
        data['ReciprocalRanking'].append(reciprocalRanking)
        data['Recall'].append(recall)
        data['Precision@1'].append(precisionAt1)
        data['Precision@2'].append(precisionAt2)
        data['Precision@5'].append(precisionAt5)
        data['Precision@10'].append(precision)
        data['F1-Score'].append(f1Score)
        of.write('1,{},{},{},{},{:f},{:f},{:f},{:f},{:f}\n'.format(ranking,length,clase,categoria,float(recall),float(precisionAt1),float(precisionAt2),float(precisionAt5),float(precision),float(f1Score)))

        andQuery = not andQuery
        # log_matches(querystring, offset, pagesize, matches)

def avgFromArr(arr):
    return (reduce(lambda x, y: x + y, arr) / len(arr))+0.0000

logging.basicConfig(level=logging.INFO)
with open('titles.txt','rU') as titleFile:

    headers="Frecuencia,Ranking,LargoTitulo,Etiqueta,Categoria,Recall,Precision@1,Precision@2,Precision@5,Precision@10,F1-Score\n"
    andFile.write(headers)
    orFile.write(headers)
    lines = titleFile.readlines()
    for (i,line) in enumerate(lines):
        # print(line)
        data=line.split('|');
        title,clase,categoria = [x.replace('\n','') for x in data]
        classes.append(clase);
        search(title,clase, categoria, i+1)
        
    andFile.close
    orFile.close
    # print('\nLENGHTS')
    # print(lengths)
    # print('\nCLASSES')
    # print(classes)

    for t in ['AND','OR']:
        for attr in atributes:
            if attr == 'ReciprocalRanking':
                tag = 'MRR'
            else: 
                tag=attr
            print('\n{} {}'.format(t,tag))
            data = DATA[t][attr];
            print(data)
            val = avgFromArr(data)
            print('{}: '.format(tag))
            print(val)
            analysis.write('{} {}: {}\n'.format(tag,t,val))
        analysis.write('\n')
    

