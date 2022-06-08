from flask import Flask, redirect, url_for, render_template, request, session, flash
from authlib.integrations.flask_client import OAuth
from datetime import timedelta
import os, requests
from module.user_login import user_login     #** 해당 파일에서 적용한 변수명으로 가져옴

# App config
app = Flask(__name__)
app.register_blueprint(user_login)  #** 블루프린트 적용 

# Session config
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


@app.route('/')
def home() :
    return render_template('index.html')


if __name__ == '__main__' :
    app.run(debug=True, port=5000, threaded=True)
    
