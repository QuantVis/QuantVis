import imp
from unittest import result
import pymysql
from flask_login import UserMixin
import urllib
from urllib.request import urlopen

class Portfolio():  
    # config         
    def __init__(self):
        self.config = {
                'host':'127.0.0.1',
                'user':'quantvis',
                'password':'quantvis',
                'database':'quantvis_portfolio',
                'port':3306,
                'charset':'utf8',
                'use_unicode':True
            }   
    
    # 포트폴리오 DB에 insert
    def insert_port(self, email, pfname, ticker_name, ticker_code, order_state, stock_cnt, price):
        print(f'select:{pfname}')
        print(f'email:{email}')
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            sql = f"INSERT INTO portfolio (email,pfname,ticker_name,ticker_code,order_state,stock_cnt,price) VALUES ('{email}','{pfname}','{ticker_name}','{ticker_code}','{order_state}','{stock_cnt}','{price}')"
            result = cursor.execute(sql)                
            if result == 1 : conn.commit()
            return result
        except Exception as e:
            print("DB연동 에러 : ", e)
        finally:
            cursor.close()
            conn.close()
    
    # 포트폴리오 데이터 가져오기
    def select_port(self, pfname):
        print(f'select:{pfname}')
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            sql = f"SELECT * FROM portfolio WHERE pfname='{pfname}'"
            cursor.execute(sql)                
            res = cursor.fetchall()
            if not res : return None
            return res
        except Exception as e:
            print("DB연동 에러 : ", e)
        finally:
            cursor.close()
            conn.close()
    
    # 포트폴리오 이름 가져오기
    def select_port_list(self):  # email 추가해야함!
        #print(f"select:{email}")
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            sql = f"SELECT DISTINCT pfname FROM portfolio" # WHERE email='{email}'
            cursor.execute(sql)                
            res = cursor.fetchall()
            result = []
            for re in res:
                result.append(re)
            if not res : return None
            return result
        except Exception as e:
            print("DB연동 에러 : ", e)
        finally:
            cursor.close()
            conn.close()
       
    # 포트폴리오 삭제        
    def delete_port(self, pfname):
        print(f'select:{pfname}')
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            sql = f"DELETE FROM portfolio WHERE pfname='{pfname}'"
            res = cursor.execute(sql)                
            if res == 1: conn.commit()
            return res
        except Exception as e:
            print("DB연동 에러 : ", e)
        finally:
            cursor.close()
            conn.close()