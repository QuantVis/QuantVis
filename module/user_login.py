from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint, current_app
from authlib.integrations.flask_client import OAuth
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash        # 비번확인할때는 똑같이 generate_password_hash를 적용해서 비교하기
import os, requests, re
from DB.userDB import User

user_login = Blueprint('user_login', __name__, url_prefix='/account')


# current_app.config['SESSION_COOKIE_NAME'] = 'google-login-session'

# oAuth Setup
oauth = OAuth(current_app)
google = oauth.register(
    name='google',
    client_id="473052259458-ln8c74jlp47gb5g5dl7979c529emka0k.apps.googleusercontent.com",
    client_secret="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",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    # This is only needed if using openId to fetch user info
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'},
)

kakao = dict(
    name='kakao',
    CLIENT_ID='032f2f02eb98da0067159843349b1fda',
    CLIENT_SECRET='TsapaMYodHxqukwMYHXnfi0BqufU1b2D',
    REDIRECT_URI='http://127.0.0.1:5000/account/kakao_login/callback',
    SIGNOUT_REDIRECT_URI='http://127.0.0.1:5000/account/logout'
)


@user_login.route('/')
def login():
    return render_template('user_login.html')

@user_login.route('/local_login', methods=['POST'])
def local_login() :
        email = request.form.get('email')
        user_pwd = request.form.get('password')
        if not (email and user_pwd):
            flash('정보를 모두 입력해주세요!')
            return render_template('user_login.html')
        else :
            userdb = User()
            userdict = userdb.get_user_info(user_email = email.strip())
            if userdict == None :
                flash('계정 정보가 없습니다')
                return render_template('user_login.html')
            if check_password_hash(userdict['password'], user_pwd) == False :
                flash('비밀번호가 일치하지 않습니다')
                return render_template('user_login.html')
            else :
                session['email'] = userdict['email']
                session['nick'] = userdict['nick']
                if userdict['nick'] == '' : return redirect('settings')
                return redirect('/')


@user_login.route('/signup', methods=['GET', 'POST'])   # 로컬 회원가입
def signup():
    if request.method == 'GET':
        return render_template('user_signup.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password1')
        password_2 = request.form.get('password2')
        
        # DB 입력
        userdb = User()
        if userdb.get_user_info(user_email = email) != None :
            flash(email+'은 이미 가입된 계정입니다')
            return render_template('user_signup.html')
        
        if not (email and password and password_2):
            flash('정보를 모두 입력해주세요!')
            return render_template('user_signup.html')
        
        if password != password_2:
            flash('비밀번호가 일치하지 않습니다')
            return render_template('user_signup.html')
        
        else:
            res = userdb.create_user_info(user_id=email.strip(), email=email.strip(), method='local',password=generate_password_hash(password))
            if res == 1 : 
                session['email'] = email
                return redirect('settings')
            else : 
                return redirect('/', error = 'DB에러')



@user_login.route('/settings', methods=['GET', 'POST'])
def user_settings():    
    if request.method == 'GET' :
        if not session : return redirect('/account/')
        userdb = User()
        if session['email'] :
            userdict = userdb.get_user_info(user_email=session['email'])   
        elif session['id'] :
            userdict = userdb.get_user_info(user_id=session['id'])
        return render_template('user_settings.html', userdict=userdict)
    else :
        userdb = User()
        if session['email'] : userdict = userdb.get_user_info(user_email = session['email'])
        elif session['id'] :  userdict = userdb.get_user_info(user_id = session['id'])
        email = request.form.get('email')
        nick = request.form.get('nick')
        password = request.form.get('password1')
        password_2 = request.form.get('password2')
        
        if userdict['method'] == 'local' :
            if not nick :
                flash('닉네임은 필수 입력 요소입니다')
                return render_template('user_settings.html', userdict=userdict)
            if userdb.nick_check(nick) != None and userdb.nick_check(nick)[0] != userdict['id'] :
                flash('중복되는 닉네임입니다')
                return render_template('user_settings.html', userdict=userdict)
            
            if password or password_2 :
                if password != password_2:
                    flash('비밀번호가 일치하지 않습니다')
                    return render_template('user_settings.html', userdict=userdict)
                else : 
                    userdb.set_change1(email=email.strip(), nick=nick.strip(), password=generate_password_hash(password))
                    flash('정보 변경이 완료되었습니다')
                    return redirect('settings')
            else :
                userdb.set_change1(email=email.strip(), nick=nick.strip())
                flash('정보 변경이 완료되었습니다')
                session['email'] = email
                session['nick'] = nick
                return redirect('settings')                    
        
        else :
            if (session['email'] and (not nick)) or (session['id'] and (not email)) :
                flash('이메일과 닉네임은 필수 입력 요소입니다')
                return render_template('user_settings.html', userdict=userdict)
            else :                
                userdb.set_change2(user_id = userdict['id'], nick = nick.strip(), email = email)
                flash('정보 변경이 완료되었습니다')
                session['email'] = email
                session['nick'] = nick
                return redirect('settings')
    
