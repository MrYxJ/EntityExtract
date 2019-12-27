# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:01:23 2019

@author: bnuzgn
"""
import re
import json
import xlrd
import cpca 


def extract_xb(content):
    retList = ''
    genderTag = ['男','女']
    contentSegs = re.split('[,.、，。！!]',content)
    for contentSeg in contentSegs:
        for tag in genderTag:
            if tag in contentSeg:
                retList += contentSeg
                return retList
    return retList

def extract_csrq(content):
    retList = ''
    birthTag = ['出生','生于','日出','日生','出生于','出生地']
    contentSegs = re.split('[,.，、。！!]',content)
    for contentSeg in contentSegs:
        for tag in birthTag:
            if tag in contentSeg:
                timePattern = re.compile(r'(\d+年\d+月\d+日)')
                retList += "".join(timePattern.findall(contentSeg))
                return retList
    return retList

def extract_age(csrqList, pjrqList):
    age = ''
    yearPattern = re.compile(r'(\d+)年')  #匹配段落中的年份信息
    for i in range(len(csrqList)):
        if len(csrqList)>0 and len(pjrqList)>0:  #当前数据条目中的判决日期和出生日期同时非空时进行计算，否则输出为空
            if csrqList[i]!='' and pjrqList[i]!='':
                csrqYear = int(yearPattern.findall(csrqList[i])[0])
                pjrqYear = int(yearPattern.findall(pjrqList[i])[0])
                age = str(pjrqYear-csrqYear)   #判决日期的年份减去出生日期的年份 
            else:
                return age
        else:
            return age
    return age

def extract_zzmm(content):
    retStr = ''
#    zzmmTag = ['中国共产党党员','中国共产党预备党员','中国共产主义青年团团员',
#                '中国国民党革命委员会会员','中国民主同盟盟员','中国民主建国会会员',
#                '中国民主促进会会员','中国农工民主党党员','中国致公党党员',
#                '九三学社社员','台湾民主自治同盟盟员','无党派民主人士','群众']
    otherTag = ['中国国民党革命委员会会员','中国民主同盟盟员','中国民主建国会会员',
                '中国民主促进会会员','中国农工民主党党员','中国致公党党员',
                '九三学社社员','台湾民主自治同盟盟员','无党派民主人士','群众']
    contentSegs = re.split('[,.、，。！!]',content)
    for contentSeg in contentSegs:
        #仅仅是'党员'的情况
        if contentSeg=='党员':
            retStr += '中国共产党党员'
            return retStr
        #其他政体
        for tag in otherTag:
            if tag in contentSeg:
                retStr += contentSeg
                return retStr
        #共青团员
        if '团员' in contentSeg and '共青团' in contentSeg:
            retStr += '中国共产主义青年团团员'
            return retStr
        if '党员' in contentSeg and '共产党' in contentSeg:
            if '预备' in contentSeg:
                retStr += '中国共产党预备党员'
            else:
                retStr += '中国共产党党员'
            return retStr
    return retStr

def extract_rddb(content):
    retStr = ''
    #先判断是否属于人大代表，再判断层级；否则认为不是人大代表，值为‘无’
    contentSegs = re.split('[,.，、。！!]',content)
    for contentSeg in contentSegs:
        if '人大代表' in contentSeg:
            if '全国' in contentSeg:
                retStr = '全国'
                return retStr
            elif '省' in contentSeg:
                retStr = '省级'
                return retStr
            elif '市' in contentSeg:
                retStr = '地市'
                return retStr
            elif '县' in contentSeg:
                retStr = '县级'
                return retStr
            elif '乡' in contentSeg or '镇' in contentSeg:
                retStr = '乡镇'
                return retStr
    return retStr

def extract_zxwy(content):
    retStr = ''
    #先判断是否属于政协委员，再判断层级；否则认为不是人大代表，值为‘无’
    contentSegs = re.split('[,.，、。！!]',content)
    for contentSeg in contentSegs:
        if '政协委员' in contentSeg:
            if '全国' in contentSeg:
                retStr = '全国'
                return retStr
            elif '省' in contentSeg:
                retStr = '省级'
                return retStr
            elif '市' in contentSeg:
                retStr = '地市'
                return retStr
            elif '县' in contentSeg:
                retStr = '县级'
                return retStr
    return retStr

def extract_cardtype(content):
    #匹配证件类型为‘身份证’，匹配值为‘1’
    retList = ''
    cardtypeTag = ['身份证']
    contentSegs = re.split('[,.，、。！!]',content)
    for contentSeg in contentSegs:
        for tag in cardtypeTag:
            if tag in contentSeg:
                retList += '1'
                return retList
    return retList

def extract_cardid(content):
    retList = ''
    cardtypeTag = ['身份证']
    contentSegs = re.split('[,.，、。！!]',content)
    cardPattern = re.compile(r'([1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|([1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$)')
    for contentSeg in contentSegs:
        for tag in cardtypeTag:
            if tag in contentSeg:
                cardNumber = cardPattern.findall(contentSeg)
                if len(cardNumber)>0:
                    retList += cardNumber[0][0]
                    return retList
    return retList

def extract_whcd(content):
    retList = ''
    whcdTag = ['小学','初中','高中','中专','大专','本科','硕士','博士']
    contentSegs = re.split('[,.，、。！!]',content)
    for contentSeg in contentSegs:
        for tag in whcdTag:
            if tag in contentSeg:
                retList += contentSeg
                return retList
    return retList

def extract_rysf(content):
    retList = ''
    rysfTag = ['权利机关工作人员','行政机关工作人员','公安机关工作人员',
               '检察机关工作人员','审判机关工作人员','司法行政机关工作人员',
               '政协机关工作人员','共产党机关工作人员','国有公司企业工作人员',
               '国有事业单位工作人员','人民团体从事公务员','其他依法从事公务的人员',
               '其他人员']
    contentSegs = re.split('[,.、，。！!]',content)
    for contentSeg in contentSegs:
        for tag in rysfTag:
            if tag in contentSeg:
                retList += contentSeg
                return retList
    return retList

def extract_ssdw(contentSeg,tag):
    ssdw = ''
    content = contentSeg.split(tag)[0]
    if len(content)<5:
        return ssdw
    if content[:3]=='捕前系' or content[:3]=='捕前任':
        ssdw = content[3:]
    elif content[:2]=='原系' or content[:2]=='原任' or content[:2]=='曾任':
        ssdw = content[2:]
    elif  content[0]=='系' or content[0]=='原' or content[0]=='任':
        ssdw = content[1:]
    return ssdw

def extract_zw(content):      
    retList = []
     #数据表中没有给出职务的数据项，以下职务为自行总结
    zwTag = ['副主任','主任','副局长','局长','副科长','科长','副书记','书记','总工程师','工程师','总经理','副总经理','经理',
             '副厂长','厂长','调研员','副校长','校长','总负责人','负责人','安全员','会计','出纳','副组长','组长',
             '农民','副站长','站长','副所长','副镇长','副组长',
             '所长','镇长','临时工','副组长','组长','普查员','教师','老师','副教授','副部长','副董事'
             '教授','教研员','文书','部长','协管员','董事','指导员','助理','专员','副社长','副队长',
             '社长','公证员','翻译','队长','职工','职员','员工','裁判员','副主席','主席','副市长',
             '秘书','市长','副处长','处长','乡长','工作人员','干部','指挥长',
             '关长','监理','理事','副庭长','庭长','业务员','司长','副总监','总监','总厨',
             '厨师','副省长','省长','政委','院长','收款员','段长',
             '设计员','民警','聘用人员','承包','行长','副总裁','总裁','维护人员','丈量人员',
             '区长','股东','批发人员','副园长','园长','副厂长','场长','采购员','主管','矿长',
             '报账员','村长','技术员','操作员','监狱长','材料员','干警','班长',
             '执行官','队员','股长','办事员','医生','控制人','辅导员',
             '专干','经商','党组成员','科员','保管员','施工','协警',
             '公务员','经营人','调度员','巡视员']
    contentSegs = re.split('[,.，、。！!]',content)
    for contentSeg in contentSegs:
        for tag in zwTag:
            if tag in contentSeg:
                retList.append(tag)
                sadw = extract_ssdw(contentSeg,tag)
                retList.append(sadw)
                return retList
    return ['','']

def extract_zj(content):
    retList = ''
    zjTag = ['总理','副总理','正部级','副部级','正厅级','副厅级','正处级','副处级',
             '正科级','副科级','科员级','办事员','未定级的干部']
    contentSegs = re.split('[,.，、。！!]',content)
    for contentSeg in contentSegs:
        for tag in zjTag:
            if tag in contentSeg:
                retList += contentSeg
                return retList
    return retList

def extract_szdq(content):   
    #所在地区的判断调用了cpca，保存结果的省、市、区；结果中无法判断省、市、区的为空；有多种匹配结果的，可能出现warning
    retList = []
    contentList = [content]
    szdq = cpca.transform(contentList)
    if content == szdq['地址'].tolist()[0] or (len(content) > len(szdq['省'].tolist()[0]) and szdq['市'].tolist()[0] == ''):
        szdq = cpca.transform(contentList, cut=False)
    retList += szdq['省'].tolist()
    retList += szdq['市'].tolist()
    retList += szdq['区'].tolist()
    return retList
    


def extract_xzz(content):
    retList = ''
    xzzTag = ['家住','住址','住所','住在','住']
    contentSegs = re.split('[,.，、。！!]',content)
    for contentSeg in contentSegs:
        for tag in xzzTag:
            if tag in contentSeg:
                retList += contentSeg
                return retList
    return retList

def extract_saje(fyyj_content, tsgc_content, xmStr):
    """
    首先判断法院意见中能否抽取出涉案金额，若无，在庭审过程中抽取
    抽取涉案金额：
    首先获取所有被告人姓名，逐句判断这句话中是否有被告人，有则用正则把金额提取出来。
    由于共计是优先级最高判断，单独拿出来。
    """
    def transmit(money):
        """
         将'78.9万元 或者 798900.5元 处理成保留两位小数单位为万元的浮点数'
         201807
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

    ans = ''
    rexs = ["(共计|共)([^\d]*)?([\d][^元]*元)",
            "(转账|取|款|现金|收|贿|挪|回扣)([^\d]*)([\d][^元]*元)"]

    Find = False
    
    for sen in re.split('。', fyyj_content):
        if xmStr in sen:
