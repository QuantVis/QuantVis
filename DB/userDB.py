import pymysql

class User():       
        
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

    def get_user_info(self, user_id = '',user_email = ''):
        try:
                conn = pymysql.connect(**self.config)
                cursor = conn.cursor()
                if user_email != '' :
                    sql = f"SELECT * from user where email = '{user_email}'"
                elif user_id != '' :
                    sql = f"SELECT * from user where id = '{user_id}'"
                cursor.execute(sql)
                res = cursor.fetchone()
                if not res : return None                
                user = {'id' : res[1], 'email' : res[2], 'password' : res[3], 'nick' : res[4], 'method' : res[5], 'my_stock' : res[6]}
                return user

        except Exception as e:
            print("DB연동 에러 : ", e)
        finally:
            cursor.close()
            conn.close()
    
    def create_user_info(self, user_id,  method, email='', password='', nick='') :
        try:
                conn = pymysql.connect(**self.config)
                cursor = conn.cursor()
                sql = f"INSERT INTO user(id, email, password, nick, method) VALUES ('{user_id}', '{email}', '{password}', '{nick}', '{method}')"
                result = cursor.execute(sql)                
                if result == 1 : conn.commit()
                return result

        except Exception as e:
            print("DB연동 에러 : ", e)
            conn.rollback()
        finally:            
            cursor.close()
            conn.close()
    
    def nick_check(self, nick) :
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            sql = f"SELECT id FROM user WHERE nick = '{nick}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
        
        except Exception as e:
            print("DB연동 에러 : ", e)
            conn.rollback()
        finally:            
            cursor.close()
            conn.close()
            
    ## 로컬가입용 정보변경
    def set_change1(self, email, nick='', password='') :
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            if nick != '' : sql = f"UPDATE user SET nick = '{nick}' WHERE email = '{email}'"
            result = cursor.execute(sql)
            if result == 1 : conn.commit()
            
            if password != '' : sql = f"UPDATE user SET password = '{password}' WHERE email = '{email}'"
            result = cursor.execute(sql)
            if result == 1 : conn.commit()
            return result
        
        except Exception as e:
            print("DB연동 에러 : ", e)
            conn.rollback()
        finally:            
            cursor.close()
            conn.close()
    
    ## 소셜로그인용 정보변경
    def set_change2(self, user_id, nick='', email='') :
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            if nick != '' and email != '' : 
                sql = f"UPDATE user SET email = '{email}', nick = '{nick}' WHERE id = '{user_id}'"
            elif nick != '' : 
                sql = f"UPDATE user SET nick = '{nick}' WHERE id = '{user_id}'"
            elif email != '' : 
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
            
    def find_pw(self, email, nick) :
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            sql = f"SELECT * FROM user WHERE email = '{email}' and nick = '{nick}'"
            result = cursor.execute(sql)
            return result
        
        except Exception as e:
            print("DB연동 에러 : ", e)
            conn.rollback()
        finally:            
            cursor.close()
            conn.close()
        
    
