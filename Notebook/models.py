import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from Notebook import app
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy(app)

# 事件表
class Events(db.Model):
    __tablename__ = 'events'
    eid = db.Column(db.Integer, primary_key=True, index=True, unique=True, autoincrement=True, nullable=False)  # 事项id
    status = db.Column(db.Boolean, default=False)  # 完成状态 true表示完成 false 表示还没
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    deadline = db.Column(db.DateTime, index=True, nullable=False)  # 截止时间
    event = db.Column(db.Text)


if __name__ == '__main__':
    db.create_all()
