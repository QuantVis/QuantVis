import pymysql
import pandas as pd

class strategyy():       
    def __init__(self):
        self.config = {
                'host':'127.0.0.1',
                'user':'quantvis',
                'password':'quantvis',
                'database':'quantvis_strategy_1',
                'port':3306,
                'charset':'utf8',
                'use_unicode':True
            }   
    def getDB_STAT_2(self):
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            sql_1 = f"select date, sector, ticker, concat(truncate(earnings_yield*100,2),'%') ,concat(truncate(roic*100,2),'%') from jg_result_ey_20220615 order by earnings_yield desc"
            cursor.execute(sql_1)
            rows_1 = cursor.fetchall()
            col_1 = ['실적발표일', '섹터명', '티커심볼','이익수익률(Earnings Yield)','자본수익률(ROIC)' ]
            result1 = pd.DataFrame(rows_1, columns=col_1)
            result1.reset_index(drop=True)
            
            sql2 = f"select date, sector,ticker, concat(truncate(roic*100,2),'%'), concat(truncate(earnings_yield*100,2),'%') from jg_result_roic_20220615 order by roic desc"
            cursor.execute(sql2)
            rows_2 = cursor.fetchall()
            col_2 = ['실적발표일', '섹터명','티커심볼','자본수익률(ROIC)','이익수익률(Earnings Yield)' ]
            result2 = pd.DataFrame(rows_2,  columns=col_2)
            result2.reset_index(drop=True)
            print(result1, result2)
            
            return result1, result2
        
        except Exception as e:
            print("DB연동 에러 : ", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