#            print('1')
            for res in rexs:
                pattren = re.compile(res)
                target = pattren.search(sen)
                if target != None:
#                    print('2')
                    ssen = target.group(3)
                    Find = True;
                    index = 0
                    for i in range(len(ssen) - 3, 0, -1):
                        if ssen[i].isdigit() or ssen[i] == '.':
#                            print('3')
                            pass
                        else:
                            index = i + 1;
                            break
                    ans = str(transmit(ssen[index:]))
#                    print(content, '\n ans:', ans)
                    break
        if Find: break
        else:
            for sen in re.split('。', tsgc_content):
                if xmStr in sen:
#                    print('4')
                    for res in rexs:
                        pattren = re.compile(res)
                        target = pattren.search(sen)
                        if target != None:
#                            print('5')
                            ssen = target.group(3)
                            index = 0
                            for i in range(len(ssen) - 3, 0, -1):
                                if ssen[i].isdigit() or ssen[i] == '.':
#                                    print('6')
                                    pass
                                else:
                                    index = i + 1;
                                    break
                            ans = str(transmit(ssen[index:]))
                            break
    return ans

def extract_xsgx(content):
    retList = ''
    xsgxTag = ['上下级','情人','朋友','亲友','同事','介绍认识','钱权交易','其他']
    contentSegs = re.split('[,.，、。！!]',content)
    for contentSeg in contentSegs:
        for tag in xsgxTag:
            if tag in contentSeg:
                retList += tag
                return retList
    return retList

