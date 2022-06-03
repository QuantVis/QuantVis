import pymysql
from flask_login import UserMixin

class User(UserMixin):       
        
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

    def get_user_info(self, user_email):
        print(f'select : {user_email}')
        try:
                conn = pymysql.connect(**self.config)
                cursor = conn.cursor()
                sql = f"select * from user where email = '{user_email}'"
                cursor.execute(sql)
                res = cursor.fetchone()
                if not res : return None                
                user = {'user_id' : res[1], 'user_email' : res[2], 'nick' : res[3], 'method' : res[4], 'my_stock' : res[5]}
                return user

        except Exception as e:
            print("DB연동 에러 : ", e)
        finally:
            cursor.close()
            conn.close()
    
    def create_user_info(self, user_id, email, method) :
        try:
                conn = pymysql.connect(**self.config)
                cursor = conn.cursor()
                sql = f"INSERT INTO user(id, email, method) VALUES ('{user_id}', '{email}', '{method}')"
                result = cursor.execute(sql)                
                if result == 1 : conn.commit()
                return result

        except Exception as e:
            print("DB연동 에러 : ", e)
            conn.rollback()
        finally:            
            cursor.close()
            conn.close()
            
    def update_nick(self, user_id, nick) :
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            sql = f"UPDATE user SET nick = '{nick}' WHERE id = '{user_id}'"
            result = cursor.execute(sql)                
            if result == 1 : conn.commit()
            return result
        
        except Exception as e:
            print("DB연동 에러 : ", e)
            conn.rollback()
        finally:            
            cursor.close()
            conn.close()
        
    def update_email(self, user_id, email) :
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            sql = f"UPDATE user SET email = '{email}' WHERE id = '{user_id}'"
            result = cursor.execute(sql)                
            if result == 1 : conn.commit()
            return result
        
        except Exception as e:
            print("DB연동 에러 : ", e)
            conn.rollback()
        finally:            
            cursor.close()
            conn.close()
    
