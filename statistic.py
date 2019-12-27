# encoding: utf-8

import pymysql
import json 
db = pymysql.connect(host="172.16.216.161", port=3306,
		user="law", password="cistLAW1104", database="law")
cursor = db.cursor()
code_2_top = {}
whcd_2_name = {}
ajxz_2_name = {}
location_rename = {}
punish_category = ['拘役','免予刑事处罚','有期徒刑','无期徒刑','死刑']
def figout_dq():
	if len(code_2_top) > 0:
		return
	source = open("lib/pub_code_item.json","r",encoding="utf-8")
	items = json.load(source)
	items = items['RECORDS']
	tmp = {}
	code_2_name = {}
	for item in items:
		if tmp.__contains__(item['CODE']):
			# 因为还包含中国共产党员之类的其他数据
			continue
		if not item.__contains__("OWNER_CODE") or item['OWNER_CODE'] == 'top':
			tmp[item['CODE']] = item['CODE']
		else:
			tmp[item['CODE']] = item['OWNER_CODE']

		code_2_name[item['CODE']] = item['CODE_TEXT']

	for code in tmp:
		father = tmp[code]
		while father != tmp[father]:
			father = tmp[father]
		code_2_top[code] = code_2_name[father][:-1].replace(" ","")

	print("dq code 2 owner name finished")


def figout_ajxz():
	if len(ajxz_2_name.keys()) > 0:
		return
	query = 'select code_type_no,code,code_text from PUB_CODE_ITEM where code_type_no="AJXZ"'
	cursor.execute(query)
	items = cursor.fetchall()
	for item in items:
		ajxz_2_name[item[1]] = item[2]


def figout_whcd():
	if len(whcd_2_name.keys()) > 0:
		return
	query = 'select code_type_no,code,code_text from PUB_CODE_ITEM where code_type_no="WHCD"'
	cursor.execute(query)
	items = cursor.fetchall()
	for item in items:
		whcd_2_name[item[1]] = item[2]


def provinceTendency():
	figout_dq()
	figout_ajxz()
	figout_whcd()
	query = 'select ajxz,sadq from XH_CASEINFO'
	num = cursor.execute(query)
	items = cursor.fetchall()
	count = {}
	for item in items:
		if item[0] == None:
			continue
		if not code_2_top.__contains__(item[1]):
			# print("sadq not in database")
			continue
		if not ajxz_2_name.__contains__(item[0]):
			print(item[0])
		if not count.__contains__(ajxz_2_name[item[0]]):
			count[ajxz_2_name[item[0]]] = {}
		if not count[ajxz_2_name[item[0]]].__contains__(code_2_top[item[1]]):
			count[ajxz_2_name[item[0]]][code_2_top[item[1]]] = 1
		else:
			count[ajxz_2_name[item[0]]][code_2_top[item[1]]] = count[ajxz_2_name[item[0]]][code_2_top[item[1]]] + 1
	ans = {}
	ans['category'] = []
	ans['data'] = {}
	for item  in count:
		ans['data'][item] = []
		for key in count[item]:
			if not ans['category'].__contains__(key):
				ans['category'].append(key)
		for key in ans['category']:
			if count[item].__contains__(key):
				ans['data'][item].append(count[item][key])
			else:
				ans['data'][item].append(0)
	ans['legend'] = []
	for item in count:
		ans['legend'].append(item)
	return json.dumps(ans, ensure_ascii=False)


