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


@app.route("/student_signup", methods=['GET', 'POST'])
def student_signup():
    try:
        db = pymysql.connect(host='localhost',
                                 user='root',
                                 password='secret',
                                 db='attendance_db')
        
        if (request.method == 'POST'):
            reg_no = request.form.get('reg_no')
            name = request.form.get('name')
            email = request.form.get('email')
            contact_no = request.form.get('contact_no')
            varsity = request.form.get('varsity')
            password = request.form.get('password')
            picture_1 = request.files['picture_1']
            picture_2 = request.files['picture_2']
            picture_3 = request.files['picture_3']

            filename_1 = secure_filename(picture_1.filename)
            picture_1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_1))

            filename_2 = secure_filename(picture_2.filename)
            picture_2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_2))

            filename_3 = secure_filename(picture_3.filename)
            picture_3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_3))
            
            cursor = db.cursor()
            sql = "INSERT INTO students VALUES(%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (reg_no, name, email, contact_no, varsity, password))
            db.commit()

            message = "Account Created Successfully"
            return render_template('home.html', message=message)
            db.close()
        else:
            return "Something Went Wrong."
            
    except Exception as e:
        print(e)

    return "NOT DONE!!"


if __name__=='__main__':
    app.run(debug=True)