def extract_cysd(content):
    retList = ''
    cysdTag = ['送钱卡','送贵重物品','给予回扣','期权交易','干股分红','假赌送钱',
               '高卖低买','合作投资','色情贿赂']
    contentSegs = re.split('[,.，、。！!]',content)
    for contentSeg in contentSegs:
        for tag in cysdTag:
            if tag in contentSeg:
                retList += contentSeg
                return retList
    return retList

def extract_XM(content):
    XM_list = []
    contentSegs = re.split('[,.，、。！!]',content)
    XM_pattern = re.compile(r'^.*?(上诉人（原审被告人）|被告人)(.*?)$')
    XM_pattern2 = re.compile(r'^(.*?)（.*$')
    for contentSeg in contentSegs:
        if (contentSeg[:3]=='被告人' and contentSeg!='被告人' )or (contentSeg[:10]=='上诉人（原审被告人）'and contentSeg!='上诉人（原审被告人）'):
            newName = XM_pattern.findall(contentSeg)[0][1]
            if '（' in newName:
                newName = XM_pattern2.findall(newName)[0]
            if len(XM_list)!=0:
                flag = False
                for name in XM_list:
                    if name in newName  and newName != name:
                        flag = True
                if not flag:
                    XM_list.append(newName)
            else:
                XM_list.append(newName)
    return XM_list 

