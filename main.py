from flask import Flask,render_template,request,session,redirect,url_for,Response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import os
import matplotlib.pyplot as plt
from sqlalchemy import func


db=SQLAlchemy()
DB_NAME= 'database.db'
app = Flask(__name__)
app.config['SECRET_KEY']='bene'
app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


adminkey='z'

username=''

def create_database(app):
    db.init_app(app)
    if not path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
        print("Database creaated")

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True)
    fullName=db.Column(db.String(100))
    password=db.Column(db.String(100))
    username=db.Column(db.String(100))
    
    
class Student(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    RegNo = db.Column(db.String(10),nullable=False)
    Name = db.Column(db.String(50),nullable=False)
    MAT206 = db.Column(db.String(10),nullable=False)
    CST202 = db.Column(db.String(10),nullable=False)
    CST204 = db.Column(db.String(10),nullable=False)
    CST206 = db.Column(db.String(10),nullable=False)
    EST200 = db.Column(db.String(10),nullable=False)
    MCN202 = db.Column(db.String(10),nullable=False)
    CSL202 = db.Column(db.String(10),nullable=False)
    CSL204 = db.Column(db.String(10),nullable=False)
    Earned_Credits = db.Column(db.Integer,nullable=False)
    Cumilative_Credits = db.Column(db.Integer,nullable=False)
    SGPA = db.Column(db.Integer,nullable=False)
    CGPA = db.Column(db.Integer,nullable=False)
    # User_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/")
def home():
  return render_template('index.html')

@app.route("/dash",methods=['GET','POST'])
@login_required
def dash():
  name = User.query.filter_by().first()
  return render_template('dash.html')

@app.route("/about")
def about():
  return render_template('about.html')

@app.route("/contact")
def contact():
  return render_template('contact.html')



@app.route("/logins")
def logins():
  return render_template('logins.html')

@app.route("/logint", methods=['GET', 'POST'])
def logint():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user:
        if user.password == password:
          login_user(user, remember=True)
          return redirect('/dash')
        else:
          print('Wrong pass')
  return render_template('logint.html')

@app.route("/register", methods=["POST", "GET"])
def register():
  if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email   = request.form['email']
        fullName   = request.form['fullName']
        adminkey = request.form['adminkey']
        if adminkey != 'aisat123':
            return redirect(url_for('logint'))
        new_user=User(username=username,password=password,email=email,fullName=fullName)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('logint'))

  else:
      return render_template('register.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
#   df = None
#   if request.method == 'POST':
#         # Access the uploaded file
#         file = request.files['csv_file']
#         sem=request.form.get("semester")
#         bat=request.form.get("batch")


#         # Save the file to the static/files folder
#         filename = f"s{sem}b{bat}.csv"
#         #filename = secure_filename(file.filename)
#         file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)

#         print(filename)
#         # Process the file (e.g., read and manipulate the CSV data)
#         df = pd.read_csv(file_path)
#         print(df)

# #         grades = df['sub1'].values

# # # Define the condition for failing grades
#         condition = grades < 60

# # Get the values that satisfy the condition
#         failed_grades = grades[condition]

# # Count the number of failing grades
#         num_failed = len(failed_grades)

#         print("Number of people failed:", num_failed)
#         # Your processing logic goes here

#         numpy_array = df.to_numpy()
        #return "File uploaded and processed successfully!"
  # return render_template('upload.html')
  if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)
        for index, row in df.iterrows():
            data = Student(
                        RegNo = row['RegNo'], Name=row['Name'],
                        MAT206 = row['MAT206'],
                        CST202 = row['CST202'],
                        CST204 = row['CST204'],
                        CST206 = row['CST206'],
                        EST200 = row['EST200'],
                        MCN202 = row['MCN202'],
                        CSL202 = row['CSL202'],
                        CSL204 = row['CSL204'],
                        Earned_Credits = row['Earned_Credits'],
                        Cumilative_Credits = row['Cumilative_Credits'],
                        SGPA = row['SGPA'],
                        CGPA = row['CGPA']
                        )
            db.session.add(data)
            db.session.commit()
        # return 'Data added to database!'
  return render_template("upload.html")


@app.route("/tables")                   #display table
def tables():
    data = Student.query.all()
    return render_template('tables.html', data=data)



# @app.route('/view', methods=['GET', 'POST'])
# def view():

#   if request.method == 'POST':
#     sem=request.form.get("semester")
#     bat=request.form.get("batch")
#     print(sem,bat)
#     filename = "static/files/"+f"s{sem}b{bat}.csv"
#     print(filename)
#     df=pd.read_csv(filename);
#     df2=df.to_numpy()
#     df2=df2.tolist()
#     count=0
#     for i in range(len(df2)):
#       if(df2[i][1] in "F"):
#         print(df2[i][0],df2[i][1])
#         count+=1
#     print(f"Total failures in mat206: {count}")
#     return df.to_html()
    
