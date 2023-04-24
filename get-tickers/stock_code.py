import requests, json, openpyxl, datetime


# VNDIRECT
response = requests.get(url='https://finfo-api.vndirect.com.vn/v4/stocks?q=type:stock,ifc~floor:HOSE,HNX,UPCOM&size=9999').json()['data']

wb = openpyxl.Workbook()
ws = wb.active

headrow = ['Mã SCIC', 'Tên công ty', 'Sàn', 'Ngày niêm yết', 'Ngày huỷ niêm yết']

for data in headrow:
	ws.cell(row=1, column=headrow.index(data)+1, value=data)

r = 2

list_code = []

for data in response:
	# print(data['code']+str(len(data['code'])))
	if len(data['code']) == 3:
		list_code.append(data['code'])
		ws.cell(row=r, column=1, value=data['code'])
		ws.cell(row=r, column=2, value=data['companyName'])
		ws.cell(row=r, column=3, value=data['floor'])
		ws.cell(row=r, column=4, value=datetime.datetime.strptime(data['listedDate'],'%Y-%m-%d').date())
		if "delistedDate" in data:
			ws.cell(row=r, column=5, value=datetime.datetime.strptime(data['delistedDate'],'%Y-%m-%d').date())
		r+=1

wb.save('Ticker-details-VND.xlsx')

str_code = ''
for item in sorted(list_code):
	str_code = str_code + item + ','

with open('ma.csv', 'w') as f:
	f.write(str_code[:-1])
f.close()