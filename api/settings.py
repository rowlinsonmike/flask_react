from os import environ 

JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
DYNAMO_USER_TABLE = environ.get('DYNAMO_USER_TABLE')
CORS_HEADERS=environ.get('CORS_HEADERS')
JWT_TOKEN_LOCATION=[environ.get('JWT_TOKEN_LOCATION')]
JWT_COOKIE_SECURE=environ.get('JWT_COOKIE_SECURE')
JWT_COOKIE_CSRF_PROTECT=environ.get('JWT_COOKIE_CSRF_PROTECT')
AWS_REGION=environ.get('AWS_REGION')