#!/usr/bin/python3
# encoding: utf-8
# Author MrYx
# @Time: 2019/5/30 15:42

import json, re, xlrd , datetime, sys,time
import io
import sys
import cpca

from EntityExtract.caseinfo import EntityExtraction

class CrimePenalty(EntityExtraction):
     def  __init__(self):
         self.input_file = 'OpenLaw判决书.xlsx'
         self.result_file = 'crimepenalty.json'
         self.all_items = self.xlsx_to_dict(self.input_file)
         self.analys_pos = {
             'extract_xm':['判决结果', '庭审过程'],
             'extract_xscf': ['判决结果','庭审过程']  # 可能从多个不同部分提取，所以用List
         }
         self.dict = {}
         self.cnt1=0; self.cnt2=0

     def extract_xm(self, content, id):
         judgement = content[content.find('判决如下') + 5:]
         defendant =  []
         pattern = re.compile(r'(上诉人|被告人|（原审被告人）)([\u4e00-\u9fa5＊A-Za-z0-9]+)(犯|无|（)')
         for  item  in pattern.findall(judgement):
             if item[1] not in defendant and len(item[1])<=5:
                 if defendant != [] :
                     if defendant[-1] not in item[1] : defendant.append(item[1])
                 else: defendant.append(item[1])

         return defendant

     def del_list_val(self, list, property, val):
         for item in list:
             if item.__contains__(property) and item[property] == val:
                 list.remove(item)
                 break

     def extract_xscf(self, content, id):
         def chinese2digits(uchars_chinese):
             if uchars_chinese == None : return None
             if uchars_chinese.isdigit(): return int(uchars_chinese)

             common_used_numerals = {'零': 0, '一': 1, '二': 2,'两':2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                                        '十': 10}
             total = 0
             r = 1
             for i in range(len(uchars_chinese) - 1, -1, -1):
                 val = common_used_numerals.get(uchars_chinese[i])
                 if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
                     if val > r:
                         r = val
                         total = total + val
                     else:
                         r = r * val
                 elif val >= 10:
                     if val > r:
                         r = val
                     else:
                         r = r * val
                 else:
                     total = total + r * val
             return total
         def find_index(list, name):
             """
             找到指定被告人的下标
             :return:
             """
             for index, item  in enumerate(list):
                 if item['被告人'] == name :
                     return index

         ans = []
         judgement = content[content.find('判决如下') + 5:]
         #print('Defendant:', self.dict['XM'][id])
         for name in self.dict['XM'][id]:
             ans.append({'被告人': name,'刑罚':{'是否缓刑':'否','附加刑':{'罚金项':'无','剥夺政治权利':'否','没收财产':'无'}}})

         for sen in self.split_content(judgement, split= '。'):
             if '撤销' in sen: continue
             for name in self.dict['XM'][id]:
                 if name in sen :
                     index = find_index(ans, name)
                     if '有期' in sen:
                         ans[index]['刑罚']['刑法种类'] = {'有期徒刑':'二十五年以上'}
                         pattern = re.compile(r'(有期[限]?[徒]?[刑]?[年]?)([一二两三四五六七八九十\d]+)(年|，)?')
                         year = pattern.findall(sen)
                         try:
                            year = year[-1][1]
                         except Exception :
                             #print('Sen:', sen)
                             year = None
                         if year !=None and '月' in year: year = '零' #少于一年只有月

                         try:
                            num = chinese2digits(year)
                         except  Exception as e:
                             #print('Error sen:', sen, '\nyear:', year)
                             num = 1
                         if num == None : ans[index]['刑罚']['刑法种类']['有期徒刑'] = '年限未知'
                         elif num < 5: ans[index]['刑罚']['刑法种类']['有期徒刑'] = '五年以下'
                         elif num>=5 and num <10: ans[index]['刑罚']['刑法种类']['有期徒刑'] = '五年以上，十年以下'
                         elif num>=10 and num<15: ans[index]['刑罚']['刑法种类']['有期徒刑'] = '十年以上，十五年以下'
                         elif num>=15 and num<20: ans[index]['刑罚']['刑法种类']['有期徒刑'] = '十五年以上，二十年以下'
                         elif num>20 and num<25: ans[index]['刑罚']['刑法种类']['有期徒刑'] = '二十年以上，二十五年以下'
                         #print(punish)
                     elif '无期' in sen: ans[index]['刑罚']['刑法种类'] = '无期徒刑'
                     elif '死刑' in sen:  ans[index]['刑罚']['刑法种类'] = '死刑'
                     elif '拘役' in sen: ans[index]['刑罚']['刑法种类'] = '拘役'
                     elif '免于刑事处罚'in sen:   ans[index]['刑罚']['刑法种类'] = '免于刑事处罚'

                     if '缓刑' in sen:  ans[index]['刑罚']['是否缓刑'] = '是'
                     if '没收个人财产' in sen:
                         #print('sen:',sen)
                         #self.cnt1+=1
                         ans[index]['刑罚']['附加刑']['没收个人财产'] = '有'
                         pattern = re.compile(r'(没收个人财产)([^元]+)(元)')
                         target = pattern.search(sen)
                         if target != None :
                             #self.cnt2+=1
                             ans[index]['刑罚']['附加刑']['没收个人财产'] = target.group(2) + target.group(3)
                     if '罚金' or '上缴' in sen:
                         #self.cnt1 += 1
                         pattern = re.compile(r'(人民币)([^元]+)(元)')
                         target = pattern.search(sen)
                         ans[index]['刑罚']['附加刑']['罚金项'] = '有'
                         if target != None:
                             #self.cnt2 += 1
                             ans[index]['刑罚']['附加刑']['罚金项'] = target.group(1)+ target.group(2) + target.group(3)
                     if '剥夺政治权利' in sen: ans[index]['刑罚']['附加刑']['是否缓刑'] = '是'
         #print(ans)
         return ans

     def test_task2(self, function, function_name):
         anss = []
         t1 = time.time()
         for index, item in enumerate(self.all_items):
             ans = ''
             for pos in self.analys_pos[function_name]:
                 if item[pos] == '': continue
                 ans = function(item[pos], index)
                 if ans != []:  break
             if ans == [] and function_name == 'extract_dwmc' :  ans  = self.all_items[index]['被告'].split('、')
             anss.append(ans)
         print('Cost [%s]\'s [%s]  has completed!' % (time.time() - t1, function_name))
         return anss

     def test_total(self):
         self.dict['XM'] = self.test_task2(self.extract_xm, 'extract_xm')
         self.dict['XSCF'] = self.test_task2(self.extract_xscf, 'extract_xscf')

         unitinfo = {}
         cnt = 2
         for i in range(len(self.all_items)):
             unit = {}
             unit['punishment'] = self.dict['XSCF'][i]
             unitinfo[str(cnt)] = unit
             cnt += 1
         print('cnt1:',self.cnt1, ' cnt2:',self.cnt2)
         self.write_dict_to_json(dicts=unitinfo, filename=self.result_file)

if __name__ == '__main__':
    cp = CrimePenalty()
    cp.test_total()

    #cp.test_task2(cp.extract_xm, 'extract_xm')
    #cp.test_task2(cp.extract_xscf,'extract_xscf')

