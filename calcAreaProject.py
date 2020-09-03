# -*- coding: utf-8 -*-
"""
Created on Tue May 26 10:58:09 2020

@author: 15751
"""

import random

#%%

class PlayerWindow():
    
    
    
    
   def __init__(self, name , parent = None):
      print("ok lets Go")
      self.m_unit = 1000.0   #无用参数
      #save dot data in this list
      self.maplist = []
      self.volumeDict = {}
      self.volume = 0
      self.name = name;
  

   # 制作地图点
   def mkMap(self):
       for i in range(0,1000):
           a = 0
           b = 100
           x = random.uniform(a, b)
           y = random.uniform(a, b)
           z = random.uniform(90, b)

           dot =  str(x) + ',' + str(y) + ',' + str(z)
           self.maplist.append(dot)
           
   #可以设置高度的上下限        
   def mkYourMap(self,lower,higher):
       for i in range(0,1000):
           a = 0
           b = 100
           x = random.uniform(a, b)
           y = random.uniform(a, b)
           z = random.uniform(lower, higher)
        
           dot =  str(x) + ',' + str(y) + ',' + str(z)
           self.maplist.append(dot)
               
       
           
           
          
            
   #保存地图点       
   def saveMap(self):
       mapfile = open(self.name,"w")
       #save dot in file
       for s in self.maplist:         
           mapfile.write(s + '\n')
       mapfile.close()
     
        
   #读取地图点
   def readMap(self):
       self.maplist.clear()  
       #C:\Users\15751
       mapName = "C:/Users/15751/" + self.name
       #mapName = "C:/Users/15751/map_1.txt"
       
       mapfile = open(mapName)
       line = mapfile.readline()
       self.maplist.append(line.strip('\n'))
       while line:
           line = mapfile.readline()
           if(line == ''):
               continue
           self.maplist.append(line.strip('\n'))
       mapfile.close()
       print(len(self.maplist))
       print(self.maplist)
   
    
   #把地图点放到 类 dict 里面
   def setEveryAreasdotsDict(self):
       for i in self.maplist:
           x,y,z = i.split(',')
           x = float(x)/10
           y = float(y)/10
           key = str(int(x)) + ":" + str(int(y)) 
           
           if( key  in self.volumeDict.keys()):
               oldstr = self.volumeDict[key]
               newstr = oldstr + "," + z
               self.volumeDict[key] = newstr
               
           else:
               self.volumeDict[key] = z
   #算面积           
   def calcVolume(self):
       self.volume = 0

       for i in self.volumeDict.values():
           sum_h = 0
           dots = i.split(',')
           for dot in dots:
               sum_h += float(dot)
           average_h = sum_h / len(dots)
           self.volume += average_h * 10 * 10
           
       print( self.name + "'s v0lume is :" + str(self.volume))
                   
       

           
        
#%%

if __name__ == "__main__":
    # okLetGo =  PlayerWindow("map.tx")
    # okLetGO_ = PlayerWindow("map_c.tx")
    okLetGo =  PlayerWindow("map_i.tx")
    okLetGO_ = PlayerWindow("map_j.tx")
    
    
    #云 聚在一起的时候测算 距离情况
    # okLetGo.mkMap()
    # okLetGo.saveMap()
    
    # okLetGO_.mkMap()
    # okLetGO_.saveMap()
    
    #云 有一定距离的时候的 距离情况
    okLetGo.mkYourMap(97, 100)
    okLetGo.saveMap()
    
    okLetGO_.mkYourMap(117, 120)
    okLetGO_.saveMap()
    
    #这三个可以封装一下
    okLetGo.readMap()
    okLetGo.setEveryAreasdotsDict()
    okLetGo.calcVolume()    
    
    #这三个可以封装一下
    okLetGO_.readMap()
    okLetGO_.setEveryAreasdotsDict()
    okLetGO_.calcVolume()    
    
    go = okLetGO_.volume - okLetGo.volume 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    