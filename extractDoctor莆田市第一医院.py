# -*- coding: utf-8 -*-
"""
author       : Xiaojun Wang
create date  :
modified date: 
verstion     : 
#==============================================================================
# 
#==============================================================================
"""
#%%% import modules
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time, codecs

#%%% inputs and outputs
#keshiDic = {}
#for line in codecs.open('莆田市第一医院_简表.txt', encoding='utf-8'):
#    linelist = line.strip('\n').strip('\r').split('\t')
#    keshiDic[linelist[2]] = 0
#base = 'http://www.ptsyy.com/'
#href = 'http://www.ptsyy.com/index.php/section.html'
#html = urlopen(href)
#bsObj = BeautifulSoup(html)
#keshiLIST = bsObj.find('div', {'class':'right_main'}).findAll('td')
#for ks in keshiLIST:
#    keshi = ks.get_text()[1:]
#    href = ks.find('a').attrs['href']
#    html = urlopen(href)
#    bsObj = BeautifulSoup(html)
#    kshref = bsObj.findAll('a',{'class':'more'})[2].attrs['href']
#    kshtml = urlopen(kshref)
#    bsObj = BeautifulSoup(kshtml)
#    try:
#        doctorLIST = bsObj.find('div',{'class':'r_doctor'}).findAll('div',{'class':'doctor'})
#    except:
#        continue
#    if len(doctorLIST)<1:continue
#    for doc in doctorLIST:
#        name = doc.find('a').find('img').attrs['alt']
#        href = doc.find('a').attrs['href']
#        string = '\t'.join([name, keshi, href])
#        string = string.replace('\u3000','').replace('\r','').replace('\n',' ')
#        string = string.replace('\xa0','').replace(' ','')
#        outfile = codecs.open('莆田市第一医院_简表.txt', 'a', 'utf-8')
#        try:
#            outfile.write(string+'\n')  
#        except:
#            print(string.replace('\t', '|'))
#        outfile.close()

#%%
outfile = open('莆田市第一医院_医生列表.txt', 'a')
outfile.close()
doctorDic = {}
for line in codecs.open('莆田市第一医院_医生列表.txt', encoding='utf-8'):
    doctorDic[line.strip().split('\t')[-1]]=0

href2doctor = {}
for line in codecs.open('莆田市第一医院_简表.txt', encoding='utf-8'):
    linelist = line.strip('\n').strip('\r').split('\t')
    href2doctor[linelist[-1]] = '\t'.join(linelist[0:-1])

for href in href2doctor:
    if href in doctorDic:
        continue
    try:
        html = urlopen(href)
        bsObj = BeautifulSoup(html)
        total = bsObj.find('div', {'style':'float:left;width:540px;'}).get_text().replace('\n','').replace('\t','')
        zhicheng = total.split('职称：')[1].split('简介：')[0]
        
    except:
        print(href)
        time.sleep(1)
        continue
    string = '\t'.join([href2doctor[href], zhicheng, href])
    string = string.replace('\u3000','').replace('\r','').replace('\n',' ')
    string = string.replace('\xa0','').replace('  ',' ')
    outfile = codecs.open('莆田市第一医院_医生列表.txt', 'a','utf-8')
    try:
        outfile.write(string+'\n')
    except:
        print(string.replace('\t', '|'))
    outfile.close()
    time.sleep(1)
