from flask import Flask, send_from_directory
from flask_cors import CORS #comment this on deployment
from flask_jwt_extended import JWTManager
from api.routes import auth,mock
from flask_jwt_extended import current_user,get_jwt,create_access_token,set_access_cookies
from api.utils import dynamo
from datetime import datetime
from datetime import timedelta
from datetime import timezone


# app factory pattern
def create_app():
    
    app = Flask(__name__,static_url_path='',static_folder='../client/build')
    
    # import env variables
    app.config.from_pyfile('settings.py')
    
    # init dynamo plugin
    # interact with dynamo via app.extensions["dynamo"]
    dynamo.Dynamo(app)

    #jwt setup
    jwt = JWTManager(app)

    # Register a callback function that takes whatever object is passed in as the
    # identity when creating JWTs and converts it to a JSON serializable format.
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user["username"]

    # Register a callback function that loads a user from your database whenever
    # a protected route is accessed. This should return any python object on a
    # successful lookup, or None if the lookup failed for any reason (for example
    # if the user has been deleted from the database).
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        print(identity)
        try:
            return app.extensions["dynamo"].table.query(f"{identity}:USER")[0]
        except Exception as e:
            print('error',e)
            return None

    # Using an `after_request` callback, we refresh any token that is within 30
    # minutes of expiring. Change the timedeltas to match the needs of your application.
    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=current_user)
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original respone
            return response

    app.url_map.strict_slashes = False

    # Allow CORS requests to this API
    CORS(app,supports_credentials=True) #comment this on deployment

    # Add all endpoints form the API with a "api" prefix
    app.register_blueprint(auth.api, url_prefix='/api')
    app.register_blueprint(mock.api, url_prefix='/api')

    # serve React app via the client/build dir
    @app.route("/", defaults={'path':''})
    def serve(path):
        return send_from_directory(app.static_folder,'index.html')
    return app