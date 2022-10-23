import numpy as np
import time
import pandas as pd

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

def triangle(a):
        arr = [" "]*(2*a+1)
        arr[a] = "*"
        for i in range(a+1):
            arr[a+i] = "*"
            arr[a-i] = "*"
            for j in range(len(arr)):
                print(arr[j], end='')
            print('')

        return


def histDistanve(hist1, hist2):
    distanve = 0.0
    for i in range(len(hist1)):
        distanve += (hist1[i]-hist2[i])**2
    distanve = np.sqrt(distanve)
    return distanve

def fromCSV(path):
    hist = pd.read_csv(path)
    return hist


def toCSV(data, path):
    data = pd.DataFrame(data)
    data.to_csv(data, path = path, index=False)
    return

triangle(5)
data1, data2 = np.random.randint(0, 1000, size=1000000), np.random.randint(0, 1000, size=1000000)
hist1, hist2 = CalcHist(data1), CalcHist(data2)
print(histDistanve(hist1, hist2))