@user_login.route('/find_pw', methods=['GET', 'POST'])
def find_pw() :
    if request.method == 'GET' :
        return render_template('user_findpw.html')
    else :
        userdb = User()
        email = request.form.get('email').strip()
        nick = request.form.get('nick').strip()
        if userdb.find_pw(email, nick) :
            session['email'] = email
            return redirect('settings')
        else :
            flash('사용자 정보를 찾을 수 없습니다')
            return render_template('user_findpw.html')
        


##################### 소셜 로그인 #####################

@user_login.route('/google_login')
def google_login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('user_login.google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@user_login.route('/google_login/callback')
def google_callback():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()         # 유저정보 응답값 수신

    # DB 작업
    userdb = User()
    if userdb.get_user_info(user_email = user_info['email']) != None :    # 이미 가입한 경우
        userdict = userdb.get_user_info(user_email = user_info['email'])
        session['email'] = userdict['email']
        session['nick'] = userdict['nick']
        return redirect('/')
    else:   # 첫 로그인
        userdb.create_user_info(user_id=user_info['id'], email=user_info['email'], method='google')
        session['email'] = user_info['email']
        session['id'] = user_info['id']
        return redirect("/account/settings")
    


@user_login.route('/kakao_login')
def kakao_login():
    kakao_oauth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={kakao['CLIENT_ID']}&redirect_uri={kakao['REDIRECT_URI']}&response_type=code"
    return redirect(kakao_oauth_url)


@user_login.route('/kakao_login/callback')
def kakao_callback():
    code = request.args['code']     # # callback 뒤에 붙어오는 request token
    auth_info = requests.post(
        url="https://kauth.kakao.com/oauth/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        },
        data={
            "grant_type": "authorization_code",
            "client_id": kakao['CLIENT_ID'],
            "client_secret": kakao['CLIENT_SECRET'],
            "redirect_uri": kakao['REDIRECT_URI'],
            "code": code,
        }).json()

    if 'error' in auth_info:
        return redirect('/')  # 오류발생할때 보낼 페이지로 이동시키기!!!!!!

    user_info = requests.post(
        url="https://kapi.kakao.com/v2/user/me",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
            "Authorization": "Bearer " + auth_info['access_token'],
            # "property_keys":'["kakao_account.profile_image_url"]'
        }, data={}).json()

    profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={
                                   "Authorization": f"Bearer {auth_info['access_token']}"})

    # DB 입력
    userdb = User()
    if userdb.get_user_info(user_email = user_info['kakao_account']['email']) != None :  # 이미 가입한 경우
        userdict = userdb.get_user_info(user_id = user_info['id'])
        session['email'] = userdict['email']
        session['nick'] = userdict['nick']
        return redirect("/")
    
    else :  # 첫 로그인
        if user_info['kakao_account']['has_email']:  # 이메일 동의를 한 경우
            userdb.create_user_info(user_id=user_info['id'], email=user_info['kakao_account']['email'], method='kakao')
            session['email'] = user_info['kakao_account']['email']
            session['id'] = user_info['id'] 
        else:  # 이메일 없는경우(이메일 미동의)
            userdb.create_user_info(user_id=user_info['id'], method='kakao')
            session['id'] = user_info['id']
        return redirect("/account/settings")


@user_login.route('/logout')
def logout():
    session.clear()
    return redirect('/')
