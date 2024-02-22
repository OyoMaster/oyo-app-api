
from datetime import datetime
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connention import get_connection
from mysql.connector import Error



# resources 폴더 안에 만드는 파일에는,
# API를 만들기 위한 클래스를 작성한다.

#  API를 만들기 위해서는 flask_restful 라이브러라의 
# Resource 클래스를 상속해서 만들어야 한다

# 전체 레시피(간략히)
class RecipeListResource(Resource) :

    # JWT 토큰이 헤어데 필수로 있어야 한다는 뜻.
    # 토큰이 없으면, 이 API는 실행이 안된다.
    @jwt_required()
    def get(self) :

        order = request.args.get('order')
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        

        # 1. 클라이언트로부터 데이터를 받아온다
        # 받아올 데이터 없음.

        # 2. DB에 저장된 데이터를 가져온다.

        try :
            connection = get_connection()

            query = ''' select p.id as postingid,p.title,
                                    p.imageURL, u.nickname, u.id as userId, 
                                    avg(ifnull(r.rating,0)) as avgRating,
                                    if( f.id is null  , 0 , 1 ) as isFavorite
                                    from posting p
                                    join user u
                                    on u.id = p.userId
                                    left join review r
                                    on p.id = r.postingId
                                    left join favorites f
                                    on p.id = f.postingId
                                    group by p.id
                                    order by '''+ order +''' desc
                                    limit '''+offset +''', '''+limit+''';'''
            
            # 중요!!
            # select 문에서 커서를 만들 때에는 
            # 파라미터 dictionary = True 로 해준다
            # 왜? 리스트와 딕셔너리 형태로 가져오기 때문에
            # 클라이언트에게 json 형식으로 보내줄 수 있다.
            
            cursor = connection.cursor(dictionary=True)

            cursor.execute(query)

            result_list = cursor.fetchall()


            # datetime 은 파이썬에서 사용하는 데이터타입 이므로
            #  json 형식이 아니다. 따라서
            #  json은 문자열이나 숫자만 가능하므로
            #  datetime을 문자열로 바꿔줘야 한다.

            i = 0
            for row in result_list :
                result_list[i]['avgRating'] = float(row['avgRating'])
            
                i = i + 1

            print()
            print(result_list)
            print()


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


# 전체 레시피(더보기)
class RecipeListMoreShowResource(Resource) :

    # JWT 토큰이 헤어데 필수로 있어야 한다는 뜻.
    # 토큰이 없으면, 이 API는 실행이 안된다.
    @jwt_required()
    def get(self) :

        user_id = get_jwt_identity()

        print()
        print(user_id)

        order = request.args.get('order')
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        

        # 1. 클라이언트로부터 데이터를 받아온다
        # 받아올 데이터 없음.

        # 2. DB에 저장된 데이터를 가져온다.

        try :
            connection = get_connection()

            query = ''' SELECT 
                                        p.id as postingid, p.imageURL, p.title, u.id as userId,
                                        u.nickname,
                                        p.createdAt,p.updatedAt,
                                        IF(f.id IS NULL, 0, 1) AS isFavorite,
                                        AVG(IFNULL(r.rating, 0)) AS avgRating
                                    FROM 
                                        posting p
                                    JOIN    
                                        user u ON p.userId = u.id
                                    LEFT JOIN 
                                        favorites f ON p.id = f.postingId AND f.userId = %s
                                    LEFT JOIN 
                                        review r ON p.id = r.postingId
                                    GROUP BY 
                                        p.id
                                    order by '''+ order +''' desc
                                    limit '''+offset +''', '''+limit+''';'''
            
            # 중요!!
            # select 문에서 커서를 만들 때에는 
            # 파라미터 dictionary = True 로 해준다
            # 왜? 리스트와 딕셔너리 형태로 가져오기 때문에
            # 클라이언트에게 json 형식으로 보내줄 수 있다.

            record = (user_id, )
            
            cursor = connection.cursor(dictionary=True)

            cursor.execute(query, record)

            result_list = cursor.fetchall()


            # datetime 은 파이썬에서 사용하는 데이터타입 이므로
            #  json 형식이 아니다. 따라서
            #  json은 문자열이나 숫자만 가능하므로
            #  datetime을 문자열로 바꿔줘야 한다.

            i = 0
            for row in result_list :
                result_list[i]['createdAt']= row['createdAt'].isoformat()
                result_list[i]['updatedAt']= row['updatedAt'].isoformat()
                result_list[i]['avgRating'] = float(row['avgRating'])
                i = i + 1

            print()
            print(result_list)
            print()


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

