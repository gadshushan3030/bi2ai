import logging
from flask import Flask
from api.src.core.validations import is_valid_payload
from api.src.core.exceptions import *

app = Flask(__name__)


@app.route('/')
def index():
    return 'BI2AI API'


@app.route('/login', methods=['POST'])
def login(request):
    payload = request.get_json(force=True, silent=True)
    # Validate the payload (group is the current endpoint path)
    validation_result, validation_errors = is_valid_payload(payload, group='/login')
    if validation_result is False:
        logging.error(f"api.hosts.add_host: Validation errors were found {validation_errors}")
        raise ValidationError(validation_errors)
    # Check the payload
    if payload.get('username') == 'kiril' or payload.get('username') == 'gad':
        return f"Welcome {payload.get('usernamee')}"
    else:
        return 'Wrong'


if __name__ == "__main__":
    app.run()
