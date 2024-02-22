from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from config import Config
from mysql_connention import get_connection
from mysql.connector import Error

from datetime import datetime

import boto3

# 레시피 업로드
class RecipeResource(Resource):
        
    @jwt_required()
    def post(self) :

        file = request.files.get('photo')  # 파일이 없을 경우 None을 반환하도록 수정
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        recipe = request.form.get('recipe')

        user_id = get_jwt_identity()

        current_time = datetime.now()

        new_file_name = current_time.isoformat().replace(':', '_').replace(' ', '_') + str(user_id) + '.jpg'
        imageURL = None

        if file:
            file.filename = new_file_name
            s3 = boto3.client('s3',
                        aws_access_key_id = Config.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key = Config.AWS_SECRET_ACCESS_KEY )
            
            try:
                s3.upload_fileobj(file, 
                                    Config.S3_BUCKET,
                                    file.filename,
                                    ExtraArgs={'ACL': 'public-read', 
                                                'ContentType': 'image/jpeg'})
                imageURL = Config.S3_LOCATION + new_file_name
            except Exception as e:
                return {'error': str(e)}, 500

        try:
            connection = get_connection()
            query = '''insert into posting
                        (userId, title, imageURL, ingredients, recipe)
                        values
                        (%s,%s,%s,%s,%s);'''
            record = (user_id, title, imageURL, ingredients, recipe)
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            return {'error': str(e)}, 500

        return {'result' : 'success'}, 200
 
# 레시피 수정, 삭제
class MyRecipeResource(Resource):

    # 수정
    @jwt_required()
    def put(self, Myrecipes_id):
        file = request.files.get('photo')
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        recipe = request.form.get('recipe')
        user_id = get_jwt_identity()

        # 파일이 존재하는 경우에만 처리
        if file:
            try:
                # 파일 이름 생성
                current_time = datetime.now()
                new_file_name = current_time.isoformat().replace(':', '_') + str(user_id) + '.jpg'
                file.filename = new_file_name

                # S3에 파일 업로드
                s3 = boto3.client('s3',
                                aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY)
                s3.upload_fileobj(file,
                                Config.S3_BUCKET,
                                file.filename,
                                ExtraArgs={'ACL': 'public-read',
                                            'ContentType': 'image/jpeg'})

                # 이미지 URL 생성
                imageURL = Config.S3_LOCATION + new_file_name
            except Exception as e:
                print(e)
                return {'error': '파일 업로드 실패'}, 500
        else:
            imageURL = None  # 파일이 없는 경우 이미지 URL은 None으로 설정

        try:
            # 데이터베이스 업데이트
            connection = get_connection()
            query = '''UPDATE posting
                        SET title=%s,
                            imageURL=%s,
                            ingredients=%s,
                            recipe=%s
                        WHERE id=%s AND userId=%s;'''
            record = (title, imageURL, ingredients, recipe, Myrecipes_id, user_id)

            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()

            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            return {'error': '데이터베이스 업데이트 실패'}, 500

        return {'result': 'success'}, 200

        

    # 삭제
    @jwt_required()
    def delete(self,Myrecipes_id):
        
        user_id=get_jwt_identity()
        try:
            connection = get_connection()
            query = '''delete from posting
                        where id = %s and userId = %s;'''
            record = (Myrecipes_id,user_id)

            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {'error':str(e)},500
        
        return {'result':'success'},200
