from flask import Flask, redirect, url_for, render_template, request, session, flash
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
    five, now = get_five()      # five는 2주간의 종가 가져오기(차트용), now는 현재가(텍스트용)  
    TOP5 = get_top5s()          # keys = ['kvol', 'krise', 'kfall', 'usvol', 'usrise', 'usfall']  / 미주는 티커/한국은 회사명, 현재가격, 등락률, 거래량
    
    return render_template('index.html', five=five, now = now, gauge_data=fng_gauge(), TOP5 = TOP5)

if __name__ == '__main__' :
    #get_treemap()     # 메인 트리맵 업데이트
    app.run(debug=True, port=5000, threaded=True)
    
