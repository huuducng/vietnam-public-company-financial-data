import pandas as pd
import numpy as np
import json, datetime

# Tạo dict cho date
date_range = pd.date_range(start=datetime.datetime(2002,1,1), end=datetime.datetime.today(), freq='Y')
# print(date_range.to_numpy())
datedict = {}

value = 1
for date in pd.to_datetime(date_range.to_numpy()):
	index = (date.year+1)*100 + 1
	value +=1
	datedict.update({index:value})

with open('datedict.json', 'w') as f:
	json.dump(datedict, f)
f.close()

# Tạo dict cho mã chứng khoán
# Load mã chứng khoán
f1 = open('ma.csv', 'r+')
data1 = f1.read().strip()
MASCIC = []
if data1:
  MASCIC = data1.split(',')
f1.close()

codedict = {}
value = 1
for code in MASCIC:
	value+=1
	codedict.update({code:value})

with open('codedict.json', 'w') as f:
	json.dump(codedict, f)
f.close()