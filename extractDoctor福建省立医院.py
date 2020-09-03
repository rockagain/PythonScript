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
#for line in codecs.open('福建省立医院_简表.txt', encoding='utf-8'):
#    linelist = line.strip('\n').strip('\r').split('\t')
#    keshiDic[linelist[2]] = 0
#base = 'http://www.fjsl.com.cn/'
#base2 = 'http://www.fjsl.com.cn/Doctor/'
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
#dcap = dict(DesiredCapabilities.PHANTOMJS)
#dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36")
#browser = webdriver.PhantomJS(executable_path='D:/software/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs', desired_capabilities=dcap)
#
#browser.get(base2)   
#bsObj = BeautifulSoup(browser.page_source)
#
#keshiLIST = bsObj.findAll('td', {'background':'images/bg_18.gif'})
#for ks in keshiLIST:
#    keshi = ks.get_text()
#    #keshilshref=href + ks.find('a').attrs['href']
#    #browser.get(keshilshref)
#    browser.get(base2)   
#    bsObj = BeautifulSoup(browser.page_source)
#  
#    browser.find_element_by_link_text(keshi).click()
#        
#    bsObj = BeautifulSoup(browser.page_source)
#    doctorLIST = bsObj.findAll('tr',{'bgcolor':'#FFFFFF'})
#
#    if len(doctorLIST)<1:continue
#    for doc in doctorLIST:
#        name = doc.find('a').get_text().strip()
#        href = base + 'Doctor/' + doc.find('a').attrs['href']
#        string = '\t'.join([name, keshi, href])
#        string = string.replace('\u3000','').replace('\r','').replace('\n',' ')
#        string = string.replace('\xa0','').replace(' ','')
#        outfile = codecs.open('福建省立医院_简表.txt', 'a', 'utf-8')
#        try:
#            outfile.write(string+'\n')  
#        except:
#            print(string.replace('\t', '|'))
#        outfile.close()
#        
#    try:
#        browser.find_element_by_link_text('下一页').click()
#    
#        bsObj = BeautifulSoup(browser.page_source)
#    except:
#        continue
#    doctorLIST = bsObj.findAll('tr',{'bgcolor':'#FFFFFF'})
#    for doc in doctorLIST:
#        name = doc.find('a').get_text().strip()
#        href = base + 'Doctor/' + doc.find('a').attrs['href']
#        string = '\t'.join([name, keshi, href])
#        string = string.replace('\u3000','').replace('\r','').replace('\n',' ')
#        string = string.replace('\xa0','').replace(' ','')
#        outfile = codecs.open('福建省立医院_简表.txt', 'a', 'utf-8')
#        try:
#            outfile.write(string+'\n')  
#        except:
#            print(string.replace('\t', '|'))
#        outfile.close()
#   
#    try:
#        browser.find_element_by_link_text('下一页').click()
#        bsObj = BeautifulSoup(browser.page_source)
#    except:
#        continue
#    doctorLIST = bsObj.findAll('tr',{'bgcolor':'#FFFFFF'})
#    for doc in doctorLIST:
#        name = doc.find('a').get_text().strip()
#        href = base + 'Doctor/' + doc.find('a').attrs['href']
#        string = '\t'.join([name, keshi, href])
#        string = string.replace('\u3000','').replace('\r','').replace('\n',' ')
#        string = string.replace('\xa0','').replace(' ','')
#        outfile = codecs.open('福建省立医院_简表.txt', 'a', 'utf-8')
#        try:
#            outfile.write(string+'\n')  
#        except:
#            print(string.replace('\t', '|'))
#        outfile.close()
#    

#%%
outfile = open('福建省立医院_医生列表.txt', 'a')
outfile.close()
doctorDic = {}
for line in codecs.open('福建省立医院_医生列表.txt', encoding='utf-8'):
    doctorDic[line.strip().split('\t')[-1]]=0

href2doctor = {}
for line in codecs.open('福建省立医院_简表.txt', encoding='utf-8'):
    linelist = line.strip('\n').strip('\r').split('\t')
    href2doctor[linelist[-1]] = '\t'.join(linelist[0:-1])
    
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36")
browser = webdriver.PhantomJS(executable_path='D:/software/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs', desired_capabilities=dcap)

  

for href in href2doctor:
    if href in doctorDic:
        continue
    try:
        browser.get(href) 
        bsObj = BeautifulSoup(browser.page_source)
        
        total = bsObj.find('td',{'width':'64%'}).get_text().replace('\t','').replace(' ','').replace('\n','')
        zhicheng = total.split('职称:')[1].split('所属科室:')[0]
        jianjie = total.split('简介：')[-1]
        jianjie = jianjie.replace('\t', '').replace('\r','').replace('\n','')
    except:
        print(href)
        time.sleep(1)
        continue
    string = '\t'.join([href2doctor[href], zhicheng, jianjie, href])
    string = string.replace('\u3000','').replace('\r','').replace('\n',' ')
    string = string.replace('\xa0','').replace('  ',' ')
    outfile = codecs.open('福建省立医院_医生列表.txt', 'a','utf-8')
    try:
        outfile.write(string+'\n')
    except:
        print(string.replace('\t', '|'))
    outfile.close()
    time.sleep(1)
