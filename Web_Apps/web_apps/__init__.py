#### __INIT__.py creates and setups the app and the database (along with the migration and stuff)

from flask import Flask
#ORM & Migration
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import os

#Login : User Authentication 
from flask_login import LoginManager

#Password Hashing
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

#App initialization
app  = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SECRET_KEY"] = "winux"
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['BASE_DIR'] = base_dir

#Data Base Configuration
db_dir = os.path.join(base_dir, "database.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + db_dir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Migration
Migrate(app, db)
 
#User Auth
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.signin'


#Blueprint configuration
from web_apps.Flowers_Recognition.views import flowers_blueprints
from web_apps.Users.views import users_blueprints

app.register_blueprint(flowers_blueprints, url_prefix = '/Flowers')
app.register_blueprint(users_blueprints, url_prefix = '/')









