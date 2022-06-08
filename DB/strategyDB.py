# import pymysql

# class strategy( ):       
#     def __init__(self):
#         self.config = {
#                 'host':'127.0.0.1',
#                 'user':'quantvis',
#                 'password':'quantvis',
#                 'database':'quantvis',
#                 'port':3306,
#                 'charset':'utf8',
#                 'use_unicode':True
#             }   
#     def getDB_STAT_1(self, stock_cod,start_date,end_date):
#         try:
#             conn = pymysql.connect(**config)
#             cursor = conn.cursor()
#             stock_code = stock_cod.replace("-","_")
#             sql = f"select * from `{stock_code}` where date >= {start_date} and date <={end_date}"
#             cursor.execute(sql)
#             rows = cursor.fetchall()
#             col = ['date', 'open', 'high', 'low', 'close', 'volume', 'company', 'ticker']
#             result = pd.DataFrame(rows, columns=col)
#             result.reset_index(drop=True)
#             return result
        
#         except Exception as e:
#             print("DB연동 에러 : ", e)
#             conn.rollback()
#         finally:
#             cursor.close()
#             conn.close()