from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.routes import user_routes, post_routes

app.register_blueprint(user_routes)
app.register_blueprint(post_routes)

from app import models