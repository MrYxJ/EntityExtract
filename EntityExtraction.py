#!/usr/bin/python3
# encoding: utf-8
# Author MrYx
# @Time: 2019/5/6 16:53

import json, re, xlrd , datetime, sys

class EntityExtraction():
    def __init__(self):
        '''
        这里analys_pos定义每个抽取任务从excel的哪个部分抽取
        '''
        self.input_file = 'OpenLaw判决书.xlsx'
        self.all_items = self.xlsx_to_dict(self.input_file)
        self.analys_pos = {
            'extract_ajxz': ['案由'],   #可能从多个不同部分提取，所以用List
            'extract_ajlx': ['当事人', '判决结果', '庭审过程'],
            'extract_unitcode_and_top': ['法院'],
            'extract_hyly':['案由', '庭审过程'],
            'extract_sahj':['庭审过程'],
            'extract_afcs':['庭审过程'],
            'extract_lasj':['庭审过程']
        }
        self.dict = {}

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
            # for pos in self.analys_pos[function_name]:
            #     ans = function(item[pos], index)
            #     if ans != [] :
            #         anss.append(ans)
            #         break
            # if ans == []: anss.append([])
            contents = []
            for pos in self.analys_pos[function_name]:
                contents.append(item[pos])
            ans = function(contents, index)
            if ans == 0:
                print(str(index) + "\n" + str(item))
                break
            anss.append(ans)
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
            anss_1.append(ans_1)
            anss_2.append(ans_2)
        return anss_1, anss_2

    def test_total(self,  result_file):
        '''
        最后运行的程序
        :param test_file:
        :return:
        '''
        print('input: ', self.input_file)
        # self.dict['AJXZ'] = self.test_task(self.extract_ajxz, 'extract_ajxz')
        # self.dict['AJLX'] = self.test_task(self.extract_ajlx, 'extract_ajlx')
        # self.dict['TOP_UNITCODE'], self.dict['UNITCODE'] = self.test_task_duo(self.extract_unitcode_and_top, 'extract_unitcode_and_top')
        # self.dict['HYLY'] = self.test_task(self.extract_hyly, 'extract_hyly')
        self.dict['LASJ'] = self.test_task(self.extract_lasj, 'extract_lasj')

        #...............

        ans = []
        dict_key_order = ['LASJ']

        for i in range(len(self.all_items)):
            item = {}
            for key in dict_key_order:
                value = self.dict[key][i]
                if value != None: item[key] = value
            ans.append(item)
        self.write_dict_to_json(dicts=ans, filename=result_file)

    def extract_ajxz(self, content, id): # id为第几个item索引
        return [content]

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
        return content[0]

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




if __name__ == '__main__':
    ee = EntityExtraction()
    # ee.load_china_regions()
    print(ee.all_items[0]['案由'])
    ee.test_total('unitcode.json')
    # ee.test_method()
