from flask import Flask
from api.utils import dynamo
from dotenv import load_dotenv
import os 

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
        app.extensions["dynamo"].table.create_table()
    else:
        app.extensions["dynamo"].table.delete_table()