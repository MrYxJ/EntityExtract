#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
import json

def into_xh_caseinfo():
    with open("result.json",'r') as result:
        res = json.load(result)
        for item in res:
           #table xh_caseinfo
           #判断结果里是否有UUID属性

            uuid = item['UUID'][0]

            ajxz = item['AJXZ'][0]
            ajxzsql = "select CODE from pub_code_item  where CODE_TYPE_NO ='AJXZ' and CODE_NAME = '"+ajxz+"'"
            try:
                cursor.execute(ajxzsql)
                ajxzcode = cursor.fetchone()[0]
            except:
                ajxzcode = ""

            ajlx = item['AJLX'][0]
           # 单位
            unicode = item['UNICODE'][0]

           # 单位省级代码
            top_unicode = item['TOP_UNICODE'][0]

            hyly = item['HYLY'][0]
            hylysql = ""

           # 涉案环节
            sahj = item['SAHJ'][0]
            sahjsql = "select code from pub_code_item where CODE_TYPE_NO ='SAHJ' and CODE_NAME = '"+sahj+"'"
            try:
                cursor.execute(sahjsql)
                sahjcode = cursor.fetchone()[0]
            except:
                sahjcode = ""

           # 案发场所
            afcs = item['AFCS'][0]
            afcssql = "select code from pub_code_item where CODE_TYPE_NO ='AFCS' and CODE_NAME = '"+afcs+"'"
            try:
                cursor.execute(afcssql)
                afcscode = cursor.fetchone()[0]
            except:
                afcscode=""

            lasj = item['LASJ'][0]
            pjsj = item['PJSJ'][0]


           # 涉案地区
            sadq = item['SADQ'][0]
            sadqsql = "select code from pub_code_item where CODE_TYPE_NO ='administrative_area' and CODE_NAME = '"+sadq+"'"
            try:
                cursor.execute(sadqsql)
                sadqcode = cursor.fetchone()[0]
            except:
                sadqcode = ""

            sasj = item['SASJ'][0]
            saje = item['SAJE'][0]
            zacs = item['ZACS'][0]
            dcfz = item['DCFZ'][0]
            sw = item['SW'][0]
            aqzy = item['AQZY'][0]
            createtime = item['CREATETIME'][0]
            updatetime = item['UPDATETIME'][0]
            sql = "insert into xh_caseinfo values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (uuid, ajxzcode, ajlx, unicode, top_unicode,
                    hyly, sahjcode,afcscode, lasj, pjsj,
                    sadqcode, sasj, saje, zacs, dcfz,
                    sw, aqzy, createtime, updatetime)
            cursor.execute(sql, data)
            db.commit()



