import jwt
import datetime
from api.src.core.exceptions import AuthorizationError


BI2AI_JWT_SECRET = 'blabla123'
BI2AI_JWT_EXPIRE_MINUTES = 7200


def create_token(user_id):
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=BI2AI_JWT_EXPIRE_MINUTES)
    }, BI2AI_JWT_SECRET)
    return token


def parse_token(jwt_token):
    try:
        payload = jwt.decode(jwt_token)
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        raise AuthorizationError("Access token is expired")
