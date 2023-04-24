import requests, json

headers_cookie = input('Headers cookie? :')
data_cookie = input('Data cookie?: ')

headers = {
	'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
	'Cookie':headers_cookie,
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

data = 'stockCode=GIL&__RequestVerificationToken='+data_cookie

response = requests.post(url='https://finance.vietstock.vn/data/GetListReportNormByStockCode', headers=headers, data=data).json()['data']
indexdict = {}

for item in response:
	indexdict.update({item['ReportNormId']:item['ReportNormName']})

with open('iddict.json', 'w') as f:
	json.dump(indexdict, f)
	f.close()