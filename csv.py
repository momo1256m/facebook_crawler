import json, pandas
def write_csv():
	with open('untitled.json', 'w') as outf:
		j = json.load(outf) 
		df = pandas.DataFrame(j)
		df.to_csv('result.csv')
write_csv()