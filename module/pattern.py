import re
from flask import Flask, render_template, request, Response, url_for, redirect,Blueprint, session, flash ,current_app
import DB.pattern_data as pt
import io
import time
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import mpl_finance as mplfinance
#from mpl_finance import candlestick_ohlc
import numpy as np
import FinanceDataReader as fdr

matplotlib.use('Agg')

pat = Blueprint('pattern', __name__, url_prefix='/pattern')

@pat.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('pattern.html')
    else:
        code = request.form['code']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        if not(code and startdate and enddate):
            flash('정보를 모두 입력해주세요.')
            return render_template('pattern.html')
        else:
            if request.form['action'] == '패턴검색':
                return redirect(url_for('pattern.pattern_re', startdate=startdate, enddate=enddate, code=code))
            elif request.form['action'] == '차트확인':
                return render_template('pattern.html', startdate=startdate, enddate=enddate, code=code, chart=True)

@pat.route('/plot.png', methods=['GET'])
def plot_png():
    code  = request.args.get('code', None)
    startdate  = request.args.get('startdate', None)
    enddate  = request.args.get('enddate', None)
    print(startdate)
    p = pt.PatternFinder()
    p.set_stock(code)
    result = p.search(startdate, enddate)
    print(result)
    if len(result) > 0:
        fig = p.plot_pattern(list(result.keys())[0])
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@pat.route('/plotchart.png', methods=['GET'])
def plot_chart():
    code  = request.args.get('code', None)
    startdate  = request.args.get('startdate', None)
    enddate  = request.args.get('enddate', None)
    
    fig = plt.figure()
    fig.set_facecolor('w')
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
    axes = []
    axes.append(plt.subplot(gs[0]))
    axes.append(plt.subplot(gs[1], sharex=axes[0]))
    axes[0].set_title('차트')
    axes[0].get_xaxis().set_visible(False) 

    print(code)
    data = fdr.DataReader(code)
    data_ = data[startdate:enddate]
    print(code, startdate, enddate)

    x = np.arange(len(data_.index))
    ohlc = data_[['Open', 'High', 'Low', 'Close']].values
    dohlc = np.hstack((np.reshape(x, (-1, 1)), ohlc))

    # 봉차트
    mplfinance.candlestick_ohlc(axes[0], dohlc, width=0.5, colorup='r', colordown='b')

    # 거래량 차트
    axes[1].set_title('거래량')
    axes[1].bar(x, data_['Volume'], color='grey', width=0.6, align='center')
    axes[1].set_xticks(range(len(x)))
    axes[1].set_xticklabels(list(data_.index.strftime('%Y-%m-%d')), rotation=90)
    axes[1].get_yaxis().set_visible(False)

    plt.tight_layout()

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@pat.errorhandler(403)
@pat.errorhandler(404)
@pat.errorhandler(410)
@pat.errorhandler(500)
def page_not_found(e):
    return render_template('error.html')

@pat.route('/result', methods=['GET', 'POST'])
def pattern_re():
    if request.method == 'POST':
        code = request.form['code']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
    else:
        code  = request.args.get('code', None)
        startdate  = request.args.get('startdate', None)
        enddate  = request.args.get('enddate', None)
    p = pt.PatternFinder()
    p.set_stock(code)
    result = p.search(startdate, enddate)
    N = 5
    preds = p.stat_prediction(result, period=N)

    if len(preds) > 0:
        avg_ = preds.mean() * 100
        min_ = preds.min() * 100
        max_ = preds.max() * 100
        size_ = len(preds)
        print(avg_, min_, max_, size_)
        return render_template('pattern_result.html', code=code, startdate=startdate, enddate=enddate, avg=round(avg_, 2), min=round(min_, 2), max=round(max_, 2), size=size_)
    else:
        return render_template('pattern_result.html', code=code, startdate=startdate, enddate=enddate, noresult=1)