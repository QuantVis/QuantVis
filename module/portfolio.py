from posixpath import split
from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint, current_app
from authlib.integrations.flask_client import OAuth
from datetime import timedelta
import os, requests
from pykrx import stock

from DB.portfolioDB import Portfolio
from DB.quantvis import Quantvis
import re
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
    
    # Quantvis DB에 있는 회사이름,종목코드 추출
    quantvis = Quantvis()
    portfolio = Portfolio()
    
    # 튜플데이터 리스트형으로 변형
    res_list=[] # 한국, 해외주식 모든 회사
    res = quantvis.select_All_table()
    for r in res:
        res_list.append(r[0])
        
    for lis in res_list :
        if re.search('^k[0-9]+',lis) != None or lis=='company_info' or lis=='daily_price':
            res_list.remove(lis)
        else:
            data['F_code'].append(lis)
    for i in data['K_code']:
        ticker_name = stock.get_market_ticker_name(i)
        data['K_company'].append(ticker_name)
        # today,exday=portfolio.get_data_now(i)
        # data['K_price'].append(today)
    for k in data['F_code']:
        ticker = quantvis.select_ticker_name(k)
        if ticker == None:
            pass
        else:
            data['F_company'].append(ticker[0])
            print(ticker[0])
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
    
    # 테스트용 데이터 변수
    data = []
    
    # DB에 저장
    for i in range(len(tickers)):
        port = Portfolio()
        port.insert_port(email,pfname,tickers[i].split('|')[0].strip(),tickers[i].split('|')[1].strip(),order_states[i],stock_cnt[i],prices[i])    
        # data.append([pfname,tickers[i].split('|')[0].strip(),tickers[i].split('|')[1].strip(),order_states[i],stock_cnt[i],prices[i]])
        # print(data[i][0])
    return redirect(url_for('portfolio.portfolio_list'))

# 포트폴리오 뷰
@port.route('/result',methods=["GET"])
def portfolio_result() :
    port = Portfolio()
    pfname = request.args.get('pfname')
    res = port.select_port(pfname)
    F_stock={'company':[],'code':[],'price':[],'stocks':[]}
    K_stock={'company':[],'code':[],'price':[],'stocks':[]}
    for rl in res:
        if re.search('[0-9]+',rl[3]) != None:
            K_stock['company'].append(rl[2])
            K_stock['code'].append(rl[3])
            K_stock['price'].append(rl[6])
            K_stock['stocks'].append(rl[5])
        else:
            F_stock['company'].append(rl[2])
            F_stock['code'].append(rl[3])
            F_stock['price'].append(rl[6])
            F_stock['stocks'].append(rl[5])
    F_total_price=0
    K_total_price=0
    for i in range(len(F_stock['price'])):
        F_total_price += float(F_stock['price'][i])*float(F_stock['stocks'][i])
    for i in range(len(K_stock['price'])):
        K_total_price += float(K_stock['price'][i])*float(K_stock['stocks'][i])
    K_total_price_fi = round(K_total_price + round(F_total_price*1254.4,2))
    F_total_price_fi = round(F_total_price + round(K_total_price/1254.4,2))
    total = sum([int(i[5]) for i in res])
    return render_template('portfolio_result.html',res=res,total=total,K_total_price_fi=K_total_price_fi,F_total_price_fi=F_total_price_fi)

@port.route('/list')
def portfolio_list() :
    port = Portfolio()
    pfname_list = port.select_port_list()
    return render_template('portfolio_list.html',pfname_list=pfname_list)