def into_xh_personinfo():
    with open("result.json",'r') as result:
        res = json.load(result)
        for item in res:
                uuid = item['UUID'][0]
                ajid = item['AJID'][0]
                dwid = item['DWID'][0]
                persontype = item['PERSONTYPE'][0]
                xm = item['XM'][0]

                # 性别
                xb = item['XB'][0]
                xbsql = "select CODE from pub_code_item where CODE_TYPE_NO ='gender' and CODE_NAME = '"+xb+"'"
                cursor.execute(xbsql)
                xbcode = cursor.fetchone()[0]

                csrq = item['CSRQ'][0]
                age = item['AGE'][0]

                # 政治面貌
                zzmm = item['ZZMM'][0]
                zzmmsql = "select CODE from pub_code_item where CODE_TYPE_NO ='zzmm' and CODE_NAME = '"+zzmm+"'"
                try:
                    cursor.execute(zzmmsql)
                    zzmmcode = cursor.fetchone()[0]
                except:
                    zzmmcode = ""

                rddb = item['RDDB'][0]
                rddbsql = "select CODE from pub_code_item where CODE_TYPE_NO ='rddb' and CODE_NAME = '"+rddb+"'"
                try:
                    cursor.execute(rddbsql)
                    rddbcode = cursor.fetchone()
                except:
                    rddbcode = ""

                zxwy = item['ZXWY'][0]
                zxwysql = "select CODE from pub_code_item where CODE_TYPE_NO ='zxwy' and CODE_NAME = '"+zxwy+"'"
                try:
                    cursor.execute(zxwysql)
                    zxwycode = cursor.fetchone()[0]
                except:
                    zxwycode = ""

                rysf = item['RYSF'][0]
                rysfsql = "select CODE from pub_code_item where CODE_TYPE_NO ='rysf' and CODE_NAME = '"+rysf+"'"
                try:
                    cursor.execute(rysfsql)
                    rysfcode = cursor.fetchone()[0]
                except:
                    rysfcode = ""

                zw = item['ZW'][0]

                zj = item['ZJ'][0]
                zjsql = "select CODE from pub_code_item where CODE_TYPE_NO ='zj' and CODE_NAME = '"+zj+"'"
                try:
                    cursor.execute(zjsql)
                    zjcode = cursor.fetchone()[0]
                except:
                    zjcode = ""

                cardtype = item['CARDTYPE'][0]

                cardid = item['CARDID'][0]

                whcd = item['WHCD'][0]
                whcdsql = "select CODE from pub_code_item where CODE_TYPE_NO ='whcd' and CODE_NAME = '"+whcd+"'"
                try:
                    cursor.execute(whcdsql)
                    whcdcode = cursor.fetchone()[0]
                except:
                    whcdcode = ""

                szdq = item['SZDQ'][0]
                szdqsql = "select CODE from pub_code_item where CODE_TYPE_NO ='administrative_area' and CODE_NAME = '"+szdq+"'"
                try:
                    cursor.execute(szdqsql)
                    szdqcode = cursor.fetchone()[0]
                except:
                    szdqcode = ""

                ssdw = item['SSDW'][0]

                xzz = item['XZZ'][0]

                saje = item['SAJE'][0]

                xsgx = item['XSGX'][0]
                xsgxsql = "select CODE from pub_code_item where CODE_TYPE_NO ='administrative_area' and CODE_NAME = '"+xsgx+"'"
                try:
                    cursor.execute(xsgxsql)
                    xsgxcode = cursor.fetchone()[0]
                except:
                    xsgxcode = ""

                cysd = item['CYSD'][0]
                cysdsql = "select CODE from pub_code_item where CODE_TYPE_NO ='xsgx' and CODE_NAME = '"+cysd+"'"
                try:
                    cursor.execute(cysdsql)
                    cysdcode = cursor.fetchone()[0]
                except:
                    cysdcode = ""

                sql = "insert into xh_personinfo values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s)"
                data = (uuid, ajid, dwid, persontype, xm,
                        xbcode, csrq, age, zzmmcode, rddbcode,
                        zxwycode, rysfcode, zw, zjcode, cardtype,
                        cardid, whcdcode, szdqcode, ssdw, xzz,
                        saje, xsgxcode, cysdcode)
                cursor.execute(sql, data)
                db.commit()

def into_xh_unitinfo():
    with open("result.json",'r') as result:
        res = json.load(result)
        for item in res:
                uuid = item['UUID'][0]
                ajid = item['AJID'][0]
                dwmc = item['DWMC'][0]
                tyshxydm = item['TYSHXYDM'][0]
                frxm = item['FRXM'][0]
                frsa = item['FRSA'][0]
                unittype = item['UNITTYPE'][0]
                bcfj = item['BCFJ'][0]

                dwxz = item['DWXZ'][0]
                dwxzsql = "select CODE from pub_code_item where CODE_TYPE_NO ='dwxz' and CODE_NAME = '"+dwxz+"'"
                try:
                    cursor.execute(dwxzsql)
                    dwxzcode = cursor.fetchone()[0]
                except:
                    dwxzcode = ""

                szdq = item['DWXZ'][0]
                szdqsql = "select CODE from pub_code_item where CODE_TYPE_NO ='administrative_area' and CODE_NAME = '"+szdq+"'"
                try:
                    cursor.execute(szdqsql)
                    szdqcode = cursor.fetchone()[0]
                except:
                    szdqcode = ""

                licenseno = item['LICENSENO'][0]
                regadd = item['REGADD'][0]
                workadd = item['WORKADD'][0]

                sql = "insert into xh_unitinfo values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                data = (uuid, ajid, dwmc, tyshxydm, frxm, frsa, unittype, bcfj, dwxzcode, szdqcode, licenseno, regadd, workadd)
                cursor.execute(sql, data)
                db.commit()


if __name__ == '__main__':

    # connect database
    db = pymysql.connect(host="172.16.216.161", user="law", password="cistLAW1104", database="law", charset="utf8")
    # 创建游标
    cursor = db.cursor()
    into_xh_caseinfo()
    into_xh_personinfo()
    into_xh_unitinfo()
    cursor.close()
    db.close()

