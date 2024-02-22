from flask import request
from flask_jwt_extended import  get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector import Error
from mysql_connention import get_connection

class FavoritesResource(Resource):
    # 즐겨찾기 추가
    @jwt_required()
    def post(self,postingId) :

        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''
                        insert into favorites
                            (userId, postingId)
                            values 
                            (%s,%s);'''
            
            record = (user_id,postingId)
            
            cursor = connection.cursor()
            cursor.execute(query,record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)},500
        
        
        return {'result' : 'success'} , 200
    
    # 즐겨찾기 해제
    @jwt_required()
    def delete(self,postingId) :

        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''
                        delete 
                            from favorites
                            where userId = %s and postingId = %s;'''
                                        
            record = (user_id,postingId)
            
            cursor = connection.cursor()
            cursor.execute(query,record)

            connection.commit()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)},500
        
        
        return {'result' : 'success'} , 200
