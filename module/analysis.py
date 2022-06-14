import re
from flask import Flask, render_template, request, Response, url_for, redirect,Blueprint, session, flash ,current_app, send_file
import DB.analysis_data as al
import io
import time
import os
from sklearn import svm
from sklearn.svm import SVR
import numpy as np
import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import pymysql
import itertools
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

matplotlib.use('Agg')

anal = Blueprint('analysis', __name__, url_prefix='/analysis')

@anal.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('analysis.html')
    else:
        code = request.form['code']
        startdate = request.form['startdate']
        if not (code and startdate):
            flash('정보를 모두 입력해주세요.')
            return render_template('analysis.html')
        if request.form['action'] == '분석':
            return redirect(url_for('analysis.result', code = code, startdate=startdate))
@anal.route('/plot_png', methods=['GET'])        
def plot():
    startdate = request.args.get('startdate', None)
    code = request.args.get('code', None)
    s = al.svm_al(startdate)
    data = s.close_data(code)
    close = data['Close'].values
    
    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(16,8))
    plt.title('Stock Price Comparison')
        
    days = []
    j = 1
    for j in range(len(data)):
        days.append([int(j+1)])
        j += 1
            
    lin_svr = SVR(kernel='linear', C=1000)
    lin_svr.fit(days, close)

    poly_svr = SVR(kernel='poly', C=1000, degree=2)
    poly_svr.fit(days, close)

    rbf_svr = SVR(kernel='rbf', C=1000, gamma=0.05)
    rbf_svr.fit(days, close)
        
    rbf_model = []
    lin_model = []
    poly_model = []
    for i in range(len(close)):
        rbf_model.append(rbf_svr.predict([[i]]))
        lin_model.append(lin_svr.predict([[i]]))
        poly_model.append(poly_svr.predict([[i]]))
        
    plt.scatter(days,close,marker='o',c='blue')    
    plt.plot(rbf_model,'red')
    plt.plot(lin_model,'tomato')
    plt.plot(poly_model,'green')
    plt.xlabel('date', fontsize=14)
    plt.ylabel('stock', fontsize=14)
    plt.legend(['data','rbf','lin','poly'])
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')

    
@anal.errorhandler(403)
@anal.errorhandler(404)
@anal.errorhandler(410)
@anal.errorhandler(500)
def page_not_found(e):
    return render_template('error.html')    
        
@anal.route('/result', methods=['GET','POST'])
def result():
    if request.method == 'POST':
        code = request.form['code']
        startdate = request.form['startdate']
    else:
        code = request.args.get('code', None)
        startdate = request.args.get('startdate', None)
    s = al.svm_al(startdate)
    s.close_data(code)
    dpc = s.dpc()
    x = datetime.today().strftime('%Y-%m-%d')
    min_ = min(dpc) 
    max_ = max(dpc)
    today_ = dpc[len(dpc)-1]
    
    if not(code and startdate):
        return render_template('analysis_result.html', noresult=1)
    else: 
        return render_template('analysis_result.html', code=code, startdate=startdate, min=round(min_,2), max=round(max_,2), today=round(today_,2), day=x)