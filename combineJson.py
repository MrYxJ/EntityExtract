# -*- coding: utf-8 -*-
"""
Created on Sun May 12 01:26:01 2019

@author: 44128
"""

import json

jsonFile1 = r'personinfo.json'
jsonFile2 = r'caseinfo.json'
jsonSave = r'save.json'

with open(jsonFile1,'r',encoding='utf-8')as f1:    
    dic1 = json.load(f1)
with open(jsonFile2,'r',encoding='utf-8')as f2:
    dic2 = json.load(f2)

#print(len(dic2))
for key in dic1:
    dic1[key]['caseinfo'] = dic2[key]['caseinfo']
with open(jsonSave,'w',encoding='utf-8')as f3:
    f3.write(json.dumps(dic1,ensure_ascii=False, indent=3))

print('successfully combine!')
