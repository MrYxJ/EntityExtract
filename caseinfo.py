#!/usr/bin/python3
# encoding: utf-8
# Author MrYx
# @Time: 2019/5/6 16:53

import json, re, xlrd , datetime, sys
import jieba.posseg as pseg
import io
import sys
import cpca
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

class EntityExtraction():
    def __init__(self):
        '''
        这里analys_pos定义每个抽取任务从excel的哪个部分抽取
        '''
        self.input_file = 'OpenLaw判决书.xlsx'
        self.result_file = 'caseinfo.json'
        self.all_items = self.xlsx_to_dict(self.input_file)
        self.analys_pos = {
            'extract_ajxz': ['案由'],   #可能从多个不同部分提取，所以用List
            #'extract_ajlx': ['当事人', '判决结果', '庭审过程'],
            'extract_unitcode_and_top': ['法院'],
            'extract_hyly':['案由', '庭审过程'],
            'extract_sahj':['庭审过程'],
            'extract_afcs':['庭审过程'],
            'extract_lasj':['庭审过程'],
            'extract_pjsj':['判决日期'],
            'extract_sadq':['法院'],
            'extract_sasj':['庭审过程'],
            'extract_saje':['庭审过程'],
            'extract_aqzy':['庭审过程'],
        }
        self.dict = {}
        self.load_china_regions()

    def xlsx_to_dict(self, filename):
        """
        将xlsx的文档读成Dict构成的List，xlsx第一列属性为Dict的Key。
        :param filename: xlsx的文件路径
        :return:
        """
        try:
            file = xlrd.open_workbook(filename)
        except:
            print("open [%s]'s file failed!" % filename)

        table = file.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        dicts = []
        dict_name = {}  # 存下xlsx文件每列一一对应数据属性名称

        for pos_i, value in enumerate(table.row_values(0)):
            dict_name[pos_i] = value

        for pos_i in range(1, nrows):
            dict = { }
            for pos_j in range(1, ncols):
                if table.cell_type(pos_i, pos_j) == 3:  # 如果excel某一列的为时间格式
                    data = xlrd.xldate_as_tuple(table.cell_value(pos_i, pos_j), 0)
                    value = datetime.datetime(*data).strftime("%Y-%m-%d")
                else:
                    value = table.cell_value(pos_i, pos_j)
                dict[dict_name[pos_j]] = value
            dicts.append(dict)
        return dicts

    def write_dict_to_json(self, dicts, filename):
        """
        将dict写入json文件
        :param dicts:
        :param filename:
        :return:
        """
        with open(filename, "w") as f:
            f.write(json.dumps(dicts, ensure_ascii=False, indent=3))
            print("写入[%s]文件完成..." % filename)

    def split_content(self,content , split = None):
        """
        字符串的切割
        :param content:
        :param split:
        :return:
        """
        if split == None : split = '[、，,。；;]'
        pattern = re.compile(split)
        return pattern.split(content)

    def test_task(self,function, function_name):
        """
        测试单个任务结果
        :param function:
        :param function_name:
        :return:
        """
        anss = []
        for index, item in enumerate(self.all_items):
            ans = None
            contents = []
            for pos in self.analys_pos[function_name]:
                contents.append(item[pos])
            ans = function(contents, index)
            if ans == 0:
                print(str(index) + "\n" + str(item))
                break
            anss.append(ans)
        print(function_name + ' has completed!')
        return anss

    def test_task2(self, function, function_name):
        """
        测试单个任务结果，MrYx版本
        :param function:
        :param function_name:
        :return:
        """
        anss = []
        for index, item in enumerate(self.all_items):
            ans = None
            for pos in self.analys_pos[function_name]:
                ans = function(item[pos], index)
                if ans != [] :
                    anss.append(ans)
                    break
            if ans == []: anss.append([])
        print(function_name + ' has completed!')
        return anss

    def test_task_duo(self,function, function_name):
        """
        测试单个任务结果
        :param function:
        :param function_name:
        :return:
        """
        anss_1 = []
        anss_2 = []
        for index, item in enumerate(self.all_items):
            ans = None
            # for pos in self.analys_pos[function_name]:
            #     ans = function(item[pos], index)
            #     if ans != [] :
            #         anss.append(ans)
            #         break
            # if ans == []: anss.append([])
            contents = []
            for pos in self.analys_pos[function_name]:
                contents.append(item[pos])
            ans_1, ans_2 = function(contents, index)
            anss_1.append([ans_1])
            anss_2.append([ans_2])
        print(function_name + ' has completed!')
        return anss_1, anss_2

    def test_total(self):
        '''
        最后运行的程序
        :param test_file:
        :return:
        '''
        print('input: ', self.input_file)

        # self.dict['AJXZ'] = self.test_task(self.extract_ajxz, 'extract_ajxz')
        # self.dict['TOP_UNITCODE'], self.dict['UNITCODE'] = self.test_task_duo(self.extract_unitcode_and_top, 'extract_unitcode_and_top')
        # self.dict['HYLY'] = self.test_task(self.extract_hyly, 'extract_hyly')
        # self.dict['LASJ'] = self.test_task(self.extract_lasj, 'extract_lasj')
        # MrYx
        self.dict['PJSJ'] = self.test_task2(self.extract_pjsj, 'extract_pjsj')
        self.dict['SADQ'] = self.test_task2(self.extract_sadq, 'extract_sadq')
        self.dict['SASJ'] = self.test_task2(self.extract_sasj, 'extract_sasj')
        self.dict['SAJE'] = self.test_task2(self.extract_saje, 'extract_saje')

        caseinfo = {}
        dict_key_order = ['PJSJ','SADQ', 'SASJ', 'SAJE']

        cnt = 2
        for i in range(len(self.all_items)):
            item = {}
            for key in dict_key_order:
                value = self.dict[key][i]
                if value != None: item[key] = value
            cas = {}
            cas['caseinfo'] = item
            caseinfo[str(cnt)] = cas
            cnt +=1
        self.write_dict_to_json(dicts=caseinfo, filename=self.result_file)

    def extract_ajxz(self, content, id): # id为第几个item索引
        return content

    def extract_ajlx(self, contents, id):
        re = 0
        for content in contents:
            if re == 0 and content.__contains__("被告人"):
                re = 1
            if content.__contains__("被告单位"):
                return 2
        return re

    def extract_unitcode_and_top(self, contents, id):
    #     根据省市县表，来查最长匹配
        for content in contents:
    #         实际上就一个
            if len(content) == 0:
                return "", ""
            for country in self.country2city:
                if content.__contains__(country):
                    return self.city2province[self.country2city[country]], self.city2province[self.country2city[country]] + self.country2city[country] + country
            for city in self.city2province:
                if content.__contains__(city):
                    return self.city2province[city], self.city2province[city] + city
                if city.endswith("市"):
                    if content.__contains__(city[:-1]):
                        return self.city2province[city], self.city2province[city] + city
            for province in self.province_list:
                if content.__contains__(province):
                    return province, province
        return "", ""

    def extract_hyly(self, contents, index):
        count = 0
        for content in contents:
            if count == 11:
                break
            if (count%10) == 0:
                if content.__contains__("行贿"):
                    count = count + 1
            if (count/10) == 0:
                if content.__contains__("受贿"):
                    count = count + 10
        if count == 0:
            for content in contents:
                if content.__contains__("贿赂"):
                    count = 11
        ans = ""
        if (count%10) == 1:
            ans = ans + "行贿"
        if (count/10) == 1:
            ans = ans + "受贿"
        return ans

    def extract_sahj(self, contents, index):
        return contents[0]

    def extract_afcs(self, contents, index):
        #     根据省市县表，来查最长匹配
        for content in contents:
            #         实际上就一个
            if len(content) == 0:
                return "", ""
            for country in self.country2city:
                if content.__contains__(country):
                    return self.city2province[self.country2city[country]], self.city2province[
                        self.country2city[country]] + self.country2city[country] + country
            for city in self.city2province:
                if content.__contains__(city):
                    return self.city2province[city], self.city2province[city] + city
                if city.endswith("市"):
                    if content.__contains__(city[:-1]):
                        return self.city2province[city], self.city2province[city] + city
            for province in self.province_list:
                if content.__contains__(province):
                    return province, province
        return "", ""

    def extract_lasj(self, contents, index):
        pattern = "[0-9]+年[0-9]+月[0-9]+日"
        key = "立案"
        lasj = ""
        for content in contents:
            if content.__contains__(key):
                index = content.index(key)
                search_result = re.finditer(pattern, content)
                distance = sys.maxsize
                for item in search_result:
                    if item.end() < index:
                        tmp_distance = index - item.end()
                    else:
                        tmp_distance = item.start() - index
                    if tmp_distance < distance:
                        distance = tmp_distance
                        lasj = item.group()
                        return lasj
        return lasj

    def load_china_regions(self):
        self.province_list = []
        self.country2city = {}
        self.city2province = {}
        province_file = open("lib/province.json", "r", encoding="utf-8")
        provinces = json.load(province_file)
        for province in provinces:
            self.province_list.append(province['name'])
        city_file = open("lib/city.json", "r", encoding="utf-8")
        cities = json.load(city_file)
        code2city = {}
        for province_code in cities:
            for city in cities[province_code]:
                code2city[city['id']] = city['name']
                self.city2province[city['name']] = city['province']
        country_file = open("lib/country.json", "r", encoding="utf-8")
        countries = json.load(country_file)
        for city_code in countries:
            if not code2city.__contains__(city_code):
                print(city_code)
                print("ERROR!")
            for country in countries[city_code]:
                self.country2city[country['name']] = code2city[city_code]

    def test_method(self):
        for index, item in enumerate(self.all_items):
            if self.extract_ajlx(item, index) == 0:
                print(item)
        print("finish")

    def extract_pjsj(self, content, id):
        """
        直接取
        :param content:
        :param id:
        :return:
        """
        return content

    def extract_sadq(self, content, id):
        """
        先用区|县|旗|州|省，再用jieba分地名
        :param content:
        :param id:
        :return:
        """
        retList = []
        contentList = [content]
        szdq = cpca.transform(contentList)
        #print(szdq['省'].tolist())
        if content == szdq['地址'].tolist()[0] or (len(content) > len(szdq['省'].tolist()[0]) and szdq['市'].tolist()[0] == ''):
            szdq = cpca.transform(contentList, cut=False)
        retList += szdq['省'].tolist()
        retList += szdq['市'].tolist()
        retList += szdq['区'].tolist()
        #print(retList)
        return retList

    def extract_sasj(self,content, id):
        """
        用正则匹配一下，然后取两个区间最大，然后一些出生后，判定细节处理一下
        :param content:
        :param id:
        :return:
        """
        def compare_time(time1,time2):
            def cal(time):
                sum =0 ; t= 0
                for s in time:
                    if s == '年' : sum += t*365; t = 0
                    elif s == '月': sum += t*30; t = 0
                    elif s =='日' : sum +=t
                    else : t = t*10+int(s)
                return sum
            return cal(time1) >= cal(time2)
        rex = '([\d]+年)([\d]*月?)([\d]*日?)'
        minn_time = '2020年'
        maxx_time = '1900年'

        for sen in self.split_content(content, split='。'):
            if '出生' in sen: continue
            patten = re.compile(rex)
            targets = patten.findall(sen)
            for target in targets:
                time = target[0] + target[1] + target[2]
                #print('time:',time)
                if compare_time(minn_time, time) : minn_time = time
                if compare_time(time, maxx_time) : maxx_time = time
            if '认定' in sen : break
        #print(minn_time, ' : ', maxx_time)
        if maxx_time == minn_time : return [maxx_time]
        else :return [minn_time, maxx_time]

    def extract_saje(self,content, id):
        """
        KE里，然后处理一下
        :param content:
        :param id:
        :return:
        """
        def transmit(money):
            """
            将'78.9万元 或者 798900.5元 处理成保留两位小数单位为万元的浮点数'
            :param money:
            :return:
            """
            sum = 0.0; Flag = False; t = 0.1;
            for s in money:
                if s == '.':  Flag = True
                elif s == '万': sum *= 10000.0
                elif s.isdigit():
                    if Flag == False:    sum = sum * 10.0 + float(s)
                    else:  sum = sum + t * float(s); t *= 0.1
            sum = float(int(sum / 100.0)) / 100.0
            return sum

        rexs = ["(共计|共)([^\d]*)?([\d][^元]*元)",
                "(转账|取|款|现金|收|贿|挪|回扣)([^\d]*)([\d][^元]*元)"]
        ans = ''
        Find = False
        for sen in self.split_content(content, split='。'):
            for res in rexs:
                pattren = re.compile(res)
                target = pattren.search(sen)
                if target != None:
                    ssen = target.group(3)
                    Find = True ; index = 0
                    for i in range(len(ssen)-3,0 ,-1):
                        if ssen[i].isdigit() or ssen[i] == '.' : pass
                        else : index = i+1; break
                    ans = ssen[index:]
                    break
            if Find: break
        return transmit(ans)

if __name__ == '__main__':
    ee = EntityExtraction()
    ee.test_total()

    # cont = '五指山市人民法院'
    # print('ok???')
    # ee.extract_sadq(cont,1)
    #ee.test_task2(ee.extract_sasj, 'extract_saje')
    #ee.test_task2(ee.extract_sadq,'extract_sadq')

    # ee.test_method()
