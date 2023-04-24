import requests, json, openpyxl

# Load mã chứng khoán
f1 = open('ma.csv', 'r+')
data1 = f1.read().strip()
MASCIC = []
if data1:
  MASCIC = data1.split(',')
f1.close()

# Load file json để tạo ngày
f2 = open('datedict.json', 'r+')
datedict = json.load(f2)
f2.close()

wb = openpyxl.Workbook()
ws = wb.active
ws.title='CDKT'

r = 1

for date in datedict:
	ws.cell(row=r, column=datedict[date], value=int(date))

list_report_headers_cookie = input('List report headers cookie?: ')
data_cookie = input('Data cookie?: ')

list_report_headers = {
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Cookie':list_report_headers_cookie,
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',}

for code in MASCIC:
	print(code)
	r+=1
	ws.cell(row=r, column=1, value=code)
	list_report_data = 'StockCode='+code+'&UnitedId=-1&AuditedStatusId=-1&Unit=1000&IsNamDuongLich=false&PeriodType=NAM&SortTimeType=Time_ASC&__RequestVerificationToken='+data_cookie
	list_report = requests.post(url='https://finance.vietstock.vn/data/CDKT_GetListReportData', headers=list_report_headers, data=list_report_data)
	for item in list_report.json()['data']:
		if str(item['BasePeriodBegin']) in datedict:
			c = datedict[str(item['BasePeriodBegin'])]
			ws.cell(row=r, column=c, value=item['ReportDataID'])

wb.save('CDKT.xlsx')