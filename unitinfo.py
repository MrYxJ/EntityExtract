#!/usr/bin/python3
# encoding: utf-8
# Author MrYx
# @Time: 2019/5/22 19:29

from EntityExtract.caseinfo import EntityExtraction
from EntityExtract.NER import NER
import re

class unitinfo(EntityExtraction):
     def __init__(self):
         self.input_file = 'OpenLaw判决书.xlsx'
         self.result_file = 'unitinfo.json'
         self.all_items = self.xlsx_to_dict(self.input_file)
         self.cursor = self.get_mysql()
         self.analys_pos = {
             'extract_dwmc': ['当事人','庭审过程', '法院意见'],  # 可能从多个不同部分提取，所以用List
             'extract_bcfj':['判决结果','法院意见'],
             'extract_dwxz':['法院意见'],
             'extract_szdq':['法院']
         }
         self.dict = {}

     def extract_dwmc(self, content, index):
         key_word1 = ['公司', '所', '中心', '医院', '校', '小组', '政府', '局', '部',
                      '系', '室', '会', '区','书记']

         def extract_more(sen):
             try: return [x for x in NER(sen)[2] if not x.endswith('检察院') and not x.endswith('法院') and not x.endswith('看守所') and not x.endswith('公安局') and not x.endswith('派出所')]
             except: return sen
             # for key in key_word1:
             #     rex = '([\s\S]*)' + '(' + key + ')'
             #     pattern = re.compile(rex)
             #     if pattern.search(sen) != None:
             #         return pattern.search(sen).group(1) + pattern.search(sen).group(2)
             # return sen

         ans = ''
         Find  = False
         for sen in self.split_content(content, split='。'):
             if '被告人' in sen or '上诉人' in sen  or  '判决书' in sen or '被告单位' in sen:
                 #print('sen:',sen)
                 for ssen in self.split_content(sen):
                     for key in key_word1:
                         if key in ssen:
                             #print('ssen: ',ssen)
                             target = extract_more(ssen)
                             #print('target: ', target)
                             #c = input('???')
                             if target != []:
                                  Find = True
                                  ans = target[0]
                             #c = input('???')
                             break
                     if Find: break
             if Find : break

         #print('ans:',ans)
         return ans

     def extract_bcfj(self, content, index):
         def transmit(money):
             """
             将'78.9万元 或者 798900.5元 处理成保留两位小数单位为万元的浮点数'
             :param money:
             :return:
             """
             sum = 0.0;
             Flag = False;
             t = 0.1;
             for s in money:
                 if s == '.':
                     Flag = True
                 elif s == '万':
                     sum *= 10000.0
                 elif s.isdigit():
                     if Flag == False:
                         sum = sum * 10.0 + float(s)
                     else:
                         sum = sum + t * float(s); t *= 0.1
             sum = float(int(sum / 100.0)) / 100.0
             return sum
         rexs = ["(共计|共)([^\d]*)?([\d][^元]*元)",
                 "(转账|取|款|现金|收|贿|挪|回扣|人民币)([^\d]*)([\d][^元]*元)"]
         ans = ''
         Find = False
         for sen in self.split_content(content, split='。'):
             for res in rexs:
                 pattren = re.compile(res)
                 target = pattren.search(sen)
                 if target != None:
                     ssen = target.group(3)
                     Find = True;
                     index = 0
                     for i in range(len(ssen) - 3, 0, -1):
                         if ssen[i].isdigit() or ssen[i] == '.':
                             pass
                         else:
                             index = i + 1; break
                     ans = ssen[index:]
                     break
             if Find: break
         return transmit(ans)

     def extract_dwxz(self, content , index):
         """
         :param content:
         :param index:
         :return:
         """
         dicts = {'国有':'01','外商独资':'02', '民营':'03','股份制':'04',
                  '中外合资':'05','个体':'06','其他':'07','中外合作':'08','国有(央企)':'09'}

         FirstSentence = self.split_content(content,split="。")[0]
         if  '非国家工作人员' not in  FirstSentence and '国家工作人员' in FirstSentence: return '01'
         else:
             company_name = self.dict['DWMC'][index]
             if company_name == '': return '06'
             elif '股份' in company_name : return '04'
             elif '有限公司' in company_name : return '03'
             elif  '中国' in company_name : return '09'
             else : return  '01'

     def test_total(self):

         self.dict['DWMC'] = self.test_task2(self.extract_dwmc, 'extract_dwmc')
         self.dict['BCFJ'] = self.test_task2(self.extract_bcfj, 'extract_bcfj')
         self.dict['DWXZ'] = self.test_task2(self.extract_dwxz, 'extract_dwxz')
         self.dict['SZDQ'] = self.test_task2(self.extract_sadq, 'extract_szdq')

         unitinfo = {}
         dict_key_order = ['DWMC','BCFJ','DWXZ','SZDQ']
         cnt = 2
         for i in range(len(self.all_items)):
             item = { }
             for key in dict_key_order:
                 value = self.dict[key][i]
                 if value != None: item[key] = value
             unit = { }
             unit['unitinfo'] = item
             unitinfo[str(cnt)] = unit
             cnt += 1
         self.write_dict_to_json(dicts=unitinfo, filename=self.result_file)

if __name__ == '__main__':
    # def extract_more(sen):
    #     try:
    #         return [x for x in NER(sen)[2] if
    #                 not x.endswith('检察院') and not x.endswith('法院') and not x.endswith('看守所') and not x.endswith(
    #                     '公安局') and not x.endswith('派出所')]
    #     except:
    #         return sen

    # Str2 = '公诉机关清涧县人民检察院。、被告人邱某某，男，汉族，高中文化，清涧县折家坪镇财政所工作，任退耕还林专项资金出纳，现住清涧县电影院家属楼。、因涉嫌犯贪污罪于2009年5月14日被清涧县人民检察院刑事拘留，同年5月28日被执行逮捕。、现羁押于清涧县看守所。'
    # Str = '重庆市綦江区人民法院认定，被告人程某某从重庆市綦江区文龙街道办事处调至重庆市綦江区赶水镇担任中共重庆市綦江区赶水镇党委副书记、赶水镇人民政府镇长，主持赶水镇人民政府全面工作，主管财政、监察等工作'

    un = unitinfo()
    #print(un.extract_dwmc(content=Str2, index=1))
    #un.test_task2(un.extract_dwmc, 'extract_dwmc')
    #un.test_task2(un.extract_bcfj, 'extract_bcfj')

    #un.test_task2(un.extract_dwxz, 'extract_dwxz')
    un.test_total()




