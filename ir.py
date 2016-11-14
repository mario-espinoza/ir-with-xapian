import xapian as xap
import json

def _query_parser(db):
    qp = xap.QueryParser()
    qp.set_stemmer(xap.Stem("english"))
    qp.set_database(db)
    qp.set_stemming_strategy(xap.QueryParser.STEM_SOME)
    return qp

indexador = xap.TermGenerator()
indexador.set_stemmer(xap.Stem("english"))
xap_doc = xap.Document()
indexador.set_document(xap_doc)
data = {"cuerpo":"This is Xapian example. It's made for my Intelligent System students",
"titulo":"The firts example"}
indexador.index_text("This is Xapian example")
indexador.index_text("It's made for my Intelligent System students")
indexador.index_text("The firts example",1,"S")
xap_doc.set_data(json.dumps(data, encoding='utf8'))
indexador2 = xap.TermGenerator()
indexador2.set_stemmer(xap.Stem("english"))
xap_doc2 = xap.Document()
indexador2.set_document(xap_doc2)
data2 = {"cuerpo":"This is another Xapian example. It's made for my Intelligent System students","titulo":"The second example"}
indexador2.index_text("This is another Xapian example")
indexador2.index_text("It's made for my Intelligent System students, too")
indexador2.index_text("The second example",1,"S")
xap_doc2.set_data(json.dumps(data2, encoding='utf8'))
indexador3 = xap.TermGenerator()
indexador3.set_stemmer(xap.Stem("english"))
xap_doc3 = xap.Document()
indexador3.set_document(xap_doc3)
data3 = {"cuerpo":"Ayesha Curry is a stupid and ignorant. She can keep on tweeting. Her muthafucking team can keep on losing, too.Fat, talkative whore, no","titulo": "The Yahoo Answers example"}
indexador3.index_text("Ayesha Curry is a stupid and ignorant")
indexador3.index_text("She can keep on tweeting")
indexador3.index_text("Her muthafucking team can keep on losing, too")
indexador3.index_text("Fat, talkative whore, no")
indexador3.index_text("The Yahoo Answers example",1,"S")
xap_doc3.set_data(json.dumps(data3, encoding='utf8'))
datb = xap.WritableDatabase('ejemploSI.db',xap.DB_CREATE_OR_OPEN)
1
datb.add_document(xap_doc)
datb.add_document(xap_doc2)
datb.add_document(xap_doc3)
datb.commit()
datb.close()
datb = xap.WritableDatabase('ejemploSI.db',xap.DB_CREATE_OR_OPEN)
qp = _query_parser(datb)
query1 = qp.parse_query("student")
enq = xap.Enquire(datb)
enq.set_query(query1)
for res in enq.get_mset(0, datb.get_doccount(), None, None):
    print res.document.get_data()
