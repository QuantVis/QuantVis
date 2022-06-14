from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint, current_app
from authlib.integrations.flask_client import OAuth
from datetime import timedelta
import os, requests
from DB.getDB import getDB, getName, getUSDB

chart = Blueprint('chart', __name__, url_prefix='/chart')

@chart.route('/')
def getChart() :
    # 기본을 삼성으로
    data = getDB('005930')
    a, b, c, d, e, f, ma130, macd, signal, macdhist, fast_k, slow_d, company, insight = data.GetStockData()
    # a-date, b-low, c-open, d-close, e-high, f-volume  
    return render_template('chart.html', a = a, b = b, c = c, d = d, e = e,
                           f = f, macd=macd,signal= signal, macdhist=macdhist, ma130=ma130,
                           company = company, fastk = fast_k, slowd = slow_d, insight= insight)

@chart.route('/search', methods=(['GET']))
def search():
    search = request.args.get('stockName')
    cls1 = getName(search)
    stock_code = cls1.GetStockName()
    try:
        if len(stock_code) >= 1:
            if search in stock_code[0]:
                cls2 = getDB(stock_code[0][1])
                a, b, c, d, e, f, ma130, macd, signal, macdhist, fast_k, slow_d, company, insight = cls2.GetStockData()
                return render_template('chart.html', a = a, b = b, c = c, d = d, e = e,
                            f = f, macd=macd,signal= signal, macdhist=macdhist, ma130=ma130,
                            company = company, fastk = fast_k, slowd = slow_d, insight= insight)
        else:
            stock_code = search
            cls2 = getDB(search)
            a, b, c, d, e, f, ma130, macd, signal, macdhist, fast_k, slow_d, company, insight = cls2.GetStockData()
    except:
        return render_template('charterror.html')
        # 잘못 검색하셨습니다로 이동
    return render_template('chart.html', a = a, b = b, c = c, d = d, e = e,
                                f = f, macd=macd,signal= signal, macdhist=macdhist, ma130=ma130,
                                company = company, fastk = fast_k, slowd = slow_d, insight= insight)

# # 미국주식 -----------------------------------------------------------------------------------------
@chart.route('/chartA')
def getChartA() :
    # 기본을 에플로
    data = getUSDB('AAPL')
    a, b, c, d, e, f, ma130, macd, signal, macdhist, fast_k, slow_d, company, insight = data.GetUSStockData()
    # a-date, b-low, c-open, d-close, e-high, f-volume  
    return render_template('chartA.html', a = a, b = b, c = c, d = d, e = e,
                           f = f, macd=macd,signal= signal, macdhist=macdhist, ma130=ma130,
                           company = company, fastk = fast_k, slowd = slow_d, insight= insight)

@chart.route('/searchA', methods=(['GET']))
def searchA():
    search = request.args.get('stockName')
    cls1 = getName(search)
    stock_code = cls1.GetStockName()
    try:
        if len(stock_code) >= 1:
            if search in stock_code[0]:
                cls2 = getUSDB(stock_code[0][1])
                a, b, c, d, e, f, ma130, macd, signal, macdhist, fast_k, slow_d, company, insight = cls2.GetUSStockData()
                return render_template('chartA.html', a = a, b = b, c = c, d = d, e = e,
                            f = f, macd=macd,signal= signal, macdhist=macdhist, ma130=ma130,
                            company = company, fastk = fast_k, slowd = slow_d, insight= insight)
        else:
            stock_code = search
            cls2 = getUSDB(search)
            a, b, c, d, e, f, ma130, macd, signal, macdhist, fast_k, slow_d, company, insight = cls2.GetUSStockData()
    except:
        return render_template('charterror.html')
                # 잘못 검색하셨습니다로 이동
    return render_template('chartA.html', a = a, b = b, c = c, d = d, e = e,
                            f = f, macd=macd,signal= signal, macdhist=macdhist, ma130=ma130,
                            company = company, fastk = fast_k, slowd = slow_d, insight= insight)