# 안씀
class RecipeResource(Resource) :


    #  Path (경로)에 숫자나 문자가 바뀌면서 처리되는 경우에는
    #  해당 변수를, 파라미터에 꼭 써줘야 한다.
    #  이 변수는, app.py 파일의 addResource 함수에서 사용한 변수다!
    def get(self, recipe_id ) :
        print(recipe_id)

        # 1. 클라이언트로부터 데이터를 받아온다.
        #    이미 경로에 들어있는, 레시피 아이디를 받아왔다.
        #    위의 recipe_id 라는 변수에 이미 있다.

        # 2. DB에서 recipe_id에 해당하는 레시피 1개를 가져온다.
        try :
            connection = get_connection()
            
            query = '''select *
                        from recipe
                        where id = %s; '''
            
            recode = (recipe_id , )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query,recode)

            #  fetchall 함수는 항상 결과를 리스트로 리턴한다.
            result_list = cursor.fetchall()
            print('DB에서 실행')
            print(result_list)

            i = 0
            for row in result_list :
                result_list[0]['createdAt']= row['createdAt'].isoformat()
                result_list[0]['updatedAt']= row['updatedAt'].isoformat()
                i = i + 1


            cursor.close()
            connection.close()


        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail", "error" : str(e)} , 500
        
        #  여기서 리스트에 데이터가 있는 경우와 없는 경우로 체크하여
        #  클라이언트에게 데이터를 보낸다
        
        if len(result_list) == 0 :
            return {"result" : "fail", "message" : "데이터를 찾을 수 없습니다"}, 400
        else :
              return {"result" : "success",
                "items" : result_list[0]} , 200

# 상세 레시피
class RecipeDetail(Resource) :
    
        
    #  Path (경로)에 숫자나 문자가 바뀌면서 처리되는 경우에는
    #  해당 변수를, 파라미터에 꼭 써줘야 한다.
    #  이 변수는, app.py 파일의 addResource 함수에서 사용한 변수다!
    @jwt_required()
    def get(self, posting_id ) :

        user_id = get_jwt_identity()

        print(user_id)
        print(posting_id)

        # 1. 클라이언트로부터 데이터를 받아온다.
        #    이미 경로에 들어있는, 레시피 아이디를 받아왔다.
        #    위의 recipe_id 라는 변수에 이미 있다.

        # 2. DB에서 recipe_id에 해당하는 레시피 1개를 가져온다.
        try :
            connection = get_connection()
            
            query = '''select u.id, u.nickname, u.profileUrl, 
                                p.id as postingid, p.title, p.imageURL, 
                                p.ingredients, p.recipe, p.createdAt, p.updatedAt,
                                avg(ifnull(r.rating,0)) as avgRating,
                                if( f.id is null  , 0 , 1 ) as isFavorite
                                from posting p
                                join user u
                                on u.id = p.userId
                                left join review r
                                on p.id = r.postingId
                                left join favorites f
                                on p.id = f.postingId
                                where p.id = %s
                                group by p.id
                                order by p.createdAt desc; '''
            
            recode = (posting_id , )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query,recode)

            #  fetchall 함수는 항상 결과를 리스트로 리턴한다.
            result_list = cursor.fetchall()
            print('DB에서 실행')
            print(result_list)

            i = 0
            for row in result_list :
                result_list[0]['createdAt']=row['createdAt'].isoformat()
                result_list[0]['updatedAt']= row['updatedAt'].isoformat()
                result_list[0]['avgRating'] = float(row['avgRating'])
                i = i + 1
        

            # datetime.datetime.strpftime('%Y-%m-%d %H시 %M분')


            cursor.close()
            connection.close()


        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail", "error" : str(e)} , 500
        
        #  여기서 리스트에 데이터가 있는 경우와 없는 경우로 체크하여
        #  클라이언트에게 데이터를 보낸다
        
        if len(result_list) == 0 :
            return {"result" : "fail", "message" : "데이터를 찾을 수 없습니다"}, 400
        else :
              return {"result" : "success",
                      "items" : result_list[0]} , 200


# 나만의 레시피 상단 나의 정보 불러오기(240206 : 추가) 

