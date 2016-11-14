import csv

withBody = 0;
noBody = 0;
	
with open('newMarioEspinoza.csv', 'w+') as ocsvfile:
	with open('marioEspinoza.csv', 'rU') as icsvfile:
		spamwriter = csv.writer(ocsvfile, delimiter=',')
		spamreader = csv.reader(icsvfile, delimiter=',')
		spamwriter.writerow(['ID','TITLE','BODY'])
		for i,row in enumerate(spamreader):	
			if i>0:
				idText = row[0].replace('\n', ' ').strip();
				title = row[2].replace('\n', ' ').strip();
				body=''
				# try:
				body = row[3]
				# .replace('\n', ' ').strip();
				body = ' '.join(x.strip() for x in body.split())
					# text = title + ' ' +body
				# except IndexError:		
					# text = title
				

				if len(body) == 0:
					noBody=noBody+1;
					print 'Empty'
				else: 
										
					withBody=withBody+1;
					print '{}'.format(idText);
					print '{}'.format(title);
					print 'len: {}'.format(len(body));
					print 'body:"{}"'.format(body);
					spamwriter.writerow([idText,title,body])
print 'withBody: {}'.format(withBody);
print 'nobody: {}'.format(noBody);