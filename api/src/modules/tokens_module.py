from flask_jwt_extended import create_access_token, create_refresh_token

BI2AI_JWT_BLACKLIST_ENABLED = True


def create_token(user_id):
    access_token = create_access_token(identity=user_id)
    refresh_token= create_refresh_token(identity=user_id)
    return access_token, refresh_token




