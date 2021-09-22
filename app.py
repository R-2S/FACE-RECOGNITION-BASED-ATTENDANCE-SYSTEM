from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
import pymysql
import os


app=Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')

  
@app.route("/log_out")
def log_out():
    session.clear()
    return render_template('home.html')


if __name__=='__main__':
    app.run(debug=True)