def timeTendency():
	figout_dq()
	figout_ajxz()
	figout_whcd()
	query = 'select ajxz,pjsj from XH_CASEINFO'
	num = cursor.execute(query)
	items = cursor.fetchall()
	count = {}
	year_list = []
	for item in items:
		if item[0] == None:
			continue
		if item[1] == None:
			continue
		if not ajxz_2_name.__contains__(item[0]):
			print(item[0])
		if not count.__contains__(ajxz_2_name[item[0]]):
			count[ajxz_2_name[item[0]]] = {}
		if not count[ajxz_2_name[item[0]]].__contains__(item[1].year):
			count[ajxz_2_name[item[0]]][item[1].year] = 1
		else:
			count[ajxz_2_name[item[0]]][item[1].year] = count[ajxz_2_name[item[0]]][item[1].year] + 1
		if not year_list.__contains__(item[1].year):
			year_list.append(item[1].year)
	year_list.sort()
	ans = {}
	ans['category'] = []
	ans['legend'] = []
	for year in year_list:
		ans['legend'].append(year)
	ans['data'] = {}
	for item  in count:
		ans['data'][item] = []
		ans['category'].append(item)
		for year in year_list:
			if count[item].__contains__(year):
				ans['data'][item].append(count[item][year])
			else:
				ans['data'][item].append(0)
	return  json.dumps(ans, ensure_ascii=False)


def countryCaseMap():
	figout_dq()
	figout_ajxz()
	figout_whcd()
	query = 'select sadq from XH_CASEINFO'
	num = cursor.execute(query)
	items = cursor.fetchall()
	count = {}
	for item in items:
		if item[0] == None:
			continue
		if not code_2_top.__contains__(item[0]):
			# print("sadq not in database")
			continue
		if not count.__contains__(code_2_top[item[0]]):
			count[code_2_top[item[0]]] = 0
		else:
			count[code_2_top[item[0]]] = count[code_2_top[item[0]]] + 1
	ans = {}
	ans['data'] = {}
	maxNumber = 0
	for item in count:
		if count[item] > maxNumber:
			maxNumber = count[item]
		ans['data'][item] = count[item]
	ans['maxNumber'] = maxNumber
	return  json.dumps(ans, ensure_ascii=False)


def countryCaseBar():
	figout_dq()
	figout_ajxz()
	figout_whcd()
	query = 'select sadq,pjsj from XH_CASEINFO'
	num = cursor.execute(query)
	items = cursor.fetchall()
	count = {}
	for item in items:
		if item[0] == None:
			continue
		if item[1] == None:
			continue
		if not code_2_top.__contains__(item[0]):
			# print("sadq not in database")
			continue
		if not count.__contains__(code_2_top[item[0]]):
			count[code_2_top[item[0]]] = {}
		if not count[code_2_top[item[0]]].__contains__(item[1].year):
			count[code_2_top[item[0]]][item[1].year] = 1
		else:
			count[code_2_top[item[0]]][item[1].year] = count[code_2_top[item[0]]][item[1].year] + 1

	ans = {}
	ans['category'] = []
	ans['data'] = {}
	for item  in count:
		ans['category'].append(item)
		for key in count[item]:
			if not ans['data'].__contains__(key):
				ans['data'][key] = [0 for i in range(len(ans['category']) - 1)]
			ans['data'][key].append(count[item][key])
	for year in ans['data']:
		while(len(ans['data'][year]) < len(ans['category'])):
			ans['data'][year].append(0)
	return  json.dumps(ans, ensure_ascii=False)


def countryAge(year='2018'):
	figout_dq()
	figout_ajxz()
	figout_whcd()
	sql = "select count(case when age>=18 and age<=25 then age else null end),\
		count(case when age>=26 and age<=35 then age else null end),\
		count(case when age>=36 and age<=45 then age else null end),\
		count(case when age>=46 and age<=55 then age else null end),\
		count(case when age>=56 and age<=65 then age else null end),\
		count(case when age>=66 then age else null end)\
		from XH_PERSONINFO join XH_CASEINFO on XH_PERSONINFO.AJID = XH_CASEINFO.UUID \
		where substr(pjsj,1,4) = " + year
	try:
		cursor.execute(sql)
		res = cursor.fetchone()
		count = {year:list(res)}
		# print(res)
		print(count)
	except:
		res = ""
		print("age not in database")
		count = {}
	return  json.dumps(count)


