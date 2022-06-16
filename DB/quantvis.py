import pymysql

class Quantvis():           
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
        
    # 테이블 목록=종목코드 가져오기
    def select_All_table(self):
        print(f'select:모든 테이블')
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            sql = f"SHOW TABLES"
            cursor.execute(sql)                
            res = cursor.fetchall()
            
            if not res : return None
            return res
        except Exception as e:
            print("DB연동 에러 : ", e)
        finally:
            cursor.close()
            conn.close()
    
    # 회사이름 가져오기
    def select_ticker_name(self,table):
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            sql = f"SELECT DISTINCT company FROM `{table}`"
            cursor.execute(sql)                
            res = cursor.fetchone()
            result = []
            for re in res:
                result.append(re)
            if not res : return " "
            return result
        except Exception as e:
            print("DB연동 에러 : ", e)
        finally:
            cursor.close()
            conn.close()
    
    # 최근가격 가져오기
    def select_price(self,table):
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            sql = f"SELECT close FROM `{table}` WHERE date = (SELECT MAX(date) FROM `{table}`)"
            cursor.execute(sql)                
            res = cursor.fetchone()
            if not res : return " "
            return res[0]
        except Exception as e:
            print("DB연동 에러 : ", e)
        finally:
            cursor.close()
            conn.close()
    