class RecipeMeInfo(Resource) : 
    
    @jwt_required()
    def get(self) : 

        user_id = get_jwt_identity()

        print()
        print(user_id)
        
        try :
            connection = get_connection()
            query = ''' SELECT u.id as userId, u.email, u.nickname, u.profileUrl,
                        (SELECT COUNT(*) FROM posting WHERE userId = %s) AS postingCnt,
                        (SELECT COUNT(*) FROM follow WHERE followeeId = %s) AS follwerCnt,
                        (SELECT COUNT(*) FROM follow WHERE followerId = %s) AS followeeCnt
                        from user u
                        where u.id = %s;'''
            
            record = (user_id ,user_id ,user_id,user_id)
            cursor = connection.cursor(dictionary= True)
            cursor.execute(query,record)

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {'result' : 'fail', 'error' : str(e)} , 400
        print()
        print(result_list[0])


    


        return {'result' : 'success',
                'items' : result_list[0] } , 200   

# 나만의 레시피 
class RecipeMeResource(Resource) :


    @jwt_required()
    def get(self) :

        order = request.args.get('order')
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        user_id = get_jwt_identity()

        print()
        print(user_id)


        try :
            connection = get_connection()
            query = ''' select p.id as postingid, p.imageURL, p.title, u.nickname,
                                    p.createdAt,p.updatedAt,
                                    avg(ifnull(r.rating,0)) as avgRating,
                                    if( f.id is null  , 0 , 1 ) as isFavorite
                                    from posting p
                                    join user u
                                    on u.id = p.userId
                                    left join review r
                                    on p.id = r.postingId
                                    left join favorites f
                                    on p.id = f.postingId
                                    where u.id = %s
                                    group by p.id
                                    order by '''+ order +''' desc
                                    limit '''+offset +''', '''+limit+''';'''
            
            record = (user_id , )

            cursor = connection.cursor(dictionary= True)
            cursor.execute(query,record)

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {'result' : 'fail', 'error' : str(e)} , 400
        print()
        print(result_list)

        i = 0
        for row in result_list :
                result_list[i]['createdAt']= row['createdAt'].isoformat()
                result_list[i]['updatedAt']= row['updatedAt'].isoformat()
                result_list[i]['avgRating'] = float(row['avgRating'])
                i = i + 1


    


        return {'result' : 'success',
                'items' : result_list,
                'count' : len(result_list)
                  } , 200

# 내가 즐겨찾기한 사람의 레시피   
class MyFavoriteRecipeResource(Resource) :
    
    @jwt_required()
    def get(self) :

        user_id = get_jwt_identity()

        print()
        print(user_id)

        

        # 1. 클라이언트로부터 데이터를 받아온다
        # 받아올 데이터 없음.

        # 2. DB에 저장된 데이터를 가져온다.

        try :
            connection = get_connection()

            query = ''' SELECT p.id AS postingId,
                                    p.title,
                                    p.imageURL,
                                    u.id as userId, 
                                    u.nickname,
                                    p.createdAt,
                                    p.updatedAt,
                                    AVG(IFNULL(r.rating, 0)) AS avgRating,
                                    if( f.id is null  , 0 , 1 ) as isFavorite
                                FROM posting p
                                JOIN favorites f ON p.id = f.postingId
                                LEFT JOIN review r ON p.id = r.postingId
                                join user u on p.userId = u.id
                                WHERE f.userId = %s
                                GROUP BY p.id
                                order by p.createdAt desc;'''
            record = (user_id , )
            
            # 중요!!
            # select 문에서 커서를 만들 때에는 
            # 파라미터 dictionary = True 로 해준다
            # 왜? 리스트와 딕셔너리 형태로 가져오기 때문에
            # 클라이언트에게 json 형식으로 보내줄 수 있다.
            
            cursor = connection.cursor(dictionary=True)

            cursor.execute(query,record)

            result_list = cursor.fetchall()


            # datetime 은 파이썬에서 사용하는 데이터타입 이므로
            #  json 형식이 아니다. 따라서
            #  json은 문자열이나 숫자만 가능하므로
            #  datetime을 문자열로 바꿔줘야 한다.

            i = 0
            for row in result_list :
                result_list[i]['createdAt']= row['createdAt'].isoformat()
                result_list[i]['updatedAt']= row['updatedAt'].isoformat()
                result_list[i]['avgRating'] = float(row['avgRating'])
                
                i = i + 1

            print()
            print(result_list)
            print()


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