def countrySex(year='2018'):
	figout_dq()
	figout_ajxz()
	figout_whcd()
	sql = "select count(case when xb = 1 then xb else null end) as `男`,\
		count(case when xb = 2 then xb else null end) as `女`,\
		count(case when xb = 9 then xb else null end) as `未知`\
		from XH_PERSONINFO join XH_CASEINFO on XH_PERSONINFO.AJID = XH_CASEINFO.UUID\
		where substr(pjsj,1,4) = " + year
	try:
		cursor.execute(sql)
		res = cursor.fetchone()
		count = {'男':res[0],'女':res[1]}
		# print(res)
		ans = {year:count}
	except:
		res = ""
		print("gender not in database")
		ans = {year:{'男':0,'女':0}}
	return  json.dumps(ans, ensure_ascii=False)


def countryJob():
	figout_dq()
	figout_ajxz()
	figout_whcd()
	sql = "select \
			substr(pjsj,1,4) as year,\
			count(zw) as zw_count,\
			zw\
		from XH_PERSONINFO\
		join\
		XH_CASEINFO\
		on XH_PERSONINFO.AJID = XH_CASEINFO.UUID\
		group by substr(pjsj,1,4),zw"
	# try:
	cursor.execute(sql)
	data = cursor.fetchall()
	count_category = {}
	for item in data:
		job = item[2]
		if job == '':
			job = '其他'
		if not count_category.__contains__(job):
			count_category[job] = item[1]
		else:
			count_category[job] = count_category[job] + item[1]
	count_category_top = sorted(count_category.items(), key=lambda k:k[1], reverse=True)
	count_category_top = count_category_top[:11]
	for i in range(len(count_category_top)):
		if count_category_top[i][0] == '其他':
			count_category_top.pop(i)
			break
	ans = {}
	ans['category'] = []
	for item in count_category_top:
		ans['category'].append(item[0])
	ans['data'] = {}
	tmp = {}
	for item in data:
		if item[0] == None or item[1] == None or item[2] == None:
			continue
		if not tmp.__contains__(item[0]):
			tmp[item[0]] = {}
		if not ans['category'].__contains__(item[2]):
			if not tmp[item[0]].__contains__('其他'):
				tmp[item[0]]['其他'] = item[1]
			else:
				tmp[item[0]]['其他'] = tmp[item[0]]['其他'] + item[1]
		else:
			if not tmp[item[0]].__contains__(item[2]):
				tmp[item[0]][item[2]] = item[1]
			else:
				tmp[item[0]][item[2]] = tmp[item[0]][item[2]] + item[1]
	ans['category'].append('其他')
	for year in tmp:
		ans['data'][year] = []
		for category in ans['category']:
			if tmp[year].__contains__(category):
				ans['data'][year].append(tmp[year][category])
			else:
				ans['data'][year].append(0)
	# except:
	# 	res = ""
	# 	# print("gender not in database")
	# 	count = {}
	return  json.dumps(ans, ensure_ascii=False)


def countryEdu():
	figout_dq()
	figout_ajxz()
	figout_whcd()
	query = 'select substr(pjsj,1,4),whcd from XH_PERSONINFO join XH_CASEINFO on XH_PERSONINFO.AJID = XH_CASEINFO.UUID'
	num = cursor.execute(query)
	items = cursor.fetchall()
	count = {}
	for item in items:
		if item[0] == None:
			continue
		if item[1] == None:
			continue
		if not whcd_2_name.__contains__(item[1]):
			# print("whcd not in database")
			continue
		if not count.__contains__(item[0]):
			count[item[0]] = {}
		if not count[item[0]].__contains__(whcd_2_name[item[1]]):
			count[item[0]][whcd_2_name[item[1]]] = 0
		else:
			count[item[0]][whcd_2_name[item[1]]] = count[item[0]][whcd_2_name[item[1]]] + 1
	ans = {}
	ans['category'] = []
	ans['data'] = {}
	for item in count:
		ans['data'][item] = []
		for key in count[item]:
			if not ans['category'].__contains__(key):
				ans['category'].append(key)
		for category in ans['category']:
			if count[item].__contains__(category):
				ans['data'][item].append(count[item][category])
			else:
				ans['data'][item].append(0)
	for year in ans['data']:
		while len(ans['data'][year]) < len(ans['category']):
			ans['data'][year].append(0)
	return  json.dumps(ans, ensure_ascii=False)