def extract_personType(content,XM):
    personType = ''
    contentSegs = re.split('[,.，、：。！!]',content)
    for contentSeg in contentSegs:
        if '被告人'+XM+'犯' in contentSeg:
            print(contentSeg)
            if '行贿' in contentSeg:
                return '行贿人'
            elif '受贿' in contentSeg:
                return '受贿人'
    return personType

def extract(x,lists):
    '''
    #定义模板
    #nrows是总的行数
    #lists内容为[{行1信息},{行2信息}....]
    #retDic返回结果，内容为
    {'2':{
        ‘personinfo':[{'XM','XB'},{'XM',''}]
	   },
     '3':...
    }
    '''
    retDic = {}
    for i in range(x):
        retDic[str(i+2)] = {}
        caseDic = {'personinfo':[]}
        '''1.抽取姓名'''
        XM_list = extract_XM(lists[i].get('当事人'))
        '''剩下的抽取'''
        dsrText = lists[i].get('当事人')
        if len(XM_list)>1:
            dsrTextList = []
            for j in range(len(XM_list)):       
                '''
                #按照姓名截取每人的当事人信息片段
                '''
                if j==0:
                    continue
                else:   
                    now = dsrText.split(XM_list[j],1)[0]
                    dsrText = dsrText.split(XM_list[j],1)[1]
                    dsrTextList.append(now)
            dsrTextList.append(dsrText)
