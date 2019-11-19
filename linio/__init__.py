from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'kjr3krbkr3nr3nrl3nlrn3232nrl323kk'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from linio.admin import routes