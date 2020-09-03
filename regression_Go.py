# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 08:52:53 2020

@author: ning yang
"""

'''import redis
import torch'''



import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

import numpy as np
from matplotlib.pyplot import MultipleLocator

#import threading

import sys
import math
import heapq
import arrow



#%%





# r = redis.StrictRedis(host="localhost",port=6379,db=0)

# r.set("foo","bar")


# 调整类，假如小于10 ，或者减到了一半就直接返回 ， 又或r到达了 0.8 直接 OK    # howMany 这个参数是计数的，毕竟里面需要有零
def refineArray(array,minNumber,interval , howMANy ,reduceRatio):
    
    x = []
    y = []          
        
    if(howMANy < minNumber):
        return array
    
    for i in array:
        
        if( float(i) == 0):
            y.append(0)
            continue
        y.append(float(i))

    for i in range(0, len(y)):
        x.append(i * int(interval))
        
    R = computeCorrelation(x, y)
    
    if(R > 0.8):
        return y
    else:
        x_calc = []
        y_calc = []
        count = 0
        for i in y:

            if(i == 0):
                continue
            else:
                y_calc.append(i)
                x_calc.append(x[count])
                count = count + 1    
        f = np.polyfit(x_calc, y_calc, 1)
        func =  np.poly1d(f)
        #减少了多少
        reduceNumber = int(howMANy * reduceRatio)
        howMANy = howMANy - reduceNumber
        
        distance = [abs(y_calc[i] - func(x_calc[i])) for i in range(0,len(x_calc))]
        #distance = [int(i) for i in distance]
        index = map(distance.index, heapq.nlargest(reduceNumber, distance))
        listIndex = list(index)
        
        # 把不ok的点都设置为 0 
        for i in listIndex:
            y[i] = 0
        
        
        #y = refineArray(y, minNumber, interval, howMANy, reduceRatio)
        return refineArray(y, minNumber, interval, howMANy, reduceRatio)            
    
    




# 计算相关度
def computeCorrelation(x,y):
    
    x_calc = []
    y_calc = []
    count = 0
    for i in y:
        
        if(i == 0):
            continue
        else:
            y_calc.append(i)
            x_calc.append(x[count])
        count = count + 1        
    xBar = np.mean(x_calc)
    yBar = np.mean(y_calc)
    SSR = 0.0
    varX = 0.0
    varY = 0.0
    for i in range(0,len(x)):
        diffXXbar = x[i] - xBar
        difYYbar = y[i] - yBar
        SSR += (diffXXbar * difYYbar)
        varX += diffXXbar**2
        varY += difYYbar**2
    SST = math.sqrt(varX * varY)
    return SSR/SST
      


#%%


class regression_Img():
 
    
      def __init__(self, name , parent = None):
         
          #print("ok lets Go")
          
          #版本号  起个名字
          self.name = name
          
          #Time
          self.time = ""
          
          #时间的间隔
          self.interval = ""
          
          #速度的数组
          self.velocity = []         
          self.Sma_velocity = []          
          self.Lma_velocity = []    
          
          #消灭率 每次消除的点     三组数都一样， 所以取一样的值就可以
          
          self.reduceRatio = 0.2
          
          #limitNumber       数字在这个数下面就直接停止计算， 然后拟合   
          
          self.minNumber = 10

          
          #限制 factor       小于10的情况下不予考虑 
          
          self.LimitFactor = 0.5 
          
          #How MANy line
          
          self.Three = False
          
          # time 日期管理库   把握住时间    #在这里初始化一下
          
          self.hold_Time = arrow.utcnow()


      def init_redis_related(self):
          
          '''r = redis.Redis(host='localhost', port=6379, decode_responses=True)   
          # r = redis.StrictRedis(host="localhost",port=6379,db=0)
          r.set("foo","bar")'''
          pass
          
  

    
        
      #   set parameters
      def letsGo_setParameters(self,string):
          
          strings = string.split(' ')          
          self.timeManager((strings[-1]).replace('starttime:',''))
          
          
          if("sma" in string):         # 多种参数的情况下
              self.Three = True
              
              #set interval
              self.interval  =  (strings[3]).split(":")[1]
              
              #print("Interval is : " + self.interval)
              
              #set everyVelocity
              #之后可以尝试下加速分组
              for i in  (strings[0]).split(":")[1].split(","):
                  self.velocity.append(i)
                  
                  
              #set short mean accelerate
              for i in  (strings[1]).split(":")[1].split(","):
                  self.Sma_velocity.append(i)
                  

              #set short mean accelerate
              for i in  (strings[2]).split(":")[1].split(","):
                  self.Lma_velocity.append(i)
              
          else:                        # 单一参数的情况下
              self.Three = False
              
              #set interval
              self.interval  =  (strings[1]).split(":")[1]
              
              #print("Interval is : " + self.interval)
              
              #set everyVelocity
              for i in  (strings[0]).split(":")[1].split(","):
                  self.velocity.append(i)
              #print(self.velocity)

    

      
      def timeManager(self,timeStr):
          
          self.time = timeStr.replace(","," ")
          self.hold_Time = arrow.get(self.time)
    



      
    
      def regression_Draw_Three_Line(self):




          
          # 0. 设置中文
          plt.rcParams['font.sans-serif']=['SimHei']
          plt.rcParams['axes.unicode_minus'] = False
          x_Max = 0 

          
          # 1. 第一条线点
          x = []
          y = []

          for i in self.velocity:
              if(float(i) == 0):
                  y.append(0)
              else:    
                  y.append(1 / float(i))          

          # 1.0 因为上面去除点 全部设成零了， 所以这里我们要把所有 零点  抛出去，  不放在划线的地方了， 注意要把x点正确更新
          for i in range(0, len(y)):
              if(y[i] != 0):
                  x.append(i * int(self.interval))
                  
          # 1.1 更新 y ，把 零点 去除出去
          y = [i for i in y if i != 0]
             #用3次多项式拟合
          f1 = np.polyfit(x, y, 1)
             # print('f1 is :\n',f1)
          p1 = np.poly1d(f1)
             # print('p1 is :\n',p1)
          huapo =  (-1 * f1[1] / f1[0]) / 60
          print("time:"+ str(huapo))
          #huapoFromOOA = (start * interval + -1 * f1[1] / f1[0]) / 60
          #print(r'使用', (end - start) * interval / 60, '小时数据进行预测,', r'滑坡时间',huapo, '小时后', r'滑坡时间在初始时间',
          #huapoFromOOA, '小时后')
             # return  huapo
        
           #也可使用yvals=np.polyval(f1, x)
          yvals = p1(x)  #拟合y值
          yvals_1 = [i + 1 for i in yvals]
             #     print('yvals is :\n',yvals)
             #绘图
             #     plot1 = plt.plot(x, y, 's',label='original values')
             #     plot2 = plt.plot(x, yvals, 'r',label='polyfit values')
          plot1 = plt.plot(x, y, 'o',color= 'cornflowerblue', label='speed')
          plot2 = plt.plot(x, yvals, 'cornflowerblue')
          
          x_Max = x[-1]

          # 2. 第二条线点
          x = []
          y = []
          
          for i in self.Sma_velocity:
              if(float(i) == 0):
                  y.append(0)
              else:    
                  y.append(1 / float(i))          

          # 2.0 因为上面去除点 全部设成零了， 所以这里我们要把所有 零点  抛出去，  不放在划线的地方了， 注意要把x点正确更新
          for i in range(0, len(y)):
              if(y[i] != 0):
                  x.append(i * int(self.interval))
                  
          # 2.1 更新 y ，把 零点 去除出去
          y = [i for i in y if i != 0]
             #用3次多项式拟合
          f1 = np.polyfit(x, y, 1)
             # print('f1 is :\n',f1)
          p1 = np.poly1d(f1)
             # print('p1 is :\n',p1)
          huapo =  (-1 * f1[1] / f1[0]) / 60
          print("time:"+ str(huapo))
          #huapoFromOOA = (start * interval + -1 * f1[1] / f1[0]) / 60
          #print(r'使用', (end - start) * interval / 60, '小时数据进行预测,', r'滑坡时间',huapo, '小时后', r'滑坡时间在初始时间',
          #huapoFromOOA, '小时后')
             # return  huapo
        
           #也可使用yvals=np.polyval(f1, x)
          yvals = p1(x)  #拟合y值
          yvals_1 = [i + 1 for i in yvals]
             #     print('yvals is :\n',yvals)
             #绘图
             #     plot1 = plt.plot(x, y, 's',label='original values')
             #     plot2 = plt.plot(x, yvals, 'r',label='polyfit values')
          plot1 = plt.plot(x, y, 'o',color = 'orange', label='lma')
          plot2 = plt.plot(x, yvals, 'orange')  
          
          if(x[-1] > x_Max):
              x_Max = x[-1]
          
          # 3. 第三条线点
          x = []
          y = []

          for i in self.Lma_velocity:
              if(float(i) == 0):
                  y.append(0)
              else:    
                  y.append(1 / float(i))             

          # 3.0 因为上面去除点 全部设成零了， 所以这里我们要把所有 零点  抛出去，  不放在划线的地方了， 注意要把x点正确更新
          for i in range(0, len(y)):
              if(y[i] != 0):
                  x.append(i * int(self.interval))
                  
          # 3.1 更新 y ，把 零点 去除出去
          y = [i for i in y if i != 0]
             #用3次多项式拟合
          f1 = np.polyfit(x, y, 1)
             # print('f1 is :\n',f1)
          p1 = np.poly1d(f1)
             # print('p1 is :\n',p1)
          huapo =  (-1 * f1[1] / f1[0]) / 60
          print("time:"+ str(huapo))
          #huapoFromOOA = (start * interval + -1 * f1[1] / f1[0]) / 60
          #print(r'使用', (end - start) * interval / 60, '小时数据进行预测,', r'滑坡时间',huapo, '小时后', r'滑坡时间在初始时间',
          #huapoFromOOA, '小时后')
             # return  huapo
        
           #也可使用yvals=np.polyval(f1, x)
          yvals = p1(x)  #拟合y值
          yvals_1 = [i + 1 for i in yvals]
             #     print('yvals is :\n',yvals)
             #绘图
             #     plot1 = plt.plot(x, y, 's',label='original values')
             #     plot2 = plt.plot(x, yvals, 'r',label='polyfit values')
          plot1 = plt.plot(x, y, 'o',color ='pink', label='sma')
          plot2 = plt.plot(x, yvals, 'pink')  
          

          plt.xlabel('时间')       # x
          plt.ylabel('速度倒数')   # y
          
          if(x[-1] > x_Max):
              x_Max = x[-1]
          
          # 4.0 设置         
          tricks = [ i * 60 for i in range(0,x_Max) if i*60 <= x[-1] ]
          x_axis_data_name = []
          
          #
          for i in range(0,len(tricks)):          
              #可能需要在这里更新一下
              x_axis_data_name.append(self.hold_Time.format('YYYY-MM-DD HH:mm:ss'))
              self.hold_Time = self.hold_Time.shift(hours=+1)
          
          x_ticks_label = [i for i in x_axis_data_name]
          

          x_major_locator = MultipleLocator(60)
          
          ax = plt.gca()   
          #ax为两条坐标轴的实例
          ax.xaxis.set_major_locator(x_major_locator)
          ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
          ax.yaxis.grid(True, which='major')  # y坐标轴的网格使用次刻度
          
          plt.xticks(tricks,x_ticks_label,rotation = 270)
          plt.legend(loc=3,prop={'size':8})  #指定legend的位置右下角
          plt.title("速度倒数法拟合曲线")
          plt.savefig('pic.png', dpi=1000)

          #plt.show()
      
     
        

      def regression_Draw_One_Line(self):

          # 0. 设置中文
          plt.rcParams['font.sans-serif']=['SimHei']
          plt.rcParams['axes.unicode_minus'] = False
          
          
          

          
          x = []
          y = []
          
          for i in self.velocity:
              if(float(i) == 0):
                  y.append(0)
              else:    
                  y.append(1 / float(i))
                  
          # 0.1 因为上面去除点 全部设成零了， 所以这里我们要把所有 零点  抛出去，  不放在划线的地方了， 注意要把x点正确更新
          for i in range(0, len(y)):
              if(y[i] != 0):
                  x.append(i * int(self.interval))
                  
          # 0.2 更新 y ，把 零点 去除出去
          y = [i for i in y if i != 0]
              
            
          #用3次多项式拟合         
          f1 = np.polyfit(x, y, 1)
             # print('f1 is :\n',f1)
          p1 = np.poly1d(f1)
             # print('p1 is :\n',p1)
          huapo =  (-1 * f1[1] / f1[0]) / 60
          print("time:"+ str(huapo))
          #huapoFromOOA = (start * interval + -1 * f1[1] / f1[0]) / 60
          #print(r'使用', (end - start) * interval / 60, '小时数据进行预测,', r'滑坡时间',huapo, '小时后', r'滑坡时间在初始时间',
          #huapoFromOOA, '小时后')
             # return  huapo
        
           #也可使用yvals=np.polyval(f1, x)
          yvals = p1(x)  #拟合y值
          yvals_1 = [i + 1 for i in yvals]
             #     print('yvals is :\n',yvals)
             #绘图
             #     plot1 = plt.plot(x, y, 's',label='original values')
             #     plot2 = plt.plot(x, yvals, 'r',label='polyfit values')
          plot1 = plt.plot(x, y, 'o' ,label='speed')      # color= 'cornflowerblue',   突出对比
          plot2 = plt.plot(x, yvals, 'cornflowerblue', label='regresstionLine')
          #plot3 = plt.plot(x, yvals_1,'b',label='nextline')
          #plot4 = plt.plot(x, [i+ 0.5 for i in yvals],'y',label='thirdline')
          plt.xlabel('时间')       # x
          plt.ylabel('速度倒数')   # y

          x_major_locator = MultipleLocator(60)
          
          ax = plt.gca()          

          #ax为两条坐标轴的实例
          ax.xaxis.set_major_locator(x_major_locator)
         
            
          # 0.3根据真实数量 ，把x 角标 初始化一下
          #,x_ticks_label
          tricks = [ i * 60 for i in range(0,x[-1]) if i*60 <= x[-1] ]
          x_axis_data_name = []
          
          #
          for i in range(0,len(tricks)):          
              #可能需要在这里更新一下
              x_axis_data_name.append(self.hold_Time.format('YYYY-MM-DD HH:mm:ss'))
              self.hold_Time = self.hold_Time.shift(hours=+1)
          
          x_ticks_label = [i for i in x_axis_data_name]
          

          
          ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
          ax.yaxis.grid(True, which='major')  # y坐标轴的网格使用次刻度
          

          plt.xticks(tricks,x_ticks_label,rotation = 270)
          plt.legend(loc=3,prop={'size':8})  #指定legend的位置右下角
          plt.title('速度倒数法拟合曲线')
          plt.savefig('pic.png', dpi=1000)

          plt.show()
      


      


  
      
      # 把不ok的点都去除了   # 都设置成0
      def checkOkPoints(self):
          
          if(self.Three == True):
              
              if( (len(self.velocity) * self.LimitFactor)  < 10):
                  self.minNumber = 10
              else:
                  self.minNumber = self.minNumber * self.LimitFactor
                  
              self.velocity =  refineArray(self.velocity,self.minNumber,self.interval,len(self.velocity),self.reduceRatio)
              self.Sma_velocity = refineArray(self.Sma_velocity,self.minNumber,self.interval,len(self.Sma_velocity),self.reduceRatio)
              self.Lma_velocity = refineArray(self.Lma_velocity,self.minNumber,self.interval,len(self.Lma_velocity),self.reduceRatio)
          
          else:
              
              if( (len(self.velocity) * self.LimitFactor)  < 10):
                  self.minNumber = 10
              else:
                  self.minNumber = self.minNumber * self.LimitFactor
                  
              self.velocity = refineArray(self.velocity,self.minNumber,self.interval,len(self.velocity),self.reduceRatio)
          

#%%        

#剩余 8个值或者 9个值  减到 10 以下          
        
if __name__ == "__main__":
    
    # 1. 初始化类， 附带版本号
    okLetsGo = regression_Img("v 0.1.0")
    
    # 2.1 调用脚本模式
    if(len(sys.argv) == 2):
        
        # 3. 执行功能代码，划分参数
        okLetsGo.letsGo_setParameters(sys.argv[1])
        
        # 4. 检查R值是否大于 0.8 ， 或者是否满足数量条件
        okLetsGo.checkOkPoints()
        
        # 5. 划线
        if(okLetsGo.Three):
            
            # 5.1   划三条线
            okLetsGo.regression_Draw_Three_Line()
            
        else:
            
            # 5.2   划一条线
            okLetsGo.regression_Draw_One_Line()    
               
    else:
        
        # 2.2 测试模式
        
        #print("YOU MUST HAVE ONLY ONE PARAMETER!")
        
        # 2.2.1  三个的例子
        #okLetsGo.letsGo_setParameters("speed:0.5552645,0.6595245,1.11111,1.5,2.6,5 sma:0.6552645,0.7595245,1.71111,1.8,3.9,6 lma:0.7552645,0.8595245,2.11111,3.5,4.6,7 interval:60 starttime:2018-03-03,00:00:00")
        # 2.2.2  一个的例子
        #okLetsGo.letsGo_setParameters("speed:0.5552645,0.6595245,1.11111,1.5,2.6,5,6,7,8,9,10,11,21,23,25,112 interval:60 starttime:2018-03-03,00:00:00")
        
        # 3. 执行功能代码    
        
        # 3.1  真实数据测一组
        #okLetsGo.letsGo_setParameters("speed:1.27636,0.92495,0.99056995,0.70296,1.047037,0.60007703,0.847197,1.108715,0.87866,1.296215,1.306042,1.3901191,1.3683717,0.5255663 interval:60 starttime:2019-12-30,00:00:00")
        # 3.2  真实数据测三组
        okLetsGo.letsGo_setParameters("speed:1.27636,0.92495,0.99056995,0.70296,1.047037,0.60007703,0.847197,1.108715,0.87866,1.296215,1.306042,1.3901191,1.3683717,0.5255663 sma:1.0639601,0.87282664,0.9135223,0.78335804,0.83143705,0.85199636,0.94485736,1.09453,1.1603056,1.3307921,1.3548442,1.0946857,0.63131267,0.17518876 lma:0.9236591,0.85213184,0.88275933,0.8641078,0.96298355,1.0061511,1.1378247,1.2246871,1.1274956,0.98105234,0.7650165,0.54734284,0.31565633,0.08759438 interval:60 starttime:2019-12-30,00:00:00")
        
        # 4. 检查R值是否大于 0.8 ,  或者是否满足数量条件
        okLetsGo.checkOkPoints()
        
        # 5. 划线
        if(okLetsGo.Three):
            
            # 5.1   划三条线
            okLetsGo.regression_Draw_Three_Line()
        else:
            
            # 5.2    划一条线
            okLetsGo.regression_Draw_One_Line()    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        