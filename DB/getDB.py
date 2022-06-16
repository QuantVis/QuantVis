import pandas as pd
import pymysql
import numpy as np

class getDB:
    stock_code = None
    
    def __init__(self, stock_code):
        self.stock_code = stock_code
    
    def GetStockData(self):
        config = {
            'host':'127.0.0.1',
            'user':'scott',
            'password':'tiger',
            'database':'quantvis',
            'port':3306,
            'charset':'utf8',
            'use_unicode':True
        }

        stock_code2 = 'k' + self.stock_code
        
        try:
            conn = pymysql.connect(**config)
            cursor = conn.cursor()
            sql = f"select * from {stock_code2}"
            cursor.execute(sql)
            rows = cursor.fetchall()
            col = ['date', 'open', 'high', 'low', 'close', 'volume', 'company', 'ticker']
            result = pd.DataFrame(rows, columns=col)
            result.reset_index(drop=True)
            result = result.fillna(0.0)
            result['ema60'] = result.close.ewm(span=60).mean()
            result['ema130'] = result.close.ewm(span=130).mean()
            result['macd'] = result['ema60'] - result['ema130']
            result['signal'] = result['macd'].ewm(span=45).mean()
            result['macdhist'] = result['macd']-result['signal']
            result['ndays_high'] = result.high.rolling(window=14,min_periods=1).max()
            result['ndays_low'] = result.low.rolling(window=14,min_periods=1).min()
            result['fast_k'] = (result['close'] - result['ndays_low'])/(result['ndays_high']-result['ndays_low']) * 100
            result['slow_d'] = result['fast_k'].rolling(window=3).mean()
            result = result.replace([np.inf, -np.inf], np.nan)
            result = result.fillna(0.0)

            a = []
            b = []
            c = []
            d = []
            e = []
            f = []
            ma130lst = []
            macdlst = []
            signallst = []
            macdhistlst = []
            fast_k = []
            slow_d = []
            company = result['company'][0]
            for i in range(0, len(result)):
                date = result['date'][i].strftime('%y%m%d')
                datelst = [int("20" + date[:2]), int(date[2:4]), int(date[4:6])]
                a.append(datelst)
                b.append(result['low'][i])
                c.append(result['open'][i])
                d.append(result['close'][i])
                e.append(result['high'][i])
                f.append(result['volume'][i])
                ma130lst.append(result['ema130'][i])
                macdlst.append(result['macd'][i])
                signallst.append(result['signal'][i])
                macdhistlst.append(result['macdhist'][i])
                fast_k.append(result['fast_k'][i])
                slow_d.append(result['slow_d'][i])
            insight = None
            if ma130lst[len(ma130lst)-2] < ma130lst[len(ma130lst)-1] and \
                slow_d[len(ma130lst)-2] > slow_d[len(ma130lst)-1] and slow_d[len(ma130lst)-1] <20:
                    insight = "매수"
            elif ma130lst[len(ma130lst)-2] > ma130lst[len(ma130lst)-1] and \
                slow_d[len(ma130lst)-2] < slow_d[len(ma130lst)-1] and slow_d[len(ma130lst)-1] >80:
                    insight = "매도"
            else: insight = "관망"    
            return a, b, c, d, e, f, ma130lst, macdlst, signallst, macdhistlst, fast_k, slow_d, company, insight

        except Exception as e:
            print("DB연동 에러 : ", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

class getName:
    company = None
    
    def __init__(self, company):
        self.company = company

    def GetStockName(self):
        config = {
        'host':'127.0.0.1',
        'user':'scott',
        'password':'tiger',
        'database':'quantvis',
        'port':3306,
        'charset':'utf8',
        'use_unicode':True
        }
        try:
            conn = pymysql.connect(**config)
            cursor = conn.cursor()
            sql = f"select * from companyList where company = '{self.company}'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
            
        except Exception as e:
            print("DB연동 에러 : ", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
            

class getUSDB:
    stock_code = None
    
    def __init__(self, stock_code):
        self.stock_code = stock_code
    
    def GetUSStockData(self):
        config = {
            'host':'127.0.0.1',
            'user':'scott',
            'password':'tiger',
            'database':'quantvis',
            'port':3306,
            'charset':'utf8',
            'use_unicode':True
        }
        try:
            conn = pymysql.connect(**config)
            cursor = conn.cursor()
            sql = f"select * from `{self.stock_code}`"
            cursor.execute(sql)
            rows = cursor.fetchall()
            col = ['date', 'open', 'high', 'low', 'close', 'volume', 'company', 'ticker']
            result = pd.DataFrame(rows, columns=col)
            result.reset_index(drop=True)
            result = result.fillna(0.0)
            result['ema60'] = result.close.ewm(span=60).mean()
            result['ema130'] = result.close.ewm(span=130).mean()
            result['macd'] = result['ema60'] - result['ema130']
            result['signal'] = result['macd'].ewm(span=45).mean()
            result['macdhist'] = result['macd']-result['signal']
            result['ndays_high'] = result.high.rolling(window=14,min_periods=1).max()
            result['ndays_low'] = result.low.rolling(window=14,min_periods=1).min()
            result['fast_k'] = (result['close'] - result['ndays_low'])/(result['ndays_high']-result['ndays_low']) * 100
            result['slow_d'] = result['fast_k'].rolling(window=3).mean()
            result = result.replace([np.inf, -np.inf], np.nan)
            result = result.fillna(0.0)
            
            a = []
            b = []
            c = []
            d = []
            e = []
            f = []
            ma130lst = []
            macdlst = []
            signallst = []
            macdhistlst = []
            fast_k = []
            slow_d = []
            company = result['company'][0]
            for i in range(0, len(result)):
                date = result['date'][i].strftime('%y%m%d')
                datelst = [int("20" + date[:2]), int(date[2:4]), int(date[4:6])]
                a.append(datelst)
                b.append(result['low'][i])
                c.append(result['open'][i])
                d.append(result['close'][i])
                e.append(result['high'][i])
                f.append(result['volume'][i])
                ma130lst.append(result['ema130'][i])
                macdlst.append(result['macd'][i])
                signallst.append(result['signal'][i])
                macdhistlst.append(result['macdhist'][i])
                fast_k.append(result['fast_k'][i])
                slow_d.append(result['slow_d'][i])
            insight = None
            if ma130lst[len(ma130lst)-2] < ma130lst[len(ma130lst)-1] and \
                slow_d[len(ma130lst)-2] > slow_d[len(ma130lst)-1] and slow_d[len(ma130lst)-1] <20:
                    insight = "매수"
            elif ma130lst[len(ma130lst)-2] > ma130lst[len(ma130lst)-1] and \
                slow_d[len(ma130lst)-2] < slow_d[len(ma130lst)-1] and slow_d[len(ma130lst)-1] >80:
                    insight = "매도"
            else: insight = "관망"    
            return a, b, c, d, e, f, ma130lst, macdlst, signallst, macdhistlst, fast_k, slow_d, company, insight

        except Exception as e:
            print("DB연동 에러 : ", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()