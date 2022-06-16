import pymysql
import pandas as pd

class strategy():       
    def __init__(self):
        self.config = {
                'host':'127.0.0.1',
                'user':'quantvis',
                'password':'quantvis',
                'database':'quantvis',
                'port':3306,
                'charset':'utf8',
                'use_unicode':True
            }   
    def getDB_STAT_1(self, stock_cod,start_date,end_date):
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            stock_code = stock_cod.replace("-","_")
            sql = f"select * from `{stock_code}` where date >= {start_date} and date <={end_date}"
            cursor.execute(sql)
            rows = cursor.fetchall()
            col = ['date', 'open', 'high', 'low', 'close', 'volume', 'company', 'ticker']
            result = pd.DataFrame(rows, columns=col)
            result.reset_index(drop=True)
            return result
        
        except Exception as e:
            print("DB연동 에러 : ", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
            
    def getUSstock_close(self, ticker,start_date,end_date):
        df_AAPL_close = self.getDB_STAT_1('AAPL', start_date,end_date)['date']
        df = self.getDB_STAT_1(ticker, start_date,end_date)['close']
        df_ticker_close= df.rename(ticker) 
        df_ticker_date = self.getDB_STAT_1(ticker, start_date,end_date)['date']
        df_ticker_close_date= pd.concat([df_ticker_date,df_ticker_close],axis=1)
        result= pd.merge(df_AAPL_close,df_ticker_close_date,on='date', how='left')
        result1= result.iloc[:,[1]]
        return result1