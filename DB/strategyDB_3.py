import pymysql
import pandas as pd

class strategyyy():       
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
    def getDB_STAT_3(self):
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            sql1 = f"select ticker, sector, quarterdate, concat(quarterepsgrowth,'%') as a, yeardate, concat(threeyearearningsgrowth,'%') as b, concat(threeyearroe,'%') as c, concat(oneyearprofit,'%') as d, concat(oneyearsnpprofit,'%') from william_result_roe_20220619"
            sql2= f"select ticker, sector, quarterdate, concat(quarterepsgrowth,'%') as a, yeardate, concat(threeyearearningsgrowth,'%') as b, concat(threeyearroe,'%') as c, concat(oneyearprofit,'%') as d, concat(oneyearsnpprofit,'%') from william_result_roe_20220619 order by a desc limit 5"
            sql3= f"select ticker, sector, quarterdate, concat(quarterepsgrowth,'%') as a, yeardate, concat(threeyearearningsgrowth,'%') as b, concat(threeyearroe,'%') as c, concat(oneyearprofit,'%') as d, concat(oneyearsnpprofit,'%') from william_result_roe_20220619 order by b desc limit 5"
            sql4= f"select ticker, sector, quarterdate, concat(quarterepsgrowth,'%') as a, yeardate, concat(threeyearearningsgrowth,'%') as b, concat(threeyearroe,'%') as c, concat(oneyearprofit,'%') as d, concat(oneyearsnpprofit,'%') from william_result_roe_20220619 order by c desc limit 5"
            sql5= f"select ticker, sector, quarterdate, concat(quarterepsgrowth,'%') as a, yeardate, concat(threeyearearningsgrowth,'%') as b, concat(threeyearroe,'%') as c, concat(oneyearprofit,'%') as d, concat(oneyearsnpprofit,'%') from william_result_roe_20220619 order by d desc limit 5"
            cursor.execute(sql1)
            rows1 = cursor.fetchall()
            cursor.execute(sql2)
            rows2 = cursor.fetchall()
            cursor.execute(sql3)
            rows3 = cursor.fetchall()
            cursor.execute(sql4)
            rows4 = cursor.fetchall()
            cursor.execute(sql5)
            rows5 = cursor.fetchall()
            col = ['티커심볼','산업분류','기준분기','분기EPS성장률','기준연도','3년순이익성장률','3년평균ROE','1년수익률','1년지수수익률']
            result1 = pd.DataFrame(rows1, columns=col)
            result1.reset_index(drop=True)
            result2 = pd.DataFrame(rows2, columns=col)
            result2.reset_index(drop=True)
            result3 = pd.DataFrame(rows3, columns=col)
            result3.reset_index(drop=True)
            result4 = pd.DataFrame(rows4, columns=col)
            result4.reset_index(drop=True)
            result5 = pd.DataFrame(rows5, columns=col)
            result5.reset_index(drop=True)

            return result1, result2, result3, result4, result5

        except Exception as e:
            print("DB연동 에러 : ", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
