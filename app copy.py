import serverless_wsgi

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from resources.favorites import FavoritesResource
from resources.follows import FollowResource
from resources.history import historyTop10
from resources.naver import NaverLogin

from resources.recipelist import MyFavoriteRecipeResource, RecipeDetail, RecipeListMoreShowResource, RecipeListResource, RecipeMeInfo, RecipeMeResource, RecipeResource, UserFollowResoutce, UserProfileResoucre

from resources.recipes import MyRecipeResource, RecipeResource

from resources.review import MyReviewResource, ReviewResource, ReviewlistResource

from resources.user import GoogleLogin, KaKaoLogin, UserDelete, UserPasswordUpdate, jwt_blocklist

from config import Config
from resources.user import UserLoginResource, UserLogoutResource, UserRegisterResource

app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header,jwt_payload):
    jti = jwt_payload['jti']
    return jti in jwt_blocklist

api = Api(app)

# api 작성

api.add_resource( UserRegisterResource, '/user/register')
api.add_resource( UserLoginResource ,'/user/login')
api.add_resource( UserLogoutResource,'/user/logout')
api.add_resource( UserDelete,'/user/delete')
api.add_resource( UserPasswordUpdate,'/user/passwordUpdate')


# 해당 유저의 프로필과 레시피 가져오기
api.add_resource(UserProfileResoucre, '/userprofile/<int:userId>')
# 해당 유저의 팔로우 팔로잉 게시물 수 가져오기
api.add_resource(UserFollowResoutce, '/userfollow/<int:userId>')

#구글 로그인
api.add_resource(GoogleLogin,'/user/googlelogin')
# 카카오 로그인
api.add_resource(KaKaoLogin,'/user/kakaologin')

# 레시피 전체보기(간략히)
api.add_resource(RecipeListResource, '/recipe')
# 레시피 전체보기(더보기)
api.add_resource(RecipeListMoreShowResource, '/recipemore')
# 레시피 상세보기
api.add_resource( RecipeDetail , '/recipe/<int:posting_id>')

# 내 레시피 보기 전 내 정보 불러오기
api.add_resource(RecipeMeInfo,'/myrecipe/myinfo')
# 내 레시피 보기
api.add_resource(RecipeMeResource, '/myrecipe')
# 즐겨찾기한 레시피 보기
api.add_resource(MyFavoriteRecipeResource, '/favoriterecipe')
# 인기검색어 Top10
api.add_resource(historyTop10, '/history')
# 팔로우 
api.add_resource(  FollowResource , '/follow/<int:followee_id>')

# 즐겨찾기 
api.add_resource(FavoritesResource,'/favorites/<int:postingId>')

# 레시피 작성
api.add_resource(RecipeResource, '/recipes/add')
# 레시피 수정,삭제
api.add_resource(MyRecipeResource,'/myrecipes/<int:Myrecipes_id>')

# 댓글 작성
api.add_resource(ReviewResource,'/review/<int:postingId>')
# 댓글 수정, 삭제
api.add_resource(MyReviewResource,'/review/<int:postingId>/<int:reviewId>')
# 전체 댓글 불러오기
api.add_resource(ReviewlistResource, '/review/<int:postingId>')




def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

if __name__ == '__main__':
    app.run()


