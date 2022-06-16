

from sklearn import svm
from sklearn.svm import SVR
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import pymysql
import itertools
import matplotlib.dates as mdates
import FinanceDataReader as fdr



class svm_al():
    def __init__(self, date:int):
        self.date = date

    def close_data(self, code:str):
        self.code = code
        self.data = fdr.DataReader(code,self.date)
        self.close = self.data['Close']
        self.value = self.close.values
        return self.data
        
    def svm_learn(self):
        days = []
        j = 1
        for j in range(len(self.data)):
            days.append([int(j+1)])
            j += 1
            
        lin_svr = SVR(kernel='linear', C=1000)
        lin_svr.fit(days, self.value)

        poly_svr = SVR(kernel='poly', C=1000, degree=2)
        poly_svr.fit(days, self.value)

        rbf_svr = SVR(kernel='rbf', C=1000, gamma=0.05)
        rbf_svr.fit(days, self.value)
        
        day = [[len(days)+1]]
        rbf_svr = rbf_svr.predict(day)
        lin_svr = lin_svr.predict(day)
        poly_svr = poly_svr.predict(day)
        
        return rbf_svr, lin_svr, poly_svr, days
    
    def dpc(self):
        close_data = self.value.tolist()
        days = []
        j = 1
        for j in range(len(self.data)):
            days.append([int(j+1)])
            j += 1
            
        lin_svr = SVR(kernel='linear', C=1000)
        lin_svr.fit(days, self.value)
    
        dpc = []
        lin_data = []
        for day in days:
            lin_data.append(lin_svr.predict([day]).tolist())

        lin_data = list(itertools.chain(*lin_data))

        for i in range(len(days)):
            result = (close_data[i] /lin_data[i]-1)*100
            dpc.append(round(result,2))
            
        return dpc
    