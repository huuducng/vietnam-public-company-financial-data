import requests, json, openpyxl

# Load json để locate mã báo cáo
f2 = open('codedict.json', 'r+')
codedict = json.load(f2)
f2.close()

f2 = open('datedict.json', 'r+')
datedict = json.load(f2)
f2.close()

f2 = open('iddict.json', 'r+')
iddict = json.load(f2)
f2.close()

f1 = open('ma.csv', 'r+')
data1 = f1.read().strip()
MASCIC = []
if data1:
  MASCIC = data1.split(',')
f1.close()

# Input period và code
year = int(input('Year?: '))
period = str(year*100+1)
data_cookie = input('Data cookie?: ')

# Bắt đầu từ đây
wb_code = openpyxl.load_workbook('CDKT.xlsx')
ws_code = wb_code.active

wb = openpyxl.Workbook()
ws = wb.active
ws.title = str(year)

# Dòng đầu
ws.cell(row=1, column=1, value='Ticker')
report_id = ws_code.cell(row=codedict['GIL'], column=datedict[period]).value
data_cookie = 'StockCode='+'GIL'+'&Unit=1&listReportDataIds[0][ReportDataId]='+str(report_id)+'&listReportDataIds[0][SortTimeType]=Time_ASC&__RequestVerificationToken'+data_cookie
report = requests.post(url='https://finance.vietstock.vn/data/GetReportDataDetailValueByReportDataIds', headers={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}, data=data_cookie).json()['data']
c = 1
lencheck = len(report)
list_index = []
for item in report:
	list_index.append(item['ReportNormId'])
	c+=1
	ws.cell(row=1, column=c, value=iddict[str(item['ReportNormId'])])

r = 1
for code in MASCIC:
	print(code)
	r+=1
	ws.cell(row=r, column=1, value=code)
	report_id = ws_code.cell(row=codedict[code], column=datedict[period]).value
	data_cookie = 'StockCode='+code+'&Unit=1&listReportDataIds[0][ReportDataId]='+str(report_id)+'&listReportDataIds[0][SortTimeType]=Time_ASC&__RequestVerificationToken'+data_cookie
	report = requests.post(url='https://finance.vietstock.vn/data/GetReportDataDetailValueByReportDataIds', headers={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}, data=data_cookie).json()['data']
	c = 1
	if len(report) == lencheck:
		for item in report:
			c+=1
			if item['ReportNormId'] == list_index[c-2]:
				ws.cell(row=r, column=c, value=item['Value1'])

wb.save('CDKT-'+str(year)+'.xlsx')