def crime(year='2018'):
	figout_dq()
	figout_ajxz()
	figout_whcd()
	sql = "select \
			substr(pjsj,1,4) as year,\
			count(ajxz) as ajxz_count,\
			ajxz\
		from XH_CASEINFO\
		where substr(pjsj,1,4) = " + year + \
		" group by year,ajxz"
		
	# try:
	cursor.execute(sql)
	data = cursor.fetchall()
	tmp_ans = {}
	for item in data:
		ajxz = item[2]
		if ajxz is None or ajxz == '':
			ajxz = '其他'
		tmp_ans[ajxz] = item[1]
	ans = {}
	ans['category'] = []
	for item in ajxz_2_name:
		ans['category'].append(ajxz_2_name[item])
	ans['data'] = {year:[]}
	tmp = {}
	for item in ajxz_2_name:
		if tmp_ans.__contains__(item):
			ans['data'][year].append(tmp_ans[item])
		else:
			ans['data'][year].append(0)
	ans = {year:ans}
	# except:
	# 	res = ""
	# 	# print("gender not in database")
	# 	count = {}
	return  json.dumps(ans, ensure_ascii=False)


def crimeTendency():
	figout_dq()
	figout_ajxz()
	figout_whcd()
	sql = "select \
			substr(pjsj,1,4) as year,\
			count(ajxz) as ajxz_count,\
			ajxz\
		from XH_CASEINFO\
		group by year,ajxz"
		
	# try:
	cursor.execute(sql)
	data = cursor.fetchall()
	tmp_ans = {}
	year_list = []
	for item in data:
		ajxz = item[2]
		if ajxz is None or ajxz == '':
			ajxz = '其他'
		elif ajxz_2_name.__contains__(ajxz):
			ajxz = ajxz_2_name[ajxz]
		year = item[0]
		if year is None or year == '':
			continue
		if not year_list.__contains__(year):
			year_list.append(year)
		if not tmp_ans.__contains__(ajxz):
			tmp_ans[ajxz] = {}
		tmp_ans[ajxz][year] = item[1]
	year_list.sort()
	ans = {}
	ans['category'] = []
	for item in ajxz_2_name:
		ans['category'].append(ajxz_2_name[item])
	ans['legend'] = []
	for year in year_list:
		ans['legend'].append(year)
	ans['data'] = {}
	tmp = {}
	for category in ans['category']:
		if tmp_ans.__contains__(category):
			ans['data'][category] = []
			for year in year_list:
				if tmp_ans[category].__contains__(year):
					ans['data'][category].append(tmp_ans[category][year])
				else:
					ans['data'][category].append(0)
		else:
			ans['data'][category] = []
			for year in year_list:
				ans['data'][category].append(0)
	# except:
	# 	res = ""
	# 	# print("gender not in database")
	# 	count = {}
	return  json.dumps(ans, ensure_ascii=False)


