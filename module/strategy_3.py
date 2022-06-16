#플라스크, DB
from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint, current_app
from DB.strategyDB_3 import strategyyy
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
import urllib.request 
from bs4 import BeautifulSoup 
import requests

yf.pdr_override()

                        #모듈이름
strategy_3 = Blueprint('strategy_3', __name__, url_prefix='/strategy3')
@strategy_3.route('/')
def strategy_3_main(): #Function은 Blueprint 이름과 달라야함
    return render_template('strategy_3.html')


@strategy_3.route('/strategy_3_result', methods=['POST'])
def strategy_3_result(): 
    william_og,williamquartereps,williamthreeyearearnings,williamthreeyearroe,williamoneyearprofit  = strategyyy().getDB_STAT_3() 
    execute= request.form.get('execute')


    return render_template('strategy_3.html',
                           william_og_tables=[william_og.to_html(classes='data', header="true")],
                           williamquartereps_tables=[williamquartereps.to_html(classes='data', header="true")],
                           williamthreeyearearnings_tables=[williamthreeyearearnings.to_html(classes='data', header="true")],
                           williamthreeyearroe_tables=[williamthreeyearroe.to_html(classes='data', header="true")],
                           williamoneyearprofit_tables=[williamoneyearprofit.to_html(classes='data', header="true")],
                          execute= execute ) 
    
@strategy_3.route('/strategy_3_resultwinstitution', methods=['POST'])
def strategy_3_resultt(): 
    code= request.form.get('codelist') #html -> 리스트객체로 receive   
    df, total= getInstitutionvolumechange(code)
    william_og,williamquartereps,williamthreeyearearnings,williamthreeyearroe,williamoneyearprofit  = strategyyy().getDB_STAT_3() 
    execute= "execute"
    
    a= int(total['지분매입기관수'].replace(',','')) 
    b= int(total['지분매도기관수'].replace(',','')) 
    c= int(total['지분유지기관수'].replace(',','')) 
    abc= ['지분매입기관수','지분매도기관수','지분유지기관수']
    data1= [a,b,c]

    d= int(total['지분매입주수'].replace(',','')) 
    e= int(total['지분매도주수'].replace(',','')) 
    f= int(total['지분유지주수'].replace(',','')) 
    deff= ['지분매입주수','지분매도주수','지분유지주수']
    data2=[d,e,f]


    g= int(total['새지분유치기관수'].replace(',','')) 
    h= int(total['전량매도기관수'].replace(',','')) 
    k= int(total['새지분유치주수'].replace(',','')) 
    l= int(total['전량매도주수'].replace(',','')) 
    k= format(k,',')
    l= format(l,',')
    
    handchange_dict= {'새지분유치기관수':g,'전량매도기관수':h,'새지분유치주수':k,'전량매도주수':l}

    totalpercent= total['전체기관보유율'] 
    quarter= total['기준분기']
    p=getimage3(data1,abc)
    o= getimage4(data2,deff)

    return render_template('strategy_3.html',
                           william_og_tables=[william_og.to_html(classes='data', header="true")],
                           williamquartereps_tables=[williamquartereps.to_html(classes='data', header="true")],
                           williamthreeyearearnings_tables=[williamthreeyearearnings.to_html(classes='data', header="true")],
                           williamthreeyearroe_tables=[williamthreeyearroe.to_html(classes='data', header="true")],
                           williamoneyearprofit_tables=[williamoneyearprofit.to_html(classes='data', header="true")],
                          execute= execute, codelist= code,
                          url1='/static/img/strategy3_a.png',
                          url2='/static/img/strategy3_b.png',
                          handchange_dict= handchange_dict, 
                          totalpercent= totalpercent, quarter= quarter, 
                         df_tables=[df.to_html(classes='data', header="true")]
                          )  


def getimage3(data,label): 
    fig2 = plt.figure(figsize=(8,8)) ## 캔버스 생성
    fig2.set_facecolor('white') ## 캔버스 색상 하얀색
    ax = fig2.add_subplot() ## 프래임 생성
    ax.pie(x=data,labels=label,autopct=lambda p : '{:.2f}%'.format(p)) ## 파이 차트 출력
    plt.title('지분기관수변동추이', fontsize= 20)
    plt.legend() 
    plt.savefig('static/img/strategy3_a.png')

def getimage4(data,label): 
    fig2 = plt.figure(figsize=(8,8)) ## 캔버스 생성
    fig2.set_facecolor('white') ## 캔버스 색상 하얀색
    ax = fig2.add_subplot() ## 프래임 생성
    ax.pie(x=data,labels=label,autopct=lambda p : '{:.2f}%'.format(p)) ## 파이 차트 출력
    plt.title('지분주식수변동추이', fontsize= 20)
    plt.legend() 
    plt.savefig('static/img/strategy3_b.png')





def getInstitutionvolumechange(code): 
    code= code.lower() 
    codee = yf.Ticker(code)
    df= codee.institutional_holders
    df.columns = ['보유기관', '주수','발표일','분기매도물량(%)','매입가치(달러)']
    df.loc[:, "주수"] = df["주수"].map('{:,d}'.format)
    df.loc[:, "매입가치(달러)"] = df["매입가치(달러)"].map('{:,d}'.format)
    df['분기매도물량(%)'] = df['분기매도물량(%)']*100 
    
    path = "C:\webdriver/chromedriver"
    driver= webdriver.Chrome(path)
    
    url= f"https://www.nasdaq.com/market-activity/stocks/{code}/institutional-holdings" 
    driver.get(url)
    
    html = driver.page_source 
    soup= BeautifulSoup(html,'html.parser')
    quarter= soup.select('table > tbody >tr>td')[25].text #기준분기 
    month=quarter[:5]
    year= quarter[6:]
    koreanymd= f"{year}/{month}"
    instownership= soup.select('table > tbody >tr>td ')[1].text #기관보유율 
    #ACTIVE 
    increasedposition= soup.select('table > tbody >tr>td ')[7].text #지분매입 기관수
    increasedposition_sharenum= soup.select('table > tbody >tr>td ')[8].text #지분매입 주수
    decreasedposition= soup.select('table > tbody >tr>td ')[10].text #지분매도 기관수 
    decreasedposition_sharenum= soup.select('table > tbody >tr>td ')[11].text #지분매도 주수
    heldposition= soup.select('table > tbody >tr>td ')[13].text #지분유지 기관수  
    heldposition_sharenum= soup.select('table > tbody >tr>td ')[14].text #지분유지 주수  
    #newandold 
    newposition=  soup.select('table > tbody >tr>td ')[19].text #새지분유치 기관 수 
    newposition_shares= soup.select('table > tbody >tr>td ')[20].text #새지분유치 주수
    soldoutposition= soup.select('table > tbody >tr>td ')[22].text #전량매도 기관 수 
    soldoutposition_shares= soup.select('table > tbody >tr>td ')[23].text #전량매도 주수 
    soldoutposition_shares
    
    total= {'기준분기':koreanymd,'전체기관보유율':instownership ,'지분매입기관수':increasedposition, "지분매입주수":increasedposition_sharenum ,
            "지분매도기관수":decreasedposition ,"지분매도주수":decreasedposition_sharenum,"지분유지기관수":heldposition, '지분유지주수':heldposition_sharenum, 
            '새지분유치기관수':newposition, '새지분유치주수':newposition_shares, '전량매도기관수':soldoutposition, '전량매도주수':soldoutposition_shares            
            } 
    
    return df, total
    