# 해당 유저의 프로필 레시피
class UserProfileResoucre(Resource):

    @jwt_required()
    def get(self,userId):
        user_id = get_jwt_identity()

        print()
        print(user_id)

        offset = request.args.get('offset')
        limit = request.args.get('limit')

        

        # 1. 클라이언트로부터 데이터를 받아온다
        # 받아올 데이터 없음.

        # 2. DB에 저장된 데이터를 가져온다.

        try :
            connection = get_connection()

            query = ''' SELECT 
                        u.id as userId, p.id AS postingid, 
                        p.imageURL, 
                        p.title, 
                        u.nickname, 
                        p.createdAt, 
                        p.updatedAt,
                        AVG(IFNULL(r.rating, 0)) AS avgRating, 
                        IF(f.id IS NULL, 0, 1) AS isFavorite
                        FROM 
                            posting p
                        JOIN    
                            user u ON p.userId = u.id
                        LEFT JOIN 
                            favorites f ON p.id = f.postingId 
                        LEFT JOIN 
                            review r ON p.id = r.postingId
                        WHERE 
                            u.id = %s
                        GROUP BY p.id
                        order by p.createdAt
                        limit '''+offset +''', '''+limit+''';'''
            record = (userId , )
            
            # 중요!!
            # select 문에서 커서를 만들 때에는 
            # 파라미터 dictionary = True 로 해준다
            # 왜? 리스트와 딕셔너리 형태로 가져오기 때문에
            # 클라이언트에게 json 형식으로 보내줄 수 있다.
            
            cursor = connection.cursor(dictionary=True)

            cursor.execute(query,record)

            result_list = cursor.fetchall()


            # datetime 은 파이썬에서 사용하는 데이터타입 이므로
            #  json 형식이 아니다. 따라서
            #  json은 문자열이나 숫자만 가능하므로
            #  datetime을 문자열로 바꿔줘야 한다.

            i = 0
            for row in result_list :
                result_list[i]['createdAt']= row['createdAt'].isoformat()
                result_list[i]['updatedAt']= row['updatedAt'].isoformat()
                result_list[i]['avgRating'] = float(row['avgRating'])
                
                i = i + 1

            print()
            print(result_list)
            print()


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

# 해당 유저의 팔로우 팔로잉 게시물 수
class UserFollowResoutce(Resource):
    

    @jwt_required()
    def get(self,userId):
        user_id = get_jwt_identity()

        print()
        print(user_id)

        offset = request.args.get('offset')
        limit = request.args.get('limit')

        

        # 1. 클라이언트로부터 데이터를 받아온다
        # 받아올 데이터 없음.

        # 2. DB에 저장된 데이터를 가져온다.

        try :
            connection = get_connection()

            query = ''' SELECT u.id as userId, u.email, u.nickname, u.profileUrl,
                (SELECT COUNT(*) FROM posting WHERE userId = %s) AS cntPosting,
                (SELECT COUNT(*) FROM follow WHERE followeeId = %s) AS cntFollower,
                (SELECT COUNT(*) FROM follow WHERE followerId = %s) AS cntFollowing
                from user u
                where u.id = %s;'''
            record = (userId ,userId,userId,userId )
            
            # 중요!!
            # select 문에서 커서를 만들 때에는 
            # 파라미터 dictionary = True 로 해준다
            # 왜? 리스트와 딕셔너리 형태로 가져오기 때문에
            # 클라이언트에게 json 형식으로 보내줄 수 있다.
            
            cursor = connection.cursor(dictionary=True)

            cursor.execute(query,record)

            result_list = cursor.fetchall()


            # datetime 은 파이썬에서 사용하는 데이터타입 이므로
            #  json 형식이 아니다. 따라서
            #  json은 문자열이나 숫자만 가능하므로
            #  datetime을 문자열로 바꿔줘야 한다.

            # i = 0
            # for row in result_list :
            #     result_list[i]['createdAt']= row['createdAt'].isoformat()
            #     result_list[i]['updatedAt']= row['updatedAt'].isoformat()
            #     result_list[i]['avgRating'] = float(row['avgRating'])
                
            #     i = i + 1

            print()
            print(result_list)
            print()


            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail" , "error" : str(e)}, 500


        return {"result" : "success" , 
                "items" : result_list[0]
                } , 200
    