def punish(year='2018'):
	figout_dq()
	figout_ajxz()
	figout_whcd()
	sql = "select \
			substr(pjsj,1,4) as year,\
			xfzl\
		from XH_CRIMEINFO\
		join\
		XH_CASEINFO\
		on XH_CRIMEINFO.AJID = XH_CASEINFO.UUID\
		where substr(pjsj,1,4) = " + year
	# try:
	cursor.execute(sql)
	data = cursor.fetchall()
	tmp_ans = {}
	year_list = []
	for item in data:
		year = item[0]
		if year is None or year == '':
			continue
		xfzl = item[1]
		if xfzl is None or xfzl == '':
			xfzl = '其他'
		for category in punish_category:
			if xfzl.startswith(category):
				xfzl = category
				break
		if not punish_category.__contains__(xfzl):
			continue
		if not tmp_ans.__contains__(xfzl):
			tmp_ans[xfzl] = 1
		else:
			tmp_ans[xfzl] = tmp_ans[xfzl] + 1
	year_list.sort()
	ans = {}
	ans['category'] = []
	for category in punish_category:
		ans['category'].append(category)
	ans['data'] = {year:[]}
	for item in punish_category:
		if tmp_ans.__contains__(item):
			ans['data'][year].append(tmp_ans[item])
		else:
			ans['data'][year].append(0)
	# except:
	# 	res = ""
	# 	# print("gender not in database")
	# 	count = {}
	ans = {year:ans}
	return  json.dumps(ans, ensure_ascii=False)


def punishTendency(year='2018'):
	figout_dq()
	figout_ajxz()
	figout_whcd()
	sql = "select \
			substr(pjsj,1,4) as year,\
			xfzl\
		from XH_CRIMEINFO\
		join\
		XH_CASEINFO\
		on XH_CRIMEINFO.AJID = XH_CASEINFO.UUID"
		
	# try:
	cursor.execute(sql)
	data = cursor.fetchall()
	tmp_ans = {}
	year_list = []
	for item in data:
		year = item[0]
		if year is None or year == '':
			continue
		if not year_list.__contains__(year):
			year_list.append(year)
		xfzl = item[1]
		if xfzl is None or xfzl == '':
			xfzl = '其他'
		for category in punish_category:
			if xfzl.startswith(category):
				xfzl = category
				break
		if not punish_category.__contains__(xfzl):
			continue
		if not tmp_ans.__contains__(xfzl):
			tmp_ans[xfzl] = {}
		if not tmp_ans[xfzl].__contains__(year):
			tmp_ans[xfzl][year] = 1
		else:
			tmp_ans[xfzl][year] = tmp_ans[xfzl][year] + 1
	year_list.sort()
	ans = {}
	ans['category'] = []
	for category in punish_category:
		ans['category'].append(category)
	ans['legend'] = []
	for year in year_list:
		ans['legend'].append(year)
	ans['data'] = {}
	for category in punish_category:
		ans['data'][category] = []
		if tmp_ans.__contains__(category):
			for year in year_list:
				if tmp_ans[category].__contains__(year):
					ans['data'][category].append(tmp_ans[category][year])
				else:
					ans['data'][category].append(0)
		else:
			for year in year_list:
				ans['data'][category].append(0)
	# except:
	# 	res = ""
	# 	# print("gender not in database")
	# 	count = {}
	return  json.dumps(ans, ensure_ascii=False)


