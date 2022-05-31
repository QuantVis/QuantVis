from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import getDB

app = Flask(__name__)

@app.route('/')
def home() :
    return render_template('index.html')

@app.route('/login')
def login() :          
    return render_template('login.html')



if __name__ == '__main__' :
    app.run(debug=True, port=5000, threaded=True)
    

