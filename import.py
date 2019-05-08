#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
import json

def into_xh_caseinfo():
    with open("result.json",'r') as result:
        res = json.load(result)
        for item in res:
           # table xh_caseinfo
            uuid = item['UUID']

            ajxz = item['AJXZ']
            ajxzsql = "select CODE from pub_organization where CODE_TYPE_NO ='AJXZ' and CODE_NAME = "+ajxz
            cursor.execute(ajxzsql)
            ajxzcode = cursor.fetchone()

            ajlx = item['AJLX']
           # 单位
            unicode = item['UNICODE']

           # 单位省级代码
            top_unicode = item['TOP_UNICODE']

            hyly = item['HYLY']
            hylysql = ""

           # 涉案环节
            sahj = item['SAHJ']
            sahjsql = "select code from pub_code_item where CODE_TYPE_NO ='SAHJ' and CODE_NAME = "+sahj
            cursor.execute(sahjsql)
            sahjcode = cursor.fetchone()

           # 案发场所
            afcs = item['AFCS']
            afcssql = "select code from pub_code_item where CODE_TYPE_NO ='AFCS' and CODE_NAME = "+afcs
            cursor.execute(afcssql)
            afcscode = cursor.fetchone()

            lasj = item['LASJ']
            pjsj = item['PJSJ']
            tjyear = item['TJYEAR']
            tjmonth = item['TJMONTH']

           # 涉案地区
            sadq = item['SADQ']
            sadqsql = "select code from pub_code_item where CODE_TYPE_NO ='administrative_area' and CODE_NAME = "+sadq
            cursor.execute(sadqsql)
            sadqcode = cursor.fetchone()

            sasj = item['SASJ']
            saje = item['SAJE']
            zacs = item['ZACS']
            dcfz = item['DCFZ']
            sw = item['SW']
            createtime = item['CREATETIME']
            updatetime = item['UPDATETIME']
            sql = "insert into xh_caseinfo values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (uuid, ajxzcode, ajlx, unicode, top_unicode,
                    hyly, sahjcode,afcscode, lasj, pjsj,
                    tjyear, tjmonth, sadqcode, sasj, saje,
                    zacs, dcfz, sw, createtime, updatetime)
            cursor.execute(sql, data)



def into_xh_personinfo():
    with open("personinfo.json",'r') as result:
        res = json.load(result)
        for item in res:
                uuid = item['UUID']
                ajid = item['AJID']
                dwid = item['DWID']
                persontype = item['PERSONTYPE']
                xm = item['XM']

                # 性别
                xb = item['XB']
                xbsql = "select CODE from pub_code_item where CODE_TYPE_NO ='gender' and CODE_NAME = "+xb
                cursor.execute(xbsql)
                xbcode = cursor.fetchone()

                csrq = item['CSRQ']
                age = item['AGE']

                # 政治面貌
                zzmm = item['ZZMM']
                zzmmsql = "select CODE from pub_code_item where CODE_TYPE_NO ='zzmm' and CODE_NAME = "+zzmm
                cursor.execute(zzmmsql)
                zzmmcode = cursor.fetchone()

                rddb = item['RDDB']
                rddbsql = "select CODE from pub_code_item where CODE_TYPE_NO ='rddb' and CODE_NAME = "+rddb
                cursor.execute(rddbsql)
                rddbcode = cursor.fetchone()

                zxwy = item['ZXWY']
                zxwysql = "select CODE from pub_code_item where CODE_TYPE_NO ='zxwy' and CODE_NAME = "+zxwy
                cursor.execute(zxwysql)
                zxwycode = cursor.fetchone()

                rysf = item['RYSF']
                rysfsql = "select CODE from pub_code_item where CODE_TYPE_NO ='rysf' and CODE_NAME = "+rysf
                cursor.execute(rysfsql)
                rysfcode = cursor.fetchone()

                zw = item['ZW']

                zj = item['ZJ']
                zjsql = "select CODE from pub_code_item where CODE_TYPE_NO ='zj' and CODE_NAME = "+zj
                cursor.execute(zjsql)
                zjcode = cursor.fetchone()

                cardtype = item['CARDTYPE']

                cardid = item['CARDID']

                whcd = item['WHCD']
                whcdsql = "select CODE from pub_code_item where CODE_TYPE_NO ='whcd' and CODE_NAME = "+whcd
                cursor.execute(whcdsql)
                whcdcode = cursor.fetchone()

                szdq = item['SZDQ']
                szdqsql = "select CODE from pub_code_item where CODE_TYPE_NO ='administrative_area' and CODE_NAME = "+szdq
                cursor.execute(szdqsql)
                szdqcode = cursor.fetchone()

                ssdw = item['SSDW']

                xzz = item['XZZ']

                saje = item['SAJE']

                xsgx = item['XSGX']
                xsgxsql = "select CODE from pub_code_item where CODE_TYPE_NO ='administrative_area' and CODE_NAME = "+xsgx
                cursor.execute(xsgxsql)
                xsgxcode = cursor.fetchone()

                cysd = item['CYSD']
                cysdsql = "select CODE from pub_code_item where CODE_TYPE_NO ='xsgx' and CODE_NAME = "+cysd
                cursor.execute(cysdsql)
                cysdcode = cursor.fetchone()

                sql = "insert into xh_personinfo values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s)"
                data = (uuid,ajid,dwid,persontype,xm,xb,csrq,age,zzmm,rddb,zxwy,rysf,zw,zj,cardtype,cardid,whcd,szdq,ssdw,xzz,saje,xsgx,cysd)
                cursor.execute(sql, data)

def into_xh_unitinfo():
    with open("unitinfo.json",'r') as result:
        res = json.load(result)
        for item in res:
                uuid = item['UUID']
                ajid = item['AJID']
                dwmc = item['DWMC']
                tyshxydm = item['TYSHXYDM']
                frxm = item['FRXM']
                frsa = item['FRSA']
                unittype = item['UNITTYPE']
                bcfj = item['BCFJ']
                
                dwxz = item['DWXZ']
                dwxzsql = "select CODE from pub_code_item where CODE_TYPE_NO ='dwxz' and CODE_NAME = "+dwxz
                cursor.execute(dwxzsql)
                dwxzcode = cursor.fetchone()

                szdq = item['DWXZ']
                szdqsql = "select CODE from pub_code_item where CODE_TYPE_NO ='administrative_area' and CODE_NAME = "+szdq
                cursor.execute(szdqsql)
                szdqcode = cursor.fetchone()

                licenseno = item['LICENSENO']
                regadd = item['REGADD']
                workadd = item['WORKADD']

                sql = "insert into xh_personinfo values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                data = (uuid,ajid,dwmc,tyshxydm,frxm,frsa,unittype,bcfj,dwxz,szdq,licenseno,regadd,workadd)
                cursor.execute(sql, data)



if __name__ == '__main__':

    # connect database
    db = pymysql.connect(host="172.16.216.161", user="law", password="cistLAW1104", database="law", charset="utf8")
    # 创建游标
    cursor = db.cursor()
    into_xh_caseinfo()
    into_xh_personinfo()
    into_xh_unitinfo()

