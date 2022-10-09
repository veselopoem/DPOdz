import numpy as np
import time


def CalcHist(x):
    hist = [0]*10
    for i in x:
        if i<100:
            hist[0]+=1
        elif i>=100 and i<200:
             hist[1]+=1
        elif i>=200 and i<300:
             hist[2]+=1
        elif i>=300 and i<400:
             hist[3]+=1
        elif i>=400 and i<500:
             hist[4]+=1
        elif i>=500 and i<600:
             hist[5]+=1
        elif i>=600 and i<700:
             hist[6]+=1
        elif i>=700 and i<800:
             hist[7]+=1
        elif i>=800 and i<900:
             hist[8]+=1
        else:
             hist[9]+=1
    return hist


def TimeCalc(x,n):
    CalcTime =np.array([1]*n, dtype = 'float32')
    for i in range(n):
        start = time.time()
        CalcHist(x)
        end = time.time()
        CalcTime[i-1] = end - start
    return CalcTime

x = np.random.randint(0,999,size = 1000000)
z = np.zeros(shape = 1000000)
CalcTime = TimeCalc(x,100)

print('Минимальное значение:',CalcTime.min(),'\n',
    'Максмальное значение:' ,CalcTime.max(),'\n',
    'Среднее значение:',  np.mean(CalcTime),'\n')