def main():
	figout_dq()
	figout_ajxz()
	figout_whcd()
	statistic_result = {}
	provinceTendency_ans = provinceTendency()
	statistic_result['provinceTendency'] = provinceTendency_ans
	timeTendency_ans = timeTendency()
	statistic_result['timeTendency'] = timeTendency_ans
	countryCaseMap_ans = countryCaseMap()
	statistic_result['countryCaseMap'] = countryCaseMap_ans
	countryEdu_ans = countryEdu()
	statistic_result['countryEdu'] = countryEdu_ans
	countryJob_ans = countryJob()
	statistic_result['countryJob'] = countryJob_ans
	statistic_result['countryAge'] = {}
	statistic_result['countrySex'] = {}
	statistic_result['crime'] = {}
	statistic_result['punish'] = {}
	statistic_result['punishTendency'] = {}
	for year in range(1990, 2020):
		year = str(year)
		countryAge_ans = countryAge(year)
		countrySex_ans = countrySex(year)
		crime_ans = crime(year)
		punish_ans = punish(year)
		punishTendency_ans = punishTendency(year)
		statistic_result['countryAge'][year] = countryAge_ans
		statistic_result['countrySex'][year] = countrySex_ans
		statistic_result['crime'][year] = crime_ans
		statistic_result['punish'][year] = punish_ans
		statistic_result['punishTendency'][year] = punishTendency_ans
	statistic_result['countryAge']['合计'] = {'合计':[]}
	tmp = json.loads(statistic_result['countryAge']['1990'])
	for i in range(len(tmp['1990'])):
		statistic_result['countryAge']['合计']['合计'].append(0)
	statistic_result['countrySex']['合计'] = {'合计':{'男':0,'女':0}}
	statistic_result['crime']['合计'] = {'合计':{'category':[],'data':{'合计':[]}}}
	tmp = json.loads(statistic_result['crime']['1990'])
	for key in tmp['1990']['category']:
		statistic_result['crime']['合计']['合计']['category'].append(key)
		statistic_result['crime']['合计']['合计']['data']['合计'].append(0)
	statistic_result['punish']['合计'] = {'合计':{'category':[],'data':{'合计':[]}}}
	tmp = json.loads(statistic_result['crime']['1990'])
	for key in tmp['1990']['category']:
		statistic_result['punish']['合计']['合计']['category'].append(key)
		statistic_result['punish']['合计']['合计']['data']['合计'].append(0)

	for year in range(1990,2020):
		year = str(year)
		tmp = json.loads(statistic_result['countryAge'][year])
		for i in range(len(statistic_result['countryAge']['合计']['合计'])):
			statistic_result['countryAge']['合计']['合计'][i] += tmp[year][i]
		tmp = json.loads(statistic_result['countrySex'][year])
		statistic_result['countrySex']['合计']['合计']['男'] += tmp[year]['男']
		statistic_result['countrySex']['合计']['合计']['女'] += tmp[year]['女']
		tmp = json.loads(statistic_result['crime'][year])
		for i in range(len(statistic_result['crime']['合计']['合计']['data']['合计'])):
			statistic_result['crime']['合计']['合计']['data']['合计'][i] += tmp[year]['data'][year][i]
		tmp = json.loads(statistic_result['crime'][year])
		for i in range(len(statistic_result['crime']['合计']['合计']['data']['合计'])):
			statistic_result['punish']['合计']['合计']['data']['合计'][i] += tmp[year]['data'][year][i]
	statistic_result['countryAge']['合计'] = json.dumps(statistic_result['countryAge']['合计'])
	statistic_result['countrySex']['合计'] = json.dumps(statistic_result['countrySex']['合计'])
	statistic_result['crime']['合计'] = json.dumps(statistic_result['crime']['合计'])
	statistic_result['punish']['合计'] = json.dumps(statistic_result['punish']['合计'])


	crimeTendency_ans = crimeTendency()
	statistic_result['crimeTendency'] = crimeTendency_ans
	countryCaseBar_ans = countryCaseBar()
	statistic_result['countryCaseBar'] = countryCaseBar_ans
	output_file = open("static_result_yjj.json", "w+", encoding="utf-8")
	json.dump(statistic_result,output_file, ensure_ascii=False)
	print("热力图")
	print(countryCaseMap_ans)
	print("案件分布统计")
	print(countryCaseBar_ans)
	print("性别统计")
	print(countrySex_ans)
	print("年龄段统计")
	print(countryAge_ans)
	print("文化程度分布统计")
	print(countryEdu_ans)
	print("职务分布统计")
	print(countryJob_ans)
	print("罪名最终统计")
	print(crime_ans)
	print("罪名罪种变化趋势统计")
	print(crimeTendency_ans)
	print("刑法种类分析")
	print(punish_ans)
	print("刑法种类特征分析")
	print(punishTendency_ans)
	print("高频罪名空间分布统计")
	print(provinceTendency_ans)
	print("高频罪名时间分布统计")
	print(timeTendency_ans)

	# sql = 'select * from XH_CASEINFO limit '
if __name__ == "__main__":
	main()