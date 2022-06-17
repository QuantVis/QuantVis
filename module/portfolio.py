from posixpath import split
from flask import Flask, redirect, send_file, url_for, render_template, request, session, flash, Blueprint, current_app
from authlib.integrations.flask_client import OAuth
from datetime import timedelta
import os, requests
from pykrx import stock
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import pandas as pd
import io
import matplotlib.ticker as ticker
import mpl_finance as mplfinance
from DB.portfolioDB import Portfolio
from DB.quantvis import Quantvis
import re,time
#** 블루프린트로 만들 파일에서 Blueprint 모듈을 import
#** "controller.py에서 불러올 때 쓸 변수명" = Blueprint( @app 대신 쓸 이름, __name__, 적용할 url prefix)
port = Blueprint('portfolio', __name__, url_prefix='/portfolio')

# 포트폴리오 첫 페이지
@port.route('/')
def portfolio() :
    # 세션부여 아직 미구현
    # if session.get('email') == None:
    #     flash('로그인을 하고 접근하세요')
    #     return render_template('portfolio.html', price = price, ticker_names=ticker_names, ticker_names_F=ticker_names_F,tickers_K_list=tickers_K_list)
    #     #return render_template('login.html')
    # else:
    data = {'K_company':[],'K_code':[],'K_price':[],'F_company':[],'F_code':[],'F_price':[]}
    
    # 코스닥 코스피 종목코드
    tickers_KOSDAK_market = ['265520', '035760', '058820', '195940', '028300', '067630', '035900', '035600', '060720', '108320', '060250', '030190', '218410', '151910', '036540', '098460', '078130', '035080', '007390', '033640', '119860', '032190', '068240', '045390', '078600', '213420', '194480', '086450', '005290', '025900', '131970', '141080', '058470', '267980', '215200', '235980', '086900', '140410', '080160', '053030', '064550', '323990', '090460', '100090', '000250', '038500', '038540', '089980', '006730', '092190', '046890', '178320', '015750', '299660', '268600', '068760', '091990', '357780', '036830', '253450', '222800', '222080', '096530', '025980', '092040', '084850', '027360', '067160', '053800', '131370', '196170', '293780', '101490', '056190', '041510', '237690', '298380', '088800', '230360', '086520', '247540', '383310', '036810', '183490', '061970', '290650', '066970', '033310', '039200', '138080', '122870', '041190', '240810', '074600', '104830', '030530', '069080', '112040', '018000', '206650', '023410', '084370', '272290', '078020', '102710', '039030', '060150', '048530', '095700', '204270', '082270', '036930', '144510', '085660', '278280', '293490', '042000', '078340', '214370', '032500', '052400', '290510', '183300', '041960', '029960', '033290', '200130', '294570', '214150', '095610', '108230', '064760', '131290', '104480', '034230', '214450', '140860', '091700', '263750', '022100', '319660', '137400', '166090', '003380', '256840', '084990', '048410', '243070', '084110', '145020']
    tickers_KOSPI_market = ['282330', '138930', '001040', '079160', '000120', '097950', '005830', '000990', '000210', '375500', '114090', '078930', '006360', '007070', '294870', '267250', '011200', '105560', '002380', '016380', '030200', '033780', '003550', '034220', '051900', '373220', '032640', '011070', '066570', '051910', '079550', '006260', '010120', '001120', '035420', '005940', '010060', '178920', '005490', '010950', '034730', '011790', '001740', '006120', '302440', '326030', '402340', '361610', '096770', '285130', '017670', '000660', '064960', '069260', '035250', '010130', '011780', '073240', '000270', '024110', '002350', '251270', '006280', '005250', '004370', '001680', '047040', '042660', '003090', '069620', '006650', '001440', '003490', '192080', '001230', '026960', '006040', '014820', '000150', '241560', '034020', '336260', '032350', '023530', '004000', '004990', '005300', '011170', '204320', '138040', '008560', '009900', '006800', '003850', '003000', '006400', '028260', '207940', '032830', '018260', '028050', '009150', '005930', '010140', '016360', '029780', '000810', '000070', '004490', '068270', '004170', '031430', '019170', '055550', '003410', '112610', '002790', '090430', '020560', '010780', '005850', '012750', '036570', '111770', '003520', '000670', '007310', '271560', '001800', '316140', '000100', '139480', '020150', '030000', '185750', '013890', '035720', '323410', '377300', '192820', '120110', '021240', '192400', '284740', '259960', '039490', '003240', '028670', '047050', '003670', '103140', '086790', '352820', '000080', '036460', '071050', '000240', '015760', '009540', '161890', '161390', '047810', '008930', '128940', '009240', '020000', '105630', '014680', '018880', '009420', '051600', '052690', '180640', '000880', '088350', '009830', '272210', '012450', '000720', '005440', '086280', '042670', '064350', '012330', '010620', '069960', '017800', '011210', '004020', '329180', '005380', '001450', '057050', '008770', '241590', '004800', '298050', '298020', '093370', '081660']
    data['K_code'] = tickers_KOSPI_market + tickers_KOSDAK_market
    
    # 날짜변수 설정
    now = datetime.datetime.now()
    before_7_day = now - datetime.timedelta(days=7)
    str_now = str(now)
    str_before_7_day = str(before_7_day)
    
    # Quantvis DB에 있는 회사이름,종목코드 추출
    quantvis = Quantvis()
    
    # 튜플데이터 리스트형으로 변형
    res_list=[] # 한국, 해외주식 모든 회사
    res = quantvis.select_All_table()
    for r in res:
        res_list.append(r[0])
    
    # 국내주식 해외주식 구분    
    for lis in res_list :
        if re.search('^k[0-9]+',lis) != None or lis=='company_info' or lis=='daily_price':
            res_list.remove(lis)
        else:
            data['F_code'].append(lis)
    
    # 국내주식 회사이름, 현재주가    
    for i in data['K_code']:
        ticker_name = stock.get_market_ticker_name(i)
        data['K_company'].append(ticker_name)
        data['K_price'].append(quantvis.select_price('k'+i))
        
    
    # 해외주식 회사이름, 현재주가
    for k in data['F_code']:
        ticker = quantvis.select_ticker_name(k)
        if ticker == None:
            pass
        else:
            data['F_company'].append(ticker[0])
            data['F_price'].append(quantvis.select_price(k))
    
    #print("data['F_price'] : ",data['F_price'])
    #print("data['K_price'] : ",data['K_price'])
    
    return render_template('portfolio.html', data=data)

