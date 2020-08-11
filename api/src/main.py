import logging
from flask import Flask, jsonify
from flask import request as flask_request
from api.src.core.validations import is_valid_payload
from api.src.core.exceptions import *
from api.src.core import config

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
        if payload.get('username') == 'kiril' or payload.get('username') == 'gad':
            return f"Welcome {payload.get('username')}"
        else:
            return 'Wrong!'
    except ValidationError as errors:
        return jsonify({
            "status": False,
            "errors": dict(errors.args[0])
        }), config.API_STATUS_BAD_REQUEST


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
