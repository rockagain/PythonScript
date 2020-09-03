# -*- coding: utf-8 -*-
"""
author       :  Gao
create date  :
modified date: 
verstion     : 
#==============================================================================
# 
#==============================================================================
"""
#%%% import modules
from bs4 import BeautifulSoup
import time, codecs
from selenium import webdriver
import os
#from urllib.request import urlopen

#%%% inputs and outputs
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
driver = webdriver.Chrome(chrome_options=options)
href = "http://www.hanjilibrary.com/"
base = 'http://www.hanjilibrary.com'


#%%
#keshiDic = {}
#for line in codecs.open('汉籍数字图书馆_简表.txt', encoding='utf-8'):
#    linelist = line.strip('\n').strip('\r').split('\t')
#    keshiDic[linelist[2]] = 0

#firstDir = "c:\\經部\\"

#firstDir = "丛部"
#
driver.get(href)
##driver.switch_to.frame("main")  # 3.用name来定位    Leftmenu
#
#time.sleep(1)
#
driver.switch_to.frame("Leftmenu")

#
bsObj = BeautifulSoup(driver.page_source)

wubuTotal = bsObj.find('ul',{"class":"wubu"})
wubuList = wubuTotal.findAll("ul")
      # wubuList[0]      wubuList[13]      wubuList[28]   wubuList[44]    wubuList[49]
second = wubuList[49].findAll("h4") 


for ob in second:
     secondDir = ob.get_text() 
     try:
         third = ob.next_sibling.findAll("a")
     except:
         thirdDir = ""
         href = base + ob.find("a").attrs['href']
         string = '\t'.join([firstDir, secondDir, thirdDir,href])
#        string = string.replace('\u3000','').replace('\r','').replace('\n',' ')
#        string = string.replace('\xa0','').replace(' ','')
         outfile = codecs.open('汉籍数字丛部_简表.txt', 'a', 'utf-8')
         try:
             outfile.write(string+'\n')  
         except:
             print(string.replace('\t', '|'))
         outfile.close()
         continue            
     
     for ob in third:
         thirdDir = ob.get_text()
         href = base + ob.attrs['href']
         string = '\t'.join([firstDir, secondDir, thirdDir,href])
#        string = string.replace('\u3000','').replace('\r','').replace('\n',' ')
#        string = string.replace('\xa0','').replace(' ','')
         outfile = codecs.open('汉籍数字丛部_简表.txt', 'a', 'utf-8')
         try:
             outfile.write(string+'\n')  
         except:
             print(string.replace('\t', '|'))
         outfile.close()
     #time.sleep(1)
driver.close()

#%%
#outfile = open('C://Users//kk//Desktop//汉籍数字图书馆五部//汉籍数字五部_总表.txt', 'a')
#outfile1 = open('C://Users//kk//Desktop//汉籍数字图书馆五部//汉籍数字五部_简表.txt', 'a')
#outfile.close()
#outfile1.close()
#
#wubuDic = {}
#for line in codecs.open('C://Users//kk//Desktop//汉籍数字图书馆五部//汉籍数字五部_总表.txt', encoding='utf-8'):
#    wubuDic[line.strip().split('\t')[-1]]=0
#
#href2wubu = {}
#for line in codecs.open('C://Users//kk//Desktop//汉籍数字图书馆五部//汉籍数字五部_简表.txt', encoding='utf-8'):
#    linelist = line.strip('\n').strip('\r').split('\t')
#    href2wubu[linelist[-1]] = '\t'.join(linelist[0:-1])
#
#
#
#    
#    
#    
#for href in href2wubu:
#    if href in wubuDic:
##        continue
#        pass
#    else:
#    
##    try:
#        totalDir = href2wubu[href].split("\t")
#        isDir = "C://Users//kk//Desktop//汉籍数字图书馆五部//"  + totalDir[0] + "//" + totalDir[1] + "//"
#
#        if(not  os.path.exists(isDir)):
#            os.makedirs(isDir)
#            
#        
#        driver.get(href)
#        bsObj = BeautifulSoup(driver.page_source)
#        
#        fileName = (href2wubu[href]).split("\t")[-1]
#        if(fileName == ""):
#            fileName =  (href2wubu[href]).split("\t")[-2]
#        fileName = isDir +  fileName + ".txt"
#        
#        
#        
#        pageNum  =  int(bsObj.find("p",{"class":"fyinfo"}).findAll("b")[2].get_text()) + 1 
#        for  i in range(1,pageNum):
#            href_next = href + "&page=" + str(i)
#            #print(href_next)
#            time.sleep(1)
#            driver.get(href_next)
#            bsObj = BeautifulSoup(driver.page_source)                        
#            total = bsObj.find('dl', {'class':'cfirst'})
#            books = total.findAll('dd',recursive=False)
#            
#            
#            for book in books:
#                
#                bookState = book.i.attrs["class"][0].split("-")[-1]
#                
#                orderNumber = book.find("span",{"class":"dth1"}).get_text()
#                orderNumber = orderNumber.replace(" ","").replace("◆","").replace("\u3000","").replace(" ","").replace("\n","")
#    
#                name = book.find("span",{"class":"dth2"}).get_text()
#                author = book.find("span",{"class":"dth3"}).get_text().replace("\u3000","")
#                versionInfo = book.findAll("dd")
#                bkstring = "\t".join([orderNumber,name,author,bookState]).replace("\u3000","").replace(" ","").replace("\n","")
#                
#                outfile = codecs.open(fileName,"a","utf-8")
#                outfile.write(bkstring + "\n")
#                outfile.close()
#                
#                
#                for vs in versionInfo:
#                    version =  orderNumber + "-" + vs.find("span",{"class":"nth1"}).get_text()
#                    versionNm = vs.find("span",{"class":"nth2"}).get_text()
#                    editionNm = vs.find("span",{"class":"nth3"}).get_text()
#                    edstring = "\t" + "\t".join([version,versionNm,editionNm]).replace(" ","").replace("\n","").replace("\u3000","")
#                    
#                    outfile = codecs.open(fileName,"a","utf-8")
#                    outfile.write(edstring + "\n")        
#                    outfile.close() 
#                    
#                    
#                    
#                    editionNumber = vs.findAll("tr")
#                    if(editionNumber == []):
#                        pass
#                    else:
#                        for ed in editionNumber[1:]:    
#                            num = version + ed.findAll("td")[0].get_text().replace("印本","-")
#                            imageQuality = ed.findAll("td")[1].get_text()
#                            filenum = ed.findAll("td")[2].get_text()
#                            totalnum = ed.findAll("td")[3].get_text().replace("\n","").replace(" ","")
#                            totalsize = ed.findAll("td")[4].get_text().replace("\n","").replace(" ","") + "MB"
#                            string = "\t\t" + "\t".join([num,imageQuality,filenum,totalnum,totalsize])
#                            
#                            outfile = codecs.open(fileName,"a","utf-8")                           
#                            outfile.write(string + "\n")
#                            outfile.close()
#                            
#                    
#                outfile.close()
#        
#            log = codecs.open('C://Users//kk//Desktop//汉籍数字图书馆五部//汉籍数字五部_总表.txt', 'a')
#            log.write(href_next + "\n")
#            log.close()
#        
##
##
##    except：
##        print(href)
##        time.sleep(1)
##        continue
 
