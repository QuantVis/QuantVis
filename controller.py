from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import getDB

app = Flask(__name__)
print(__name__)

@app.route('/')
def home() :
    return render_template('index.html')

@app.route('/login')
def login() :          
    return render_template('login.html')

@app.route('/chart')
def chart() :
    a = getDB.getDB('005930', 20210523)
    b = a.GetStock()
    col = []
    for i in range(0, len(b)):
        close = b['close'][i]
        open = b['open'][i]
        date = b['date'][i].strftime('%y%m%d')
        col.append([b['low'][i], b['open'][i], b['close'][i], b['high'][i]])
    
    return render_template('chart.html', col=col, len=len(date))

if __name__ == '__main__' :
    app.run(debug=True, port=5000, threaded=True)
    




# app.permanent_session_lifetime = timedelta(minutes = 30)    # 시간만큼 세션값 유지

# url_for() : 함수명을 넣으면 해당 route가 가진 url주소를 가져옴, 인자값 전달가능

# @app.route('/login', methods=['POST','GET'])
# def login() :
#     if request.method == 'POST' :
#         session.permanent = True
#         user = request.form['nm']       # form값이 딕셔너리 형태로 들어옴 
#                                         # post 요청이 오면 form의 name=nm인 값을 user에 저장
#         session['user'] = user      # 세션에 유저이름을 저장하는 방법~     
#         flash('Login Successful!')    
#         return redirect(url_for('user')) # user함수로 이동
#     else : 
#         if 'user' in session :
#             flash('Already Logged In!') 
#             return redirect(url_for('user'))    # 세션에 값이 있으면 user화면으로
#         return render_template('login.html')    # 세션에 값이 없으면 로그인 화면으로

# @app.route('/user')
# def user() :
#     if 'user' in session :
#         user = session['user']
#         return render_template('user.html', user=user)
#     else : 
#         flash('You are not Logged In!') 
#         return redirect(url_for('login'))
    
# @app.route('/logout')
# def logout() :
#     flash(f'You have been logged out!', 'info')  # message flash
#     session.pop('user', None)           # 세션에서 삭제
#     return redirect(url_for('login'))

