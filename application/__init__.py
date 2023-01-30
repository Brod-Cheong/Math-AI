from flask import Flask
from flask_cors import CORS
import joblib
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#create the Flask app
app = Flask(__name__)
CORS(app)
# load configuration from config.cfg
app.config.from_pyfile('config.cfg')

print(">> Created Flask application and read in the configuration")
db=SQLAlchemy(app)
print(">>>Created SQLAlchemy object")


# joblib_file="./application/static/joblib_model.pkl"
# ai_model=joblib.load(joblib_file)
# print(3)
# print(">> Loaded the trained model")

login_manager = LoginManager()
login_manager.init_app(app)

print(">> Loaded Login Manager")
#run the file routes.py
from application import routes