#            print(XM_list)
#            print(dsrTextList)
            '''
            #剩余操作
            '''
            for j in range(len(XM_list)):
                XM = XM_list[j]
                personDic = {}
                '''1.抽取姓名'''
                personDic["XM"] = XM
                
                '''2.抽取性别'''
                xb_str = extract_xb(dsrTextList[j])
                personDic["XB"] = xb_str
                
                '''3.抽取出生日期'''
                csrq_str = extract_csrq(dsrTextList[j])
                personDic["CSRQ"] = csrq_str
                
                '''4.抽取年龄'''
                age_str = extract_age([csrq_str],[lists[i].get('判决日期')])
                personDic["AGE"] = age_str
                
                '''5.抽取政治面貌'''
                zzmm_str = extract_zzmm(dsrTextList[j])
                personDic["ZZMM"] = zzmm_str
                
                '''6.抽取人大代表'''
                rddb_str = extract_rddb(dsrTextList[j])
                personDic["RDDB"] = rddb_str
        
                '''7.抽取政协委员'''
                zxwy_str = extract_zxwy(dsrTextList[j])
                personDic["ZXWY"] = zxwy_str
        
                '''8.抽取人员身份'''
                rysf_str = extract_rysf(dsrTextList[j])
                personDic["RYSF"] = rysf_str
                
                '''9.抽取职务与所属单位'''
                zw_list = extract_zw(dsrTextList[j])
                personDic["ZW"] = zw_list[0]
                personDic["SSDW"] = zw_list[1]
                
                '''10.抽取职级'''
                zj_str = extract_zj(dsrTextList[j])
                personDic["ZJ"] = zj_str
               
                '''11.抽取证件类型'''
                cardtype_str = extract_cardtype(dsrTextList[j])
                personDic["CARDTYPE"] = cardtype_str
                
                '''12.抽取证件号码'''
                cardid_str = extract_cardid(dsrTextList[j])
                personDic["CARDID"] = cardid_str
                
                '''13.抽取文化程度'''
                whcd_str = extract_whcd(dsrTextList[j])
                personDic["WHCD"] = whcd_str
                
                '''14.抽取所在地区'''
                szdq_list = extract_szdq(lists[i].get('法院'))
                personDic["SZDQ"] = szdq_list
                 
                '''16.抽取现住址'''
                xzz_str = extract_xzz(dsrTextList[j])
                personDic["XZZ"] = xzz_str
                
                '''17.抽取涉案金额'''
                saje_str = extract_saje(lists[i].get('法院意见'), lists[i].get('庭审过程'), XM_list[j])
                personDic["SAJE"] = saje_str
                
                '''18.抽取行受关系'''
                xsgx_str = extract_xsgx(lists[i].get('庭审过程'))
                personDic["XSGX"] = xsgx_str
                
                '''19.抽取参与手段'''
                cysd_str = extract_cysd(lists[i].get('庭审过程'))
                personDic["CYSD"] = cysd_str
                
                '''20.抽取被告人类型'''
                personType_str = extract_personType(lists[i].get('判决结果'),XM)
                personDic["PERSONTYPE"] = personType_str
                '''
                #剩余操作
                '''
                caseDic['personinfo'].append(personDic)

        elif len(XM_list)==0:
            personDic = {}
            personDic["XM"] = ''
            personDic["XB"] = ''
            personDic["CSRQ"] =''
            personDic["AGE"] =''
            personDic["ZZMM"] =''
            personDic["RDDB"] =''
            personDic["ZXWY"] =''
            personDic["RYSF"] =''
            personDic["ZW"] =''
            personDic["ZJ"] =''
            personDic["CARDTYPE"] =''
            personDic["CARDID"] =''
            personDic["WHCD"] =''
            personDic["SZDQ"] =''
            personDic["SSDW"] =''
            personDic["XZZ"] =''
            personDic["SAJE"] =''
            personDic["XSGX"] =''
            personDic["CYSD"] =''
            '''保存'''
            caseDic['personinfo'].append(personDic)
        else:
            dsrTextStr = lists[i].get('当事人')
            personDic = {}
            
            '''1.抽取姓名'''      
            XM = XM_list[0]
            personDic["XM"] = XM
            
            '''2.抽取性别'''
            xb_str = extract_xb(dsrTextStr)
            personDic["XB"] = xb_str
            
            '''3.抽取出生日期'''
            csrq_str = extract_csrq(dsrTextStr)
            personDic["CSRQ"] = csrq_str
            
            '''4.抽取年龄'''
            age_str = extract_age([csrq_str],[lists[i].get('判决日期')])
            personDic["AGE"] = age_str
            
            '''5.抽取政治面貌'''
            zzmm_str = extract_zzmm(dsrTextStr)
            personDic["ZZMM"] = zzmm_str
            
            '''6.抽取人大代表'''
            rddb_str = extract_rddb(dsrTextStr)
            personDic["RDDB"] = rddb_str
    
            '''7.抽取政协委员'''
            zxwy_str = extract_zxwy(dsrTextStr)
            personDic["ZXWY"] = zxwy_str
    
            '''8.抽取人员身份'''
            rysf_str = extract_rysf(dsrTextStr)
            personDic["RYSF"] = rysf_str
            
            '''9.抽取职务与所属单位'''
            zw_list = extract_zw(dsrTextStr)
            personDic["ZW"] = zw_list[0]
            personDic["SSDW"] = zw_list[1]
            
            '''10.抽取职级'''
            zj_str = extract_zj(dsrTextStr)
            personDic["ZJ"] = zj_str
           
            '''11.抽取证件类型'''
            cardtype_str = extract_cardtype(dsrTextStr)
            personDic["CARDTYPE"] = cardtype_str
            
            '''12.抽取证件号码'''
            cardid_str = extract_cardid(dsrTextStr)
            personDic["CARDID"] = cardid_str
            
            '''13.抽取文化程度'''
            whcd_str = extract_whcd(dsrTextStr)
            personDic["WHCD"] = whcd_str
            
            '''14.抽取所在地区'''
            szdq_list = extract_szdq(lists[i].get('法院'))
            personDic["SZDQ"] = szdq_list
             
            '''16.抽取现住址'''
            xzz_str = extract_xzz(dsrTextStr)
            personDic["XZZ"] = xzz_str
            
            '''17.抽取涉案金额'''
            saje_str = extract_saje(lists[i].get('法院意见'), lists[i].get('庭审过程'),XM)
            personDic["SAJE"] = saje_str
            
            '''18.抽取行受关系'''
            xsgx_str = extract_xsgx(lists[i].get('庭审过程'))
            personDic["XSGX"] = xsgx_str
            
            '''19.抽取参与手段'''
            cysd_str = extract_cysd(lists[i].get('庭审过程'))
            personDic["CYSD"] = cysd_str
            '''20.抽取被告人类型'''
            personType_str = extract_personType(lists[i].get('判决结果'),XM)
            personDic["PERSONTYPE"] = personType_str
            '''保存'''
            caseDic['personinfo'].append(personDic)
        retDic[str(i+2)] = caseDic
    return retDic

