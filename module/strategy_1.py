#플라스크, DB
from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint, current_app
from DB.strategyDB import strategy
##백엔드
from pandas_datareader import data as pdr 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import yfinance as yf 
import pandas as pd
import pymysql
import re
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import datapackage
import pandas as pd
import math
import numpy as np 

yf.pdr_override()


                        #모듈이름
strategy_1 = Blueprint('strategy_1', __name__, url_prefix='/strategy')
@strategy_1.route('/')
def strategy_1_main(): #Function은 Blueprint 이름과 달라야함
    return render_template('strategy_1.html')


@strategy_1.route('/strategy_1_result', methods=['POST'])
def strategy_1_result(): 
    codeli= request.form.get('codelist') #html -> 리스트객체로 receive   
    codelis= codeli.replace(" ","") #리스트의 공백제거 
    codelist= codelis.split(',')
    startdate= request.form.get('startdate') 
    enddate= request.form.get('enddate')  
    print(codelist)
    df= pd.DataFrame() 
    strategydb = strategy() 
    for code in codelist:

        stock_code = code.replace("-","_")
        df[stock_code]= strategydb.getUSstock_close(code,startdate,enddate)

    df_AAPL_close = strategydb.getDB_STAT_1('AAPL', startdate,enddate)['date'] #종가일자를 애플로 맞춘다.
    df= pd.concat([df_AAPL_close,df],axis=1)
    df = df.fillna(method='bfill') # 'NAN'뒤 값으로 전을 채운다. 
    df = df.fillna(method='ffill') # 'NAN'전의 값으로 뒤를 채운다. 

    df1= df.iloc[:, 1:]
    daily_ret= df1.pct_change() #일간변동률 
    annual_ret= daily_ret.mean()* 253 #연평균 일간변동률
    daily_cov= daily_ret.cov() # 일간변동률의 공분산
    annual_cov= daily_cov*253 #연간리스크 
    port_ret= [] 
    port_risk=[] 
    port_weights=[] 
    sharpe_ratio=[] 

    for i in range(20000):  
        weights= np.random.random(len(codelist)) 
        weights /= np.sum(weights)
        
        returns=np.dot(weights, annual_ret) 
        risk= np.sqrt(np.dot(weights.T, np.dot(annual_cov,weights)))
        
        port_ret.append(returns)
        port_risk.append(risk)
        port_weights.append(weights) 
        sharpe_ratio.append(returns/risk)
        
    portfolio= {'Returns':port_ret, 'Risk':port_risk, 'Sharpe':sharpe_ratio}

    for i, s in enumerate(codelist): 
        portfolio[s]= [weight[i] for weight in port_weights] 

    df1= pd.DataFrame(portfolio) ##
    df1= df1[['Returns','Risk','Sharpe']+[s for s in codelist]]  ##

    max_sharpe= df1.loc[df1['Sharpe']==df1['Sharpe'].max()] ##
    min_risk= df1.loc[df1['Risk']==df1['Risk'].min()] ## 

    df1.plot.scatter(x='Risk',y='Returns',c='Sharpe',cmap='viridis',edgecolors='k',figsize=(20,10), grid=True,sharex=False) 
    plt.scatter(x=max_sharpe['Risk'],y=max_sharpe['Returns'],c='r',marker= '*',s=300)
    plt.scatter(x=min_risk['Risk'],y=min_risk['Returns'],c='r',marker= 'X',s=200)
    plt.title("Portfolio Optimizaiton",fontsize= 30) 
    plt.xlabel('Risk', fontsize= 30) 
    plt.ylabel('Expected Returns',fontsize= 30) 
    plt.savefig('static/img/MPT.png')
    
    return render_template('strategy_1.html', name='mpt',url='/static/img/MPT.png')
