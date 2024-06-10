from app import Flask_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_bcrypt import Bcrypt
 


Flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/hrit'
db = SQLAlchemy(Flask_app)
migrate = Migrate(Flask_app,db)
bcrypt = Bcrypt(Flask_app)
Flask_app.secret_key = 'frybgtuhij'
