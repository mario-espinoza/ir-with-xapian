import csv,io

withBody = 0;
noBody = 0;

# classes={
# 	'1':'Opiniones',
# 	'2':'No respondibles',
# 	'3':'Particulares',
# 	'4':'Otros',
# 	'5':'Archivada',
# 	'6':'Web',
# 	'7':'Complejas',
# 	'8':'Web y Archivada'
# }

with io.open('titlesGonzalez.txt', 'w+', encoding='utf-8') as titleFile:	
	with open('dataWithBodyGonzalez.csv', 'w+') as ocsvfile:
		with open('gonzalez.csv', 'rU') as icsvfile:
			spamwriter = csv.writer(ocsvfile, delimiter=',')
			spamreader = csv.reader(icsvfile, delimiter=';')
			#id_Pregunta;Titulo;Cuerpo;Categoria;Clase;HWeb;HYA;NResp;Seguidores
			#spamwriter.writerow(['ID','TITLE','CLASS','BODY'])
			spamwriter.writerow(['ID','TITLE','BODY','CAT','CLASS'])
			for i,row in enumerate(spamreader):	
				if i>0:
					idText = row[0].replace('\n', ' ').strip();
					tag = row[4].replace('\n', ' ').strip();
					title = row[1].replace('\n', ' ').strip();
					body = row[2]
					cat = row[3].replace('\n', ' ').strip();
					body = ' '.join(x.strip() for x in body.split())

					if len(body) == 0:
						noBody=noBody+1;
						print 'Empty'
					else: 
											
						withBody=withBody+1;
						print '{}'.format(idText);
						print '{}'.format(title);
						print 'len: {}'.format(len(body));
						print 'body:"{}"'.format(body);
						# spamwriter.writerow([idText,title,classes[tag],body]);
						spamwriter.writerow([idText,title,body,cat,tag]);
						titleFile.write(unicode(title+'\n', errors='ignore'));
print 'withBody: {}'.format(withBody);
print 'nobody: {}'.format(noBody);