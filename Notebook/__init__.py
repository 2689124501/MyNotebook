from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@127.0.0.1:3306/mynotebook"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SECRET_KEY"] = os.urandom(16)
app.debug = True

# 注册蓝图
from Notebook.index import index as index_blueprint
app.register_blueprint(index_blueprint, url_prefix="/todo/api/v1.0")