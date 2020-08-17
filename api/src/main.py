import logging

from flask import Flask
from flask import request as flask_request, jsonify, make_response

from api.src.core import config
from api.src.core.exceptions import *
from api.src.core.validations import is_valid_payload

from api.src.modules import users_module
from api.src.modules.tokens_module import create_token
from api.src.modules.users_module import set_token

app = Flask(__name__)


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
        user = users_module.get_by_username(payload.get('username'))
        if user is None:
            raise NotFoundError(f"The username {payload.get('username')} was not found")
        print(user.get('user_id'))

        auth = flask_request.authorization
        if auth and auth.password == 'password':
            token = create_token(user.get('user_id'))
            return jsonify({'token': token.decode('UTF-8')}), set_token(token, user.get('user_id'))
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
