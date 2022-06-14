#플라스크, DB
from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint, current_app
from DB.strategyDB_3 import strategy_3
##백엔드
from pandas_datareader import data as pdr 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import yfinance as yf 
import pandas as pd
import pymysql
import re
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import datapackage
import pandas as pd
import math
import numpy as np 

yf.pdr_override()

                        #모듈이름
strategy_3 = Blueprint('strategy_3', __name__, url_prefix='/strategy3')
@strategy_3.route('/')
def strategy_3_main(): #Function은 Blueprint 이름과 달라야함
    return render_template('strategy_3.html')


@strategy_3.route('/strategy_3_result', methods=['POST'])
def strategy_3_result(): 
    
    return render_template('strategy_3.html'
                    )