# 포트폴리오 데이터 입력
@port.route('/insert',methods=['POST'])
def portfolio_insert() :
    # 각 변수선언
    email = session.get('email')
    pfname = request.form['pfname']
    tickers = request.form.getlist('ticker')
    order_states = request.form.getlist('order_state')
    stock_cnt = request.form.getlist('stock_cnt')
    prices = request.form.getlist('price')
    
    none_idx=[]
    for i in range(len(tickers)):
        if tickers[i] == '': 
            none_idx.append(i)
    
    for j in none_idx:
        tickers.pop(j)
        order_states.pop(j)
        stock_cnt.pop(j)
        prices.pop(j)
    print(tickers)
    print(order_states)
    print(stock_cnt)
    print(prices)
    print(len(tickers))
    # DB에 저장
    for i in range(len(tickers)):
        port = Portfolio()
        port.insert_port(email,pfname,tickers[i].split('|')[0].strip(),tickers[i].split('|')[1].strip(),order_states[i],stock_cnt[i],prices[i])    
        
    return redirect(url_for('portfolio.portfolio_list'))

# 포트폴리오 result
@port.route('/result',methods=["GET"])
def portfolio_result() :
    port = Portfolio()
    # 사용자가 클릭한 포트폴리오 이름 가져오기
    pfname = request.args.get('pfname')
    
    # 포트폴리오 이름에 해당되는 데이터 DB에서 꺼내오기
    res = port.select_port(pfname)
    
    # 한국주식 해외주식 변수 초기화
    F_stock={'company':[],'code':[],'price':[],'stocks':[],'change':[],'status':[]}
    K_stock={'company':[],'code':[],'price':[],'stocks':[],'change':[],'status':[]}
    
    # 한국, 해외주식 데이터 변수에 저장
    for rl in res:
        if re.search('[0-9]+',rl[3]) != None:
            K_stock['company'].append(rl[2])
            K_stock['code'].append(rl[3])
            K_stock['status'].append(rl[4])
            K_stock['price'].append(rl[6])
            K_stock['stocks'].append(rl[5])
        else:
            F_stock['company'].append(rl[2])
            F_stock['code'].append(rl[3])
            F_stock['status'].append(rl[4])
            F_stock['price'].append(rl[6])
            F_stock['stocks'].append(rl[5])
    now = datetime.datetime.now()
    before_3_day = now - datetime.timedelta(days=3)
    before_30_day = now - datetime.timedelta(days=30)
    str_now = str(now)
    str_before_30_day = str(before_30_day)
        
            
    # 전체 total 가격            
    F_total_price=0
    K_total_price=0
    for i in range(len(F_stock['price'])):
        if F_stock['status'][i] == '매수':
            F_total_price += float(F_stock['price'][i])*float(F_stock['stocks'][i])
        elif F_stock['status'][i] == '매도':
            F_total_price -= float(F_stock['price'][i])*float(F_stock['stocks'][i])
    for i in range(len(K_stock['price'])):
        if K_stock['status'][i] == '매수':
            K_total_price += float(K_stock['price'][i])*float(K_stock['stocks'][i])
        elif K_stock['status'][i] == '매도':
            K_total_price -= float(K_stock['price'][i])*float(K_stock['stocks'][i]) 
        elif K_stock['status'][i] == '예약':
            K_total_price += 0
    
    dalwon = yf.download(['USDKRW=X'],start=before_3_day,end=now)
    exchng = round(dalwon['Adj Close'][-1],1)
    K_total_price_fi = round(K_total_price + round(F_total_price*exchng,2))
    F_total_price_fi = round(F_total_price + round(K_total_price/exchng,2))
    total = sum([int(i[5]) for i in res])
    
    def get_chart(df_data,company):
        #-------------------------------------------------------------------------------------------#
        # 그래프구역
        fig = plt.figure(figsize=(20,5))
        top_axes = plt.subplot2grid((4,4), (0,0), rowspan=2, colspan=4,)
        mid_axes = plt.subplot2grid((4,4), (2,0), rowspan=1, colspan=4, sharex=top_axes)
        bottom_axes = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4, sharex=top_axes)
        mid_axes.get_yaxis().get_major_formatter().set_scientific(False) # 거래량 값 그대로 표현
        bottom_axes.get_yaxis().get_major_formatter().set_scientific(False) # 거래량 값 그대로 표현
        #-------------------------------------------------------------------------------------------#

        # 인덱스 설정
        idx = df_data.index.astype('str')

        # 이동평균선 그리기
        top_axes.plot(idx, df_data['MA3'], label='MA3', linewidth=0.7)
        top_axes.plot(idx, df_data['MA5'], label='MA5', linewidth=0.7)
        top_axes.plot(idx, df_data['MA10'], label='MA10', linewidth=0.7)
        mid_axes.plot(idx, df_data['DD'], label='DD', color='brown', linewidth=1)
        mid_axes.plot(idx, df_data['MDD'], label='MDD', color='red', linewidth=1)
        #mid_axes.plot(idx, df_data['전일기준등락율'], label='전일대비등락율', color='green', linewidth=1)

        # 캔들차트 그리기
        mplfinance.candlestick2_ohlc(top_axes, df_data['Open'], df_data['High'], df_data['Low'], df_data['Close'], width=0.5, colorup='r', colordown='b')
        
        #------------------------------------------------------------------------------#
        # 색깔 구분을 위한 함수
        color_fuc = lambda x : 'r' if x >= 0 else 'b'
        # kospi 거래량의 차이 
        df_data['Volume'].diff().fillna(0) ## 첫 행은 값이 Nan이므로 0으로 채워줌
        # 색깔 구분을 위한 함수를 apply 시켜 Red와 Blue를 구분한다.
        color_df = df_data['Volume'].diff().fillna(0).apply(color_fuc)

        # 구분된 값을 list 형태로 만들어준다.
        color_list = list(color_df)

        # 거래량 그래프
        bottom_axes.bar(idx, df_data['Volume'], width=0.5, 
                        align='center',
                        color=color_list)

        # 그래프 title 지정
        top_axes.set_title(company, fontsize=22)
        # X축 티커 숫자 20개로 제한
        top_axes.xaxis.set_major_locator(ticker.MaxNLocator(10))
        top_axes.legend(['MA3','MA5','MA10'])
        mid_axes.legend(['DD','MDD'])
        bottom_axes.legend(['상승거래량','하락거래량'])
        # X축 라벨 지정
        bottom_axes.set_xlabel('Date', fontsize=15)
        mid_axes.set_xlabel('Date', fontsize=15)
    
    # API 데이터 불러오기(전일대비 등락률,차트) 
    change = []
    chart_idx = 1
    for stock_dict in [K_stock,F_stock]:
        
        if re.search('[0-9]+',str(stock_dict['code'])) != None:
            # 한국주식
            
            print(stock_dict['code'])
            for i in range(len(stock_dict['code'])):
                df_data_K = pdr.get_data_yahoo(stock_dict['code'][i]+'.KS',before_30_day,now)
                df_data_K.drop('Adj Close',axis=1,inplace=True)
                df_data_K['전일종가'] = df_data_K['Close'].shift()    # default 1 : 하루(1일) 차분, 아래로 내리기
                df_data_K['전일대비변동가격'] = df_data_K['Close'] - df_data_K['전일종가']
                df_data_K['전일기준등락율'] = ((df_data_K['Close'] - df_data_K['전일종가'])/df_data_K['전일종가']) * 100
                print('ticker',stock_dict['code'][i])
                #print(round(df_data['전일기준등락율'][-1],2))
                change.append(round(df_data_K['전일기준등락율'][-1],2))
                K_stock['change'].append(round(df_data_K['전일기준등락율'][-1],2))
                df_data_K['MA3'] = df_data_K['Close'].rolling(3).mean()
                df_data_K['MA5'] = df_data_K['Close'].rolling(5).mean()
                df_data_K['MA10'] = df_data_K['Close'].rolling(10).mean()
                window = 20
                max_in_window = df_data_K['Close'].rolling(window,min_periods=1).max()
                df_data_K['DD']=((df_data_K['Close']/max_in_window)-1)*100
                df_data_K['MDD'] = df_data_K['DD'].rolling(window,min_periods=1).min()
                #print(df_data_K['MDD'])
                print(K_stock['company'][i])
                get_chart(df_data=df_data_K,company=K_stock['company'][i])
                print('chart_idx : ',chart_idx)
                plt.savefig(f'static/img/chart_{chart_idx}.png')
                chart_idx += 1
                
        else: 
            # 해외주식
            print(str(stock_dict['code']).upper())
            for i in range(len(stock_dict['code'])):
                df_data_F = pdr.get_data_yahoo(stock_dict['code'][i],before_30_day,now)
                df_data_F.drop('Adj Close',axis=1,inplace=True)
                df_data_F['전일종가'] = df_data_F['Close'].shift()    # default 1 : 하루(1일) 차분, 아래로 내리기
                df_data_F['전일대비변동가격'] = df_data_F['Close'] - df_data_F['전일종가']
                df_data_F['전일기준등락율'] = ((df_data_F['Close'] - df_data_F['전일종가'])/df_data_F['전일종가']) * 100
                print('ticker',stock_dict['code'][i])
                #print(round(df_data['전일기준등락율'][-1],2))
                change.append(round(df_data_F['전일기준등락율'][-1],2))
                F_stock['change'].append(round(df_data_F['전일기준등락율'][-1],2))
                df_data_F['MA3'] = df_data_F['Close'].rolling(3).mean()
                df_data_F['MA5'] = df_data_F['Close'].rolling(5).mean()
                df_data_F['MA10'] = df_data_F['Close'].rolling(10).mean()
                window = 20
                max_in_window = df_data_F['Close'].rolling(window,min_periods=1).max()
                df_data_F['DD']=((df_data_F['Close']/max_in_window)-1)*100
                df_data_F['MDD'] = df_data_F['DD'].rolling(window,min_periods=1).min()
                #print(df_data_F['MDD'])
                print(F_stock['company'][i])
                get_chart(df_data=df_data_F,company=F_stock['company'][i])
                print('chart_idx : ',chart_idx)
                plt.savefig(f'static/img/chart_{chart_idx}.png')
                chart_idx += 1
    print('chart_idx_final : ',chart_idx)
    
    # 등락률 total 가격
    F_total_change_price = 0
    K_total_change_price = 0
    print(F_stock)
    for i in range(len(F_stock['price'])):
        if F_stock['status'][i] == '매수':
            F_total_change_price += float(F_stock['price'][i])*float(F_stock['stocks'][i])*float(F_stock['change'][i])
        elif F_stock['status'][i] == '매도':
            F_total_change_price -= float(F_stock['price'][i])*float(F_stock['stocks'][i])*float(F_stock['change'][i])
    for i in range(len(K_stock['price'])):
        if K_stock['status'][i] == '매수':
            K_total_change_price += float(K_stock['price'][i])*float(K_stock['stocks'][i])*float(K_stock['change'][i])
        elif K_stock['status'][i] == '매도':
            K_total_change_price -= float(K_stock['price'][i])*float(K_stock['stocks'][i])*float(K_stock['change'][i])
    K_total_change_price_fi = round(K_total_change_price + round(F_total_change_price*exchng,2))
    F_total_change_price_fi = round(F_total_change_price + round(K_total_change_price/exchng,2))
    
    # 차트
    # 종목별 최근 15일 기준 MDD 지수, 일일 등락율
    return render_template('portfolio_result.html',
                           res=res,
                           total=total,
                           K_total_price_fi=K_total_price_fi,
                           F_total_price_fi=F_total_price_fi,
                           change=change,
                           K_total_change_price_fi=K_total_change_price_fi,
                           F_total_change_price_fi=F_total_change_price_fi,
                           chart_idx=chart_idx)

@port.route('/list')
def portfolio_list() :
    port = Portfolio()
    pfname_list = port.select_port_list()
    return render_template('portfolio_list.html',pfname_list=pfname_list)