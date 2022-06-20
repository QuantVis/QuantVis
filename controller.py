from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from datetime import timedelta
import os, requests
from DB.main_data import *
from module.user_login import user_login     #** 해당 파일에서 적용한 변수명으로 가져옴
from module.strategy_1 import strategy_1
from module.strategy_2 import strategy_2
from module.strategy_3 import strategy_3
from module.portfolio import port
from module.pattern import pat
from module.analysis import anal
from module.chart import *

# App config
app = Flask(__name__)
app.register_blueprint(user_login)  #** 블루프린트 적용 
app.register_blueprint(strategy_1)
app.register_blueprint(strategy_2) 
app.register_blueprint(strategy_3)
app.register_blueprint(port)
app.register_blueprint(pat)
app.register_blueprint(anal)
app.register_blueprint(chart)

# Session config
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


#@login_required     # 로그인해야만 접근가능(적절한데에 사용하기~~~)

@app.route('/')      
def home() :
    #five, now = get_five()      # five는 2주간의 종가 가져오기(차트용), now는 현재가(텍스트용)  
    #TOP5 = get_top5s()          # keys = ['kvol', 'krise', 'kfall', 'usvol', 'usrise', 'usfall']  / 미주는 티커/한국은 회사명, 현재가격, 등락률, 거래량

    five = {'snp': {'close': [4120.5, 4158.75, 4114.0, 4016.25, 3899.0, 3750.5, 3736.75, 3789.25, 3668.25, 3663.76, 3692.25]}, 'dow': {'close': [32912.0, 33165.0, 32889.0, 32263.0, 31388.0, 30527.0, 30375.0, 30661.0, 29928.0, 29806.19, 29954.0]}, 'nasdaq': {'close': [12605.0, 12711.5, 12615.75, 12275.0, 11840.0, 11296.5, 11314.25, 11593.75, 11124.75, 11130.39, 11377.25]}, 'kospi': {'close': [2626.34, 2626.15, 2625.44, 2595.87, 2504.51, 2492.97, 2447.38, 2451.41, 2440.93, 2416.77]}, 'kosdaq': {'close': [873.78, 874.95, 877.18, 869.86, 828.77, 823.58, 799.41, 802.15, 798.69, 791.89]}, 'krwx': {'close': [1250.53, 1254.48, 1254.58, 1256.74, 1264.02, 1278.28, 1291.8, 1289.48, 1278.16, 1288.18, 1291.95]}}
    now = {'snp': [True, 3692.25, 28.49, 0.78], 'dow': [True, 29954.0, 147.81, 0.5], 'nasdaq': [True, 11377.25, 246.86, 2.22], 'kospi': [False, 2416.77, -24.16, -0.99], 'kosdaq': [False, 791.89, -6.8, -0.85], 'krwx': [True, 1291.95, 3.77, 0.29]}
    TOP5 = {'kvol': [['삼성전자', '58,900', '-1.51%', '10,775,569'], ['대한전선', '1,905', '+0.79%', '4,319,206'], ['두산에너빌리티', '16,950', '-0.59%', '1,506,319'], ['HMM', '25,900', '-3.72%', '860,764'], ['팬오션', '6,740', '+1.35%', '768,191']], 'krise': [['OCI', '129,500', '+4.86%', '225,835'], ['롯데케미칼', '202,000', '+5.21%', '60,983'], ['대한유화', '146,000', '+3.18%', '13,071'], ['한국항공우주', '55,900', '+2.95%', '498,173'], ['한화에어로스페이스', '52,700', '+2.93%', '174,775']], 'kfall': [['DB하이텍', '56,200', '-4.75%', '339,271'], ['삼성엔지니어링', '20,850', '-4.36%', '485,779'], ['LX인터내셔널', '35,250', '-4.21%', '173,746'], ['포스코인터내셔널', '21,650', '-3.78%', '141,939'], ['HMM', '25,900', '-3.72%', '860,764']], 'usvol': [['AAPL', '131.56', '1.15%', '132,439,032'], ['AMD', '81.57', '-0.59%', '104,867,724'], ['AMZN', '106.22', '2.47%', '99,129,399'], ['T', '19.38', '2.22%', '97,071,478'], ['BAC', '31.92', '0.22%', '79,334,446']], 'usrise': [['NCLH', '11.43', '10.12%', '33,476,072'], ['CCL', '9.60', '9.71%', '68,307,040'], ['ENPH', '184.75', '8.94%', '3,825,536'], ['SEDG', '275.41', '8.44%', '1,997,764'], ['AAL', '12.94', '6.41%', '51,863,935']], 'usfall': [['FANG', '122.29', '-8.52%', '9,372,029'], ['COP', '93.74', '-8.47%', '24,386,422'], ['DVN', '58.02', '-8.30%', '32,196,106'], ['PXD', '221.77', '-8.17%', '9,478,203'], ['CTRA', '26.54', '-7.30%', '43,967,528']]}

    
    return render_template('index.html', five=five, now = now, gauge_data=fng_gauge(), TOP5 = TOP5)

if __name__ == '__main__' :
    #get_treemap()     # 메인 트리맵 업데이트
    app.run(debug=True, port=5000, threaded=True)
    