if __name__=='__main__':
    '''
    excelPath保存读取路径
    saveDict保存所有经过处理的字典信息
    '''
#    excelPath=r'C:\Users\acer\Desktop\OpenLaw判决书.xlsx'
    excelPath=r'D:\桌面文件\OpenLaw判决书.xlsx'
    savePath = r'C:\Users\44128\Desktop\retJson.json'
#    saveDict=dict()
#    with open(jsonPath,'r',encoding='utf-8') as f:
#        jsonDic=json.load(f)
    
    workfile = xlrd.open_workbook(excelPath) #打开excel
    table = workfile.sheets()[0] #打开第一个sheet
    nrows = table.nrows #获取行数
    ncols = table.ncols #获取列数
    
    lists = []     #保存从excel表中读取出来的值，每一行为一个list
    
    x= nrows
#    x = 100
    for i in range(x):
        '''具体操作'''
        if i==0:
            pass
        else:
            dic = {}
            list=table.row_values(i)
            '''存储信息'''
            dic["标题"]=list[0]    #存储标题
            dic["案号"]=list[1]    #存储案号
            dic["案件类型"]=list[2]
            dic["庭审程序"]=list[3]
            dic["案由"]=list[4]
            dic["文书类型"]=list[5]
            dic["法院"]=list[6]
            dic["判决日期"]=list[7]
            dic["原告"]=list[8]
            dic["被告"]=list[9]
            dic["第三人"]=list[10]
            dic["法官"]=list[11]
            dic["审判长"]=list[12]
            dic["审判员"]=list[13]
            dic["书记"]=list[14]
            dic["头部"]=list[15]
            dic["头部2"]=list[16]
            dic["当事人"]=list[17]
            dic["当事人2"]=list[18]
            dic["庭审程序说明"]=list[19]
            dic["庭审程序说明2"]=list[20]
            dic["庭审过程"]=list[21]
            dic["庭审过程2"]=list[22]
            dic["庭审过程3"]=list[23]
            dic["庭审过程4"]=list[24]
            dic["庭审过程5"]=list[25]
            dic["庭审过程6"]=list[26]
            dic["法院意见"]=list[27]
            dic["法院意见2"]=list[28]
            dic["判决结果"]=list[29]
            dic["判决结果2"]=list[30]
            dic["庭后告知"]=list[31]
            dic["庭后告知2"]=list[32]
            dic["结尾"]=list[33]
             
            lists.append(dic)        #合并字典
    retDic = extract(x-1,lists)
    with open(savePath,"w",encoding='utf-8') as f:
        f.write(json.dumps(retDic,ensure_ascii=False, indent=3))
    
