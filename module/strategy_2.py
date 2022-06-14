#플라스크, DB
from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint, current_app
from DB.strategyDB_2 import strategy_2
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
strategy_2 = Blueprint('strategy_2', __name__, url_prefix='/strategy2')
@strategy_1.route('/')
def strategy_1_main(): #Function은 Blueprint 이름과 달라야함
    return render_template('strategy_2.html')