from flask import Flask
from api.utils import dynamo
from dotenv import load_dotenv
import os 
import bcrypt
from time import sleep


#load env variables from .env
load_dotenv()

app = Flask(__name__)

# import env variables
app.config.from_pyfile(os.path.join(os.getcwd(),'api','settings.py'))
    
# init flask_dynamo
# interact with dynamo via app.extensions["dynamo"]
dynamo.Dynamo(app)

# create dynamo tables
with app.app_context():
    if os.getenv("BOOTSTRAP","TEARDOWN") == "BUILD":
        # create dynamo table
        app.extensions["dynamo"].table.create_table()
        while True:
            if app.extensions["dynamo"].table.table_exists():
                break
            sleep(10)
        # create default admin
        password = bytes("supersecret",'utf-8')
        # hash default password
        hashed = bcrypt.hashpw(password, bcrypt.gensalt(14)).decode("utf-8")
        app.extensions["dynamo"].table.load("admin:USER",username="admin",password=hashed)
    else:
        app.extensions["dynamo"].table.delete_table()