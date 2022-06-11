import yfinance as yf
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os, time, requests, fear_and_greed, math
from shutil import move

def get_five(): 
    
    today = date.today()
    before = today - timedelta(weeks=2)
    before = datetime.strptime(str(before), '%Y-%m-%d')
    five = {}
    now = {}

    snp = yf.download("ES=F", start = before)
    five['snp'] = {'close': [round(i,2) for i in snp['Close']]}
    
    dow = yf.download("YM=F", start = before)
    five['dow'] = {'close': [round(i,2) for i in dow['Close']]}
    
    nasdaq = yf.download("NQ=F", start = before)
    five['nasdaq'] = {'close': [round(i,2) for i in nasdaq['Close']]}
    
    kospi = yf.download("^KS11", start = before)
    five['kospi'] = {'close': [round(i,2) for i in kospi['Close']]}
    
    kosdaq = yf.download("^KQ11", start = before)
    five['kosdaq'] = {'close': [round(i,2) for i in kosdaq['Close']]} 
    
    krw_x = yf.download("KRW=X", start=before)  
    five['krwx'] = {'close': [round(i,2) for i in krw_x['Close']]} 

    for code in ['snp', 'dow', 'nasdaq', 'kospi', 'kosdaq', 'krwx'] :
        flag = True
        differ = five[code]['close'][-1] - five[code]['close'][-2]
        percent = (differ / five[code]['close'][-2]) * 100
        if differ < 0 : flag = False
        now[code] = [ flag, round(five[code]['close'][-1],2), round(differ,2), round(percent,2) ]
    
    return five, now


def main_with_start() :
    pass

def get_treemap() :

    op = Options()
    op.add_experimental_option('prefs', {'download.default_directory' : 'C:\\Users\\sein1\\CLASS\\0_FINAL PROJECT\\QuantVis\\static\\img'})

    path = "c:\\webdriver\\chromedriver"
    driver = webdriver.Chrome(path, options=op)
    today = date.today()
    imgpath = 'C:\\Users\\sein1\\CLASS\\0_FINAL PROJECT\\QuantVis\\static\\img'

    for cat in ['ALL','KOSPI','KOSDAQ'] :
        url = f"https://invest.zum.com/domestic?cm=invest_main_gnb&category={cat}"
        driver.get(url)
        #if cat == 'ALL' : driver.find_element_by_css_selector('#app > div.invest-event-popup > div > div > a:nth-child(1)').click()
        driver.find_element_by_css_selector('button.ic_txt.share').click()
        time.sleep(1)
        file_oldname = os.path.join(imgpath+f"\\줌투자 증시맵-{today.year}. {today.month}. {today.day}..png")
        file_newname_newfile = os.path.join(imgpath + f"\\{cat}_tree.png")
        move(file_oldname, file_newname_newfile)
        driver.switch_to.default_content()

    for cat in ['dow','nasdaq'] :
        url = f"https://invest.zum.com/global?cm=invest_main_gnb&category={cat}"
        driver.get(url)
        driver.find_element_by_css_selector('button.ic_txt.share').click()
        time.sleep(1)
        file_oldname = os.path.join(imgpath+f"\\줌투자 증시맵-{today.year}. {today.month}. {today.day}..png")
        file_newname_newfile = os.path.join(imgpath + f"\\{cat}_tree.png")
        move(file_oldname, file_newname_newfile)
        driver.switch_to.default_content()
        
def fng_gauge() :
    fng = fear_and_greed.get()
    gauge_data = {'value' : math.trunc(fng.value), 'desc' : fng.description.upper(), \
                'updated' : datetime.strftime(fng.last_update, 'Last updated : %b %d at %H:%m %Z')}
    
    return gauge_data

def get_top5s() :
    path = "c:\\webdriver\\chromedriver"
    driver = webdriver.Chrome(path)
    
    TOP5 = {}
    names = ['kvol', 'krise', 'kfall', 'usvol', 'usrise', 'usfall']
    
    # 한국 top5 가져오기 - 거래량 / 상승 / 하락
    urls = ['https://finance.naver.com/sise/entryJongmok.naver?order=acc_quant&amp;isRightDirection=true',\
            'https://finance.naver.com/sise/entryJongmok.naver?order=change_rate&isRightDirection=true',\
            'https://finance.naver.com/sise/entryJongmok.naver?order=change_rate&isRightDirection=false' ]


    # 종목명 현재가 등락률 거래량
    j = 0
    for url in urls :
        driver.get(url)
        html = driver.page_source
        html = BeautifulSoup(html, 'html.parser')
        lines = html.select('body > div > table.type_1 > tbody > tr > td')[1:]
        data = []
        for i in range(0,35, 7) :
            data.append([lines[i].text.strip(), lines[i+1].text.strip(),lines[i+3].text.strip(),lines[i+4].text.strip()])
        TOP5[names[j]] = data
        j+=1
            
    # 미국 top5 가져오기 - 거래량 / 상승 / 하락

    urls = ['https://finviz.com/screener.ashx?v=111&f=idx_sp500&o=-volume',\
            'https://finviz.com/screener.ashx?v=111&f=idx_sp500&o=-change',\
            'https://finviz.com/screener.ashx?v=111&f=idx_sp500&o=change']    
    
    for url in urls :
        driver.get(url)
        html = driver.page_source
        html = BeautifulSoup(html, 'html.parser')
        lines = html.select('#screener-views-table > tbody > tr:nth-child(4) > td > table > tbody > tr > td')[11:]
        data = []
        for i in range(0,55,11) :
            data.append([lines[i+1].text.strip(), lines[i+8].text.strip(),lines[i+9].text.strip(),lines[i+10].text.strip()])
        TOP5[names[j]] = data
        j+=1
        
    return TOP5
    
    
 

