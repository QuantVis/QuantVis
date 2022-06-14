from flask import Flask, redirect, url_for, render_template, request, session, flash
from authlib.integrations.flask_client import OAuth
from datetime import timedelta
import os, requests
from DB.main_data import *
from module.user_login import user_login     #** 해당 파일에서 적용한 변수명으로 가져옴
from module.strategy_1 import strategy
from module.strategy_2 import strategy_2
from module.strategy_2 import strategy_2
from module.portfolio import port
from module.pattern import pat
from module.analysis import anal
from module.chart import *

# App config
app = Flask(__name__)
app.register_blueprint(user_login)  #** 블루프린트 적용 
app.register_blueprint(strategy_1)
app.register_blueprint(strategy_2) 
#app.register_blueprint(strategy_3)
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
    # five, now = get_five()      # five는 2주간의 종가 가져오기(차트용), now는 현재가(텍스트용)  
    # TOP5 = get_top5s()          # keys = ['kvol', 'krise', 'kfall', 'usvol', 'usrise', 'usfall']  / 미주는 티커/한국은 회사명, 현재가격, 등락률, 거래량
    
    five = {'snp': {'close': [4055.75, 4155.75, 4131.25, 4099.0, 4175.25, 4107.0, 4120.5, 4158.75, 4114.0, 4016.25]}, 'dow': {'close': [32600.0, 33158.0, 32971.0, 32798.0, 33223.0, 32888.0, 32912.0, 33165.0, 32889.0, 32263.0]}, 'nasdaq': {'close': [12279.25, 12677.75, 12646.5, 12551.0, 12893.75, 12551.0, 12605.0, 12711.5, 12615.75, 12275.0]}, 'kospi': {'close': [2638.05, 2669.66, 2685.9, 2658.99, 2670.65, 2626.34, 2626.15, 2625.44, 2596.32]}, 'kosdaq': {'close': [873.97, 886.44, 893.36, 891.14, 891.51, 873.78, 874.95, 877.18, 870.94]}, 'krwx': {'close': [1266.6, 1258.89, 1251.59, 1236.17, 1241.74, 1246.95, 1240.84, 1250.53, 1254.48, 1254.58, 1256.74, 1265.81]}}
    now = {'snp': [False, 4016.25, -97.75, -2.38], 'dow': [False, 32263.0, -626.0, -1.9], 'nasdaq': [False, 12275.0, -340.75, -2.7], 'kospi': [False, 2595.61, -29.83, -1.14], 'kosdaq': [False, 871.07, -6.11, -0.7], 'krwx': [True, 1265.66, 8.92, 0.71]}  
    TOP5 = {'kvol': [['삼성전자', '63,800', '-2.15%', '22,022,851'], ['대한전선', '2,060', '-0.96%', '19,185,183'], ['현대로템', '22,800', '-0.22%', '4,904,746'], ['KG스틸', '17,050', '-1.16%', '4,200,386'], ['SK하이닉스', '103,500', '-1.90%', '3,466,716']], 'krise': [['DL', '70,800', '+5.83%', '366,606'], ['한국앤컴퍼니', '14,250', '+2.89%', '98,819'], ['한진칼', '61,500', '+2.84%', '134,833'], ['현대중공업', '138,000', '+2.60%', '261,651'], ['한국가스공사', '48,100', '+2.45%', '501,345']], 'kfall': [['PI첨단소재', '42,100', '-6.03%', '370,533'], ['에스디바이오센서', '43,300', '-5.77%', '622,808'], ['카카오뱅크', '39,150', '-4.63%', '2,965,288'], ['동국제강', '17,200', '-4.18%', '505,952'], ['화승엔터프라이즈', '15,150', '-3.81%', '168,729']], 'usvol': [['AMD', '98.80', '-3.04%', '95,298,976'], ['AAPL', '142.64', '-3.60%', '69,472,976'], ['AMZN', '116.15', '-4.15%', '67,029,840'], ['CCL', '11.73', '-9.28%', '63,378,716'], ['BAC', '34.51', '-3.85%', '49,464,072']], 'usrise': [['NXPI', '184.22', '4.04%', '10,137,529'], ['POOL', '416.39', '2.34%', '477,655'], ['DG', '237.71', '1.70%', '1,855,080'], ['TSCO', '201.65', '1.66%', '1,141,921'], ['MHK', '140.93', '1.00%', '423,644']], 'usfall': [['MRNA', '134.04', '-9.76%', '7,533,958'], ['CCL', '11.73', '-9.28%', '63,378,716'], ['NCLH', '13.76', '-9.17%', '28,212,100'], ['RCL', '49.37', '-8.29%', '6,632,431'], ['META', '184.00', '-6.43%', '23,501,580']]}
    
    return render_template('index.html', five=five, now = now, gauge_data=fng_gauge(), TOP5 = TOP5)

if __name__ == '__main__' :
    # get_treemap()     # 메인 트리맵 업데이트
    app.run(debug=True, port=5000, threaded=True)
    
