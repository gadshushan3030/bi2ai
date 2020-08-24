import logging

from flask import Flask
from flask import request as flask_request, jsonify, make_response

from api.src.core import config
from api.src.core.exceptions import *
from api.src.core.validations import is_valid_payload

from api.src.modules import users_module
from api.src.modules.tokens_module import create_token

from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token,jwt_refresh_token_required, get_raw_jwt)
from api.src.modules.users_module import get_by_username

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)
blacklist = set()

# For this example, we are just checking if the tokens jti
# (unique identifier) is in the blacklist set. This could
# be made more complex, for example storing all tokens
# into the blacklist with a revoked status when created,
# and returning the revoked status in this call. This
# would allow you to have a list of all created tokens,
# and to consider tokens that aren't in the blacklist
# (aka tokens you didn't create) as revoked. These are
# just two options, and this can be tailored to whatever
# your application needs.


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/')
def index():
    return 'BI2AI API'


@app.route('/login', methods=['POST'])
def login():
    try:
        payload = flask_request.get_json(force=True, silent=True)
        # Validate the payload (group is the current endpoint path)
        validation_result, validation_errors = is_valid_payload(payload, group='/login')
        if validation_result is False:
            logging.error(f"api.hosts.add_host: Validation errors were found {validation_errors}")
            raise ValidationError(validation_errors)
        # Check the payload
        username = users_module.get_by_username(payload.get('username'))
        if username is None:
            raise NotFoundError(f"The username {payload.get('username')} was not found")

        auth = flask_request.authorization
        if auth and auth.password == 'password':
            token = create_token(username.get('user_id'))
            return jsonify(token), 200
        return make_response('Could not verify!', 401, {'WWW-authenticate': 'Basic realm = " Login requires "'})

    except ValidationError as errors:
        return jsonify({
            "status": False,
            "errors": dict(errors.args[0])
        }), config.API_STATUS_BAD_REQUEST
    except NotFoundError as error:
        return jsonify({
            "status": False,
            "errors": str(error)
        }), config.API_STATUS_NOT_FOUND
    except AuthorizationError as error:
        return jsonify({
            "status": False,
            "errors": str(error)
        }), config.API_STATUS_UNAUTHORIZED


# Standard refresh endpoint. A blacklisted refresh token
# will not be able to access this endpoint
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    print(current_user)
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


# Endpoint for revoking the current users access token
@app.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


# Endpoint for revoking the current users refresh token
@app.route('/logout2', methods=['DELETE'])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


# This will now prevent users with blacklisted tokens from
# accessing this endpoint
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({'hello': 'world'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
