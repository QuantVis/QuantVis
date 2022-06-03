from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint, current_app
from authlib.integrations.flask_client import OAuth
from datetime import timedelta
import os, requests
from DB.userDB import User

#** 블루프린트로 만들 파일에서 Blueprint 모듈을 import
#** "controller.py에서 불러올 때 쓸 변수명" = Blueprint( @app 대신 쓸 이름, __name__, 적용할 url prefix)
user_login = Blueprint('user_login', __name__, url_prefix='/account')

@user_login.route('/')
def login() :    
    return render_template('login.html')

@user_login.route('/settings')
def user_settings() :
    return render_template('user_settings.html')


