import csv

withBody = 0;
noBody = 0;

classes={
	'1':'Opiniones',
	'2':'No respondibles',
	'3':'Particulares',
	'4':'Otros',
	'5':'Archivada',
	'6':'Web',
	'7':'Complejas',
	'8':'Web y Archivada'
}

with open('titles.txt', 'w+') as titleFile:	
	with open('dataWithBody.csv', 'w+') as ocsvfile:
		with open('marioEspinoza.csv', 'rU') as icsvfile:
			spamwriter = csv.writer(ocsvfile, delimiter=',')
			spamreader = csv.reader(icsvfile, delimiter=',')
			spamwriter.writerow(['ID','TITLE','CLASS','BODY'])
			for i,row in enumerate(spamreader):	
				if i>0:
					idText = row[0].replace('\n', ' ').strip();
					tag = row[1].replace('\n', ' ').strip();
					title = row[2].replace('\n', ' ').strip();
					body = row[3]
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
						spamwriter.writerow([idText,title,classes[tag],body]);
						titleFile.write('{}\n'.format(title));
print 'withBody: {}'.format(withBody);
print 'nobody: {}'.format(noBody);