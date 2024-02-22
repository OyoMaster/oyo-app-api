from datetime import datetime
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connention import get_connection
from mysql.connector import Error

# 인기 검색어 TOP10
class historyTop10(Resource) :
    
    @jwt_required()
    def get(self) :

        offset = request.args.get('offset')
        limit = request.args.get('limit')


        # 1. 클라이언트로부터 데이터를 받아온다
        # 받아올 데이터 없음.

        # 2. DB에 저장된 데이터를 가져온다.

        try :
            connection = get_connection()

            query = ''' select id, keyword,  count(keyword) as keywordCnt
                                    from history
                                    group by keyword
                                    order by keywordCnt desc
                                    limit '''+ offset+''', '''+ limit+''';'''
            
            # 중요!!
            # select 문에서 커서를 만들 때에는 
            # 파라미터 dictionary = True 로 해준다
            # 왜? 리스트와 딕셔너리 형태로 가져오기 때문에
            # 클라이언트에게 json 형식으로 보내줄 수 있다.
            
            cursor = connection.cursor(dictionary=True)

            cursor.execute(query)

            result_list = cursor.fetchall()


            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail" , "error" : str(e)}, 500


        return {"result" : "success" , 
                "items" : result_list,
                "count" : len(result_list)} , 200    