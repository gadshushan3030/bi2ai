# API_RESPONSE_HEADERS: Collection of response headers added to every API response
API_RESPONSE_HEADERS = {
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json; charset=utf-8'
}

# API_STATUS_OK: Successful API response http status code
API_STATUS_OK = 200

# API_STATUS_BAD_REQUEST: Malformed request body
API_STATUS_BAD_REQUEST = 400

# API_STATUS_BAD_REQUEST: Authorization access token is missing or expired
API_STATUS_UNAUTHORIZED = 401

# API_STATUS_FORBIDDEN: Operation is forbidden since the user has insufficient level of permissions
API_STATUS_FORBIDDEN = 403

# API_STATUS_BAD_REQUEST: The requested resource could not be found
API_STATUS_NOT_FOUND = 404

# API_STATUS_BAD_REQUEST: One of the external 3rd party services is unavailable
API_STATUS_SERVICE_UNAVAILABLE = 503
