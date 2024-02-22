import base64
from flask import Flask, jsonify, redirect, request
from flask_restful import Resource
import requests

class NaverLogin(Resource):
    # NAVER_CLIENT_ID = "lvlXKbxzsfeexwIET9zZ"
    # NAVER_CLIENT_SECRET = "K2ho6DDSQR"
    # NAVER_REDIRECT_URI = "http://localhost:5000"

    def get_naver_user_info(self, access_token):
        user_info_url = "https://openapi.naver.com/v1/nid/me"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(user_info_url, headers=headers)
        user_info_json = response.json()

        return user_info_json

    def get(self):

        NAVER_CLIENT_ID = "lvlXKbxzsfeexwIET9zZ"
        NAVER_REDIRECT_URI = "http://localhost:5000/recipe"
        
        naver_login_url = f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={NAVER_CLIENT_ID}&redirect_uri={NAVER_REDIRECT_URI}&state=YOUR_STATE"
        return redirect(naver_login_url)

    def callback(self):

        NAVER_CLIENT_ID = "lvlXKbxzsfeexwIET9zZ"
        NAVER_CLIENT_SECRET = "K2ho6DDSQR"
        NAVER_REDIRECT_URI = "http://localhost:5000/recipe"
       

        code = request.args.get("code")
        state = request.args.get("state")

        token_url = "https://nid.naver.com/oauth2.0/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": NAVER_CLIENT_ID,
            "client_secret": NAVER_CLIENT_SECRET,
            "code": code,
            "state": state,
            "redirect_uri": NAVER_REDIRECT_URI,
        }

        response = requests.post(token_url, data=data)
        token_json = response.json()

        if "access_token" in token_json:
            access_token = token_json["access_token"]
            user_info = self.get_naver_user_info(access_token)  # 수정된 부분
            return jsonify(user_info)
        else:
            return jsonify({"error": "Failed to obtain access token"}), 400