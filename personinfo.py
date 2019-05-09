# -*- coding: utf-8 -*-
"""
Created on Tue May  7 16:04:17 2019

@author: acer
"""

#!/usr/bin/python3
# encoding: utf-8
# Author MrYx
# @Time: 2019/5/6 16:53

import json, re, xlrd , datetime
import cpca

class EntityExtraction():
    def __init__(self):
        '''
        这里analys_pos定义每个抽取任务从excel的哪个部分抽取
        '''
        self.input_file = r'D:\桌面文件\OpenLaw判决书.xlsx'
        self.all_items = self.xlsx_to_dict(self.input_file)
        self.analys_pos = {
            'extract_ajxz': ['案由'],   #可能从多个不同部分提取，所以用List
            'extract_xm':['被告'],
            'extract_xb':['当事人'],
            'extract_csrq':['当事人'],
            'extract_pjrq':['判决日期'],
#            'extract_age':['当事人','判决日期'],
            'extract_zzmm':['当事人'],
            'extract_rddb':['当事人'],
            'extract_zxwy':['当事人'],
            'extract_rysf':['当事人'],
            'extract_zw':['当事人'],
            'extract_zj':['当事人'],
            'extract_cardtype':['当事人'],
            'extract_cardid':['当事人'],
            'extract_whcd':['当事人'],
            'extract_szdq':['法院'],
            'extract_ssdw':['当事人'],
            'extract_xzz':['当事人'],
            'extract_saje':['庭审过程'],
            'extract_xsgx':['庭审过程'],
            'extract_cysd':['庭审过程'],
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
        with open(filename, "w",encoding = 'utf-8') as f:
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
            for pos in self.analys_pos[function_name]:
                ans = function(item[pos], index)
                if ans != [] :
                    anss.append(ans)
                    break
            if ans == []: anss.append([])
        return anss

    def test_total(self,  result_file):
        '''
        最后运行的程序
        :param test_file:
        :return:
        '''
        print('input: ', self.input_file)
        self.dict['AJXZ'] = self.test_task(self.extract_ajxz, 'extract_ajxz')
        self.dict['XM'] = self.test_task(self.extract_xm, 'extract_xm')
        self.dict['XB'] = self.test_task(self.extract_xb, 'extract_xb')
        self.dict['CSRQ'] = self.test_task(self.extract_csrq, 'extract_csrq')
        self.dict['PJRQ'] = self.test_task(self.extract_pjrq, 'extract_pjrq')
        self.dict['ZZMM'] = self.test_task(self.extract_zzmm, 'extract_zzmm')
        self.dict['RDDB'] = self.test_task(self.extract_rddb, 'extract_rddb')
        self.dict['ZXWY'] = self.test_task(self.extract_zxwy, 'extract_zxwy')
        self.dict['RYSF'] = self.test_task(self.extract_rysf, 'extract_rysf')
        self.dict['ZW'] = self.test_task(self.extract_zw, 'extract_zw')
        self.dict['ZJ'] = self.test_task(self.extract_zj, 'extract_zj')
        self.dict['CARDTYPE'] = self.test_task(self.extract_cardtype, 'extract_cardtype')
        self.dict['CARDID'] = self.test_task(self.extract_cardid, 'extract_cardid')
        self.dict['WHCD'] = self.test_task(self.extract_whcd, 'extract_whcd')
        self.dict['SZDQ'] = self.test_task(self.extract_szdq, 'extract_szdq')
        self.dict['SSDW'] = self.test_task(self.extract_ssdw, 'extract_ssdw')
        self.dict['XZZ'] = self.test_task(self.extract_xzz, 'extract_xzz')
        self.dict['SAJE'] = self.test_task(self.extract_saje, 'extract_saje')
        self.dict['XSGX'] = self.test_task(self.extract_xsgx, 'extract_xsgx')
        self.dict['CYSD'] = self.test_task(self.extract_cysd, 'extract_cysd')
        self.dict['AGE'] = self.extract_age(self.dict['CSRQ'],self.dict['PJRQ'])
        #...............

        ans = []
        dict_key_order = ['AJXZ','XM','XB','CSRQ','AGE','ZZMM','RDDB','ZXWY',
                          'RYSF','ZW','ZJ','CARDTYPE','CARDID','WHCD','SZDQ',
                          'SSDW','XZZ','SAJE','XSGX','CYSD']

        for i in range(len(self.all_items)):
            item = {}
            for key in dict_key_order:
                value = self.dict[key][i]
                if value != None: item[key] = value
            ans.append(item)
        self.write_dict_to_json(dicts=ans, filename=result_file)

    def extract_ajxz(self, content, id): # id为第几个item索引
        return [content]
    def extract_xm(self, content, id):
        return [content]
    def extract_xb(self, content, id):
        retList = []
        genderTag = ['男','女']
        contentSegs = re.split('[,.，。！!]',content)
        for contentSeg in contentSegs:
            for tag in genderTag:
                if tag in contentSeg:
                    retList += [contentSeg]
                    return retList
        return retList
    def extract_pjrq(self, content, id): # 抽取判决日期，以便计算年龄
        return [content]
    def extract_csrq(self, content, id):
        retList = []
        birthTag = ['出生','生于','日出','日生','出生于','出生地']
        contentSegs = re.split('[,.，。！!]',content)
        for contentSeg in contentSegs:
            for tag in birthTag:
                if tag in contentSeg:
                    timePattern = re.compile(r'(\d+年\d+月\d+日)')
                    retList += timePattern.findall(contentSeg)
                    return retList
        return retList 
    def extract_age(self, csrqList,pjrqList):  #年龄计算为判决日期的年份减去出生日期的年份
        age = []
        yearPattern = re.compile(r'(\d+)年')  #匹配段落中的年份信息
        for i in range(len(csrqList)):
            if len(csrqList[i])>0 and len(pjrqList[i])>0:  #当前数据条目中的判决日期和出生日期同时非空时进行计算，否则输出为空
                if csrqList[i][0]!='' and pjrqList[i][0]!='':
                    csrqYear = int(yearPattern.findall(csrqList[i][0])[0])
                    pjrqYear = int(yearPattern.findall(pjrqList[i][0])[0])
                    age.append([str(pjrqYear-csrqYear)])  #判决日期的年份减去出生日期的年份
                else:
                    age.append([])
            else:
                age.append([])
        return age                
    def extract_zzmm(self, content, id):
        retList = []
        zzmmTag = ['中国共产党党员','中国共产党预备党员','中国共产主义青年团团员',
                    '中国国民党革命委员会会员','中国民主同盟盟员','中国民主建国会会员',
                    '中国民主促进会会员','中国农工民主党党员','中国致公党党员',
                    '九三学社社员','台湾民主自治同盟盟员','无党派民主人士','群众']
        contentSegs = re.split('[,.，。！!]',content)
        for contentSeg in contentSegs:
            for tag in zzmmTag:
                if tag in contentSeg:
                    retList += [contentSeg]
                    return retList
        return retList
    def extract_rddb(self, content, id):
        retList = []
        rddbKey = ['人大代表']   #先判断是否属于人大代表，再判断层级；否则认为不是人大代表，值为‘无’
        rddbTag = ['全国','省级','地市','县级','乡镇']
        retTag = ['无']
        contentSegs = re.split('[,.，。！!]',content)
        for contentSeg in contentSegs:
            for tag in rddbKey:
                for tag in rddbTag:
                    if tag in contentSeg:
                        retList += [contentSeg]
                        return retList
        return retTag
    def extract_zxwy(self, content, id):
        retList = []
        zxwyKey = ['政协委员']   #先判断是否属于政协委员，再判断层级；否则认为不是人大代表，值为‘无’
        zxwyTag = ['全国','省级','地市','县级']
        retTag = ['无']
        contentSegs = re.split('[,.，。！!]',content)
        for contentSeg in contentSegs:
            for tag in zxwyKey:
                for tag in zxwyTag:
                    if tag in contentSeg:
                        retList += [contentSeg]
                        return retList
        return retTag
    def extract_rysf(self, content, id):
        retList = []
        rysfTag = ['权利机关工作人员','行政机关工作人员','公安机关工作人员',
                   '检察机关工作人员','审判机关工作人员','司法行政机关工作人员',
                   '政协机关工作人员','共产党机关工作人员','国有公司企业工作人员',
                   '国有事业单位工作人员','人民团体从事公务员','其他依法从事公务的人员',
                   '其他人员']
        contentSegs = re.split('[,.，。！!]',content)
        for contentSeg in contentSegs:
            for tag in rysfTag:
                if tag in contentSeg:
                    retList += [contentSeg]
                    return retList
        return retList
    def extract_zw(self, content, id):      
        retList = []
         #数据表中没有给出职务的数据项，以下职务为自行总结
        zwTag = ['主任','局长','科长','书记','工程师','经理','代表人','厂长','委员',
                 '调研员','校长','负责人','安全员','会计','出纳','组长','农民','站长',
                 '所长','镇长','临时工','组长','代表','个体','普查员','教师','老师',
                 '教授','教研员','文书','部长','协管员','董事','指导员','助理','专员',
                 '社长','公证员','翻译','队长','职工','职员','员工','裁判员','主席',
                 '秘书','市长','无业','管理','处长','乡长','工作人员','干部','指挥长',
                 '关长','监理','理事','常委','庭长','业务员','司长','总监','总厨',
                 '厨师','省长','政委','院长','收款员','段长','业主','无固定职业',
                 '设计员','民警','聘用人员','承包','行长','总裁','维护人员','丈量人员',
                 '区长','股东','批发人员','园长','场长','采购员','主管','矿长','村民',
                 '报账员','村长','技术员','操作员','监狱长','材料员','干警','班长',
                 '执行官','队员','股长','无职业','办事员','医生','控制人','辅导员',
                 '出资人','专干','经商','党组成员','科员','保管员','施工','协警',
                 '公务员','网长','承建','经营人','调度员','巡视员']
        contentSegs = re.split('[,.，。！!]',content)
        for contentSeg in contentSegs:
            for tag in zwTag:
                if tag in contentSeg:
                    retList += [contentSeg]
                    return retList
        return retList
    def extract_zj(self, content, id):
        retList = []
        zjTag = ['总理','副总理','正部级','副部级','正厅级','副厅级','正处级','副处级',
                 '正科级','副科级','科员级','办事员','未定级的干部']
        contentSegs = re.split('[,.，。！!]',content)
        for contentSeg in contentSegs:
            for tag in zjTag:
                if tag in contentSeg:
                    retList += [contentSeg]
                    return retList
        return retList
    def extract_cardtype(self, content, id):
        #匹配证件类型为‘身份证’，匹配值为‘1’
        retList = []
        cardtypeTag = ['身份证']
        contentSegs = re.split('[,.，。！!]',content)
        for contentSeg in contentSegs:
            for tag in cardtypeTag:
                if tag in contentSeg:
                    retList += ['1']
                    return retList
        return retList
    def extract_cardid(self, content, id):
        retList = []
        cardtypeTag = ['身份证']
        contentSegs = re.split('[,.，。！!]',content)
        cardPattern = re.compile(r'([1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|([1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$)')
        for contentSeg in contentSegs:
            for tag in cardtypeTag:
                if tag in contentSeg:
                    cardNumber = cardPattern.findall(contentSeg)
                    if len(cardNumber)>0:
                        retList += [cardNumber[0][0]]
                        return retList
        return retList
    def extract_whcd(self, content, id):
        retList = []
        whcdTag = ['小学','初中','高中','中专','大专','本科','硕士','博士']
        contentSegs = re.split('[,.，。！!]',content)
        for contentSeg in contentSegs:
            for tag in whcdTag:
                if tag in contentSeg:
                    retList += [contentSeg]
                    return retList
        return retList
    def extract_szdq(self, content, id):   
        #所在地区的判断调用了cpca，保存结果的省、市、区；结果中无法判断省、市、区的为空；有多种匹配结果的，可能出现warning
        retList = []
        contentList = [content]
        szdq = cpca.transform(contentList)
        retList += szdq['省'].tolist()
        retList += szdq['市'].tolist()
        retList += szdq['区'].tolist()
        return retList
    def extract_ssdw(self, content, id):
        retList = []
        ssdwTag = ['单位']
        contentSegs = re.split('[,.，。！!]',content)
        for contentSeg in contentSegs:
            for tag in ssdwTag:
                if tag in contentSeg:
                    retList += [contentSeg]
                    return retList
        return retList
    def extract_xzz(self, content, id):
        retList = []
        xzzTag = ['家住','住址','住所','住在','住']
        contentSegs = re.split('[,.，。！!]',content)
        for contentSeg in contentSegs:
            for tag in xzzTag:
                if tag in contentSeg:
                    retList += [contentSeg]
                    return retList
        return retList
    def extract_saje(self, content, id):
        retList = []
        moneyTag = ['人民币','美元','美金','港币','澳门币','新台币','欧元','日元',
                '日币','泰铢','瑞士法郎','韩币','韩元','越南盾','爱尔兰镑','加元',
                '新加坡元','新加坡币','金条','澳元']
        contentSegs = re.split('[,.，。！!]',content)
        for contentSeg in contentSegs:
            for tag in moneyTag:
                if tag in contentSeg:
                    rePattern1 = re.compile(r'(\d+千*万*元*)'+tag)
                    rePattern2 = re.compile(tag+r'(\d+千*万*元*)')
                    retList += [i+tag for i in rePattern1.findall(contentSeg)]+[i+tag for i in rePattern2.findall(contentSeg)]
        return retList
    def extract_xsgx(self, content, id):
        retList = []
        xsgxTag = ['上下级','情人','朋友','亲友','同事','介绍认识','钱权交易','其他']
        contentSegs = re.split('[,.，。！!]',content)
        for contentSeg in contentSegs:
            for tag in xsgxTag:
                if tag in contentSeg:
                    retList += [contentSeg]
                    return retList
        return retList
    def extract_cysd(self, content, id):
        retList = []
        cysdTag = ['送钱卡','送贵重物品','给予回扣','期权交易','干股分红','假赌送钱',
                   '高卖低买','合作投资','色情贿赂']
        contentSegs = re.split('[,.，。！!]',content)
        for contentSeg in contentSegs:
            for tag in cysdTag:
                if tag in contentSeg:
                    retList += [contentSeg]
                    return retList
        return retList
if __name__ == '__main__':
    ee = EntityExtraction()
#    print(ee.test_task(ee.extract_szdq,'extract_szdq')[0])
#    print(ee.all_items[0]['案由'])
    ee.test_total('result.json')
