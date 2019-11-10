#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 13:28:26 2019

@author: xiaohezhang
"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template



river = 'Andy Zhang'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql+pymysql://root:@localhost/twitter'
db = SQLAlchemy(app)

class Example(db.):
    __tablename__ = 'alltwitter'
    id = db.Column(' ')
@app.route("/")
def home():
    return render_template('20191104map.html')

if __name__ =="__main__":
    app.run()
