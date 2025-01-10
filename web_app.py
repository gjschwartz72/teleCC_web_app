from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key_for_csrf_token_required_for_form_data'

db_path = os.path.abspath("synthetic_data/teleCC.sqlite")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

# Track modifications is often unnecessary and can be disabled
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from routes import *

#print(app.url_map) #This prints all of the modules avaialable to the app.

if __name__ == '__main__':
    app.run(debug = True)