#   return render_template('view.html')

  
@app.route('/f_grade', methods=['GET'])
def f_grade():
    students_f_grade = Student.query.filter(
        ( Student.MAT206.ilike( 'F' ) ) |
        ( Student.CST202.ilike( 'F' ) ) |
        ( Student.CST204.ilike( 'F' ) ) |
        ( Student.CST206.ilike( 'F' ) ) |
        ( Student.EST200.ilike( 'F' ) ) |
        ( Student.MCN202.ilike( 'F' ) ) |
        ( Student.CSL202.ilike( 'F' ) ) |
        ( Student.CSL204.ilike( 'F' ) ) 
    ).all()
    
    return render_template('F_grade.html', students=students_f_grade)

@app.route('/fe_grade', methods=['GET'])
def fe_grade():
    students_fe_grade = Student.query.filter(
        ( Student.MAT206.ilike( 'FE' ) ) |
        ( Student.CST202.ilike( 'FE' ) ) |
        ( Student.CST204.ilike( 'FE' ) ) |
        ( Student.CST206.ilike( 'FE' ) ) |
        ( Student.EST200.ilike( 'FE' ) ) |
        ( Student.MCN202.ilike( 'FE' ) ) |
        ( Student.CSL202.ilike( 'FE' ) ) |
        ( Student.CSL204.ilike( 'FE' ) ) 
    ).all()
    
    return render_template('Fe_grade.html', students=students_fe_grade)

@app.route('/2ff_grade', methods=['GET'])
def ff2_grade():
    all_students = Student.query.all()
    students_2f_grade = []

    for student in all_students:
        subjects = [
            student.MAT206, student.CST202, student.CST204,
            student.CST206, student.EST200, student.MCN202,
            student.CSL202, student.CSL204
        ]
        f_count = subjects.count('F')
        if f_count == 3:
            students_2f_grade.append(student)

    return render_template('test.html', students=students_2f_grade)


@app.route('/2f_grade', methods=['GET'])
def f2_grade():
    students_2f_grade = Student.query.filter(
        (func.length(func.replace(Student.MAT206, 'F', '')) == 2) +
        (func.length(func.replace(Student.CST202, 'F', '')) == 2) +
        (func.length(func.replace(Student.CST204, 'F', '')) == 2) +
        (func.length(func.replace(Student.CST206, 'F', '')) == 2) +
        (func.length(func.replace(Student.EST200, 'F', '')) == 2) +
        (func.length(func.replace(Student.MCN202, 'F', '')) == 2) +
        (func.length(func.replace(Student.CSL202, 'F', '')) == 2) +
        (func.length(func.replace(Student.CSL204, 'F', '')) == 2)
    ).all()


    return render_template('f_grade.html', students=students_2f_grade)

  
def filter_students(count: int):
    all_students = Student.query.all()
    students_2f_grade = []

    for student in all_students:
        subjects = [
            student.MAT206, student.CST202, student.CST204,
            student.CST206, student.EST200, student.MCN202,
            student.CSL202, student.CSL204
        ]
        f_count = subjects.count('F')
        if f_count == count:
            students_2f_grade.append(student)
            
    return students_2f_grade

@app.route('/filter_By_Grade', methods=['GET','POST'])
def filter_By_Grade():
    if request.method == 'POST':
       Selct_value = request.form.get('Select_value')
       text = ''
       if Selct_value == "1":
            return redirect('/')
       elif Selct_value == "2":
            return redirect('/f_grade')
       elif Selct_value == "3":
            students = filter_students(1)
            return render_template('filter_grade.html', students = students)
       elif Selct_value == "4":
            students = filter_students(2)
            return render_template('filter_grade.html', students = students)
       elif Selct_value == "5":
            students = filter_students(3)
            return render_template('filter_grade.html', students = students)
       elif Selct_value == "6":
            students = filter_students(4)
            return render_template('filter_grade.html', students = students)
       elif Selct_value == "7":
            students = filter_students(5)
            return render_template('filter_grade.html', students = students)
       elif Selct_value == "9":
            return redirect('/fe_grade')
        #elif Select_value == "8":
        #   students = filter_students(6)
        #   return render_template('filter_grade.html', students = students)
        
    return render_template('filter_grade.html')

@app.route('/filter')
def filter():
    students_f_grade_count = Student.query.filter(
        ( Student.MAT206.ilike( 'F' ) ) |
        ( Student.CST202.ilike( 'F' ) ) |
        ( Student.CST204.ilike( 'F' ) ) |
        ( Student.CST206.ilike( 'F' ) ) |
        ( Student.EST200.ilike( 'F' ) ) |
        ( Student.MCN202.ilike( 'F' ) ) |
        ( Student.CSL202.ilike( 'F' ) ) |
        ( Student.CSL204.ilike( 'F' ) ) 
    ).count()
    students_f_grade_data = Student.query.filter(
        ( Student.MAT206.ilike( 'F' ) ) |
        ( Student.CST202.ilike( 'F' ) ) |
        ( Student.CST204.ilike( 'F' ) ) |
        ( Student.CST206.ilike( 'F' ) ) |
        ( Student.EST200.ilike( 'F' ) ) |
        ( Student.MCN202.ilike( 'F' ) ) |
        ( Student.CSL202.ilike( 'F' ) ) |
        ( Student.CSL204.ilike( 'F' ) ) 
    ).all()
    print ("students_f_grade_count: ", students_f_grade_count)
    return render_template('filter_grade.html')
                 

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('home'))

# main driver function
if __name__ == '__main__':
    create_database(app)
    app.run(debug=False)