from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask import render_template, request, redirect, url_for, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.config['DEBUG'] = True


@app.route("/")
def index():
    return render_template("front_page.html")


@app.route("/account", methods=["POST"])
def onko_tunnusta():
    onko_tunnusta = request.form.get("onko_tunnusta")
    if onko_tunnusta == "Ei":
        return redirect(url_for("new_account"))
    elif onko_tunnusta == "Kyllä":
        return redirect(url_for("login"))
    
    
@app.route("/new_account", methods=["GET", "POST"])
def new_account():
    if request.method == 'POST':
        name = request.form["username"]
        admin = request.form["admin"]
        password = request.form["salasana"]
        hash_value = generate_password_hash(password)

        sql_check = "SELECT 1 FROM users WHERE username=:username"
        result = db.session.execute(text(sql_check), {"username": name})
        existing_user = result.fetchone()
        
        if existing_user:
            return "Username already exists"
        else:
            sql_insert = "INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)"
            db.session.execute(text(sql_insert), {"username": name, "password": hash_value, "admin": admin})
            db.session.commit()
        
        
        sql_get_user_id = "SELECT id FROM users WHERE username=:username"
        result = db.session.execute(text(sql_get_user_id), {"username": name})
        user_id = result.fetchone()[0]
            
        if admin == "True":
            sql_insert = "INSERT INTO teachers (teacher_id, username) VALUES (:teacher_id, :username)"
            db.session.execute(text(sql_insert), {"teacher_id": user_id, "username": name})
            db.session.commit()
        else:
            sql_insert = "INSERT INTO students (student_id, username) VALUES (:student_id, :username)"
            db.session.execute(text(sql_insert), {"student_id": user_id, "username": name})
            db.session.commit()

        return redirect(url_for("login"))

    return render_template("create_user.html")



def is_admin():
    username = session.get('username')
    
    sql_get_user_admin = "SELECT admin FROM users WHERE username=:username"
    result = db.session.execute(text(sql_get_user_admin), {"username": username})
    user_admin = result.fetchone()[0]
    
    if user_admin == "True":
        return True
    else:
        return False



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql_get_user_id = text("SELECT id, password FROM users WHERE username=:username")
        result = db.session.execute(sql_get_user_id, {"username":username})
        user = result.fetchone()    
        if not user:
            "Invalid username"
        else:
            hash_value = user.password
            
            if check_password_hash(hash_value, password):
                session['username'] = username
                
                if is_admin():
                    return redirect(url_for("teacher_front_page"))
                else:
                    return redirect(url_for("student_front_page"))
            else:
                "Invalid password"
            
    
    return render_template("login_html.html")



@app.route("/teacher_front_page")
def teacher_front_page():
    if is_admin():
        return render_template("teacher_page.html")
    else:
        return "Unauthorized Access" 
    
    
    
@app.route("/create_course", methods=["GET", "POST"])
def create_course():
    if not is_admin():
        return "Unauthorized Access" 
    
    if request.method == "POST":
        course_name = request.form["course_name"]
        course_description = request.form["course_description"]
        teacher_username = session.get("username")  
        
        sql_get_course_id = "SELECT course_id FROM courses WHERE course = :course_name"
        result = db.session.execute(text(sql_get_course_id), {"course_name": course_name})
        existing_course = result.fetchone()
        
        if existing_course:
            return "There is already a course with this name, please choose a different name."
        
        sql_get_teacher_id = "SELECT teacher_id FROM teachers WHERE username = :username"
        result = db.session.execute(text(sql_get_teacher_id ), {"username": teacher_username})
        teacher_id = result.fetchone()[0]
        
        sql_insert = "INSERT INTO courses (course, course_description, teacher_id) VALUES (:course_name, :course_description, :teacher_id)"
        db.session.execute(text(sql_insert), {"course_name": course_name,"course_description": course_description,"teacher_id": teacher_id})
        db.session.commit()
        
        return redirect(url_for("course_created"))
    
    return render_template("create_course.html")
    
    
    
@app.route("/course_created")
def course_created():
    if not is_admin():
        return "Unauthorized Access" 
    
    return render_template("course_created.html")
    
    
    
    
@app.route("/courses_list_teachers", methods=["GET"])
def courses_list_teachers():
    if not is_admin():
        return "Unauthorized Access"
    
    username = session.get("username")
    
    sql_get_teacher_id = "SELECT teacher_id FROM teachers WHERE username = :username"
    result = db.session.execute(text(sql_get_teacher_id), {"username": username})
    teacher_id = result.fetchone()
    
    sql_get_courses = "SELECT course_id, course, course_description FROM courses WHERE teacher_id = :teacher_id ORDER BY course_id"
    result = db.session.execute(text(sql_get_courses), {"teacher_id": teacher_id[0]})
    courses = result.fetchall()
    
    return render_template("courses_list_teachers.html", courses = courses)
     
    
     
@app.route("/edit_course/<int:course_id>", methods=["GET", "POST"])      
def edit_course(course_id):
    if not is_admin():
        return "Unauthorized Access"
    
    if request.method == "GET":
    
        sql_get_course_name = "SELECT course, course_id FROM courses WHERE course_id = :course_id"
        result = db.session.execute(text(sql_get_course_name), {"course_id": course_id})
        course = result.fetchone()
        
        if course:
            return render_template("edit_course.html", course = course, course_id = course_id)
    
    if request.method == "POST":
        
        course_description = request.form.get("course_description")
        
        sql_update = "UPDATE courses SET course_description = :course_description WHERE course_id = :course_id"
        db.session.execute(text(sql_update), {"course_description": course_description, "course_id": course_id})
        db.session.commit()
        
        return redirect(url_for("courses_list_teachers")) 

 

        
@app.route("/delete_course/<int:course_id>", methods=["POST"])
def delete_course(course_id):
    if not is_admin():
        return "Unauthorized Access"
    
    sql_check_enrollments = "SELECT COUNT(*) FROM enrollments WHERE course_id = :course_id"
    result = db.session.execute(text(sql_check_enrollments), {"course_id": course_id})
    student_count = result.scalar()

    if student_count > 0:
        return "You can't delete this course because there are already students enrolled for this class."
    
    sql_delete = "DELETE FROM courses WHERE course_id = :course_id"
    db.session.execute(text(sql_delete), {"course_id": course_id})
    db.session.commit()
    
    return redirect(url_for("courses_list_teachers"))

    
    
    
@app.route("/student_front_page")
def student_front_page():
    if not is_admin():
        return render_template("student_page.html")   
    else:
        return "Unauthorized Access" 
    


@app.route("/students_courses", methods = ["GET"])
def students_courses():
    if is_admin():
        return "Unauthorized Access"
   
    username = session.get("username")
    
    sql_get_student_id = "SELECT student_id FROM students WHERE username = :username"
    result = db.session.execute(text(sql_get_student_id), {"username": username})
    student_id = result.fetchone()[0]
    
    
    sql_get_student_courses = """
        SELECT courses.course, courses.course_description, grades.grade
        FROM courses
        JOIN enrollments ON courses.course_id = enrollments.course_id
        JOIN students ON enrollments.student_id = students.student_id
        LEFT JOIN grades ON courses.course_id = grades.course_id 
        AND students.student_id = grades.student_id
        WHERE students.student_id = :student_id;
    """
    
    result = db.session.execute(text(sql_get_student_courses), {"student_id": student_id})
    courses = result.fetchall()

    return render_template("students_courses.html", courses = courses)



@app.route("/apply_for_course")
def apply_for_course():
    if not is_admin():
        result = db.session.execute(text("SELECT course_id, course, course_description FROM courses"))
        courses = result.fetchall()
        
        return render_template("apply_for_course.html", courses=courses)
    
    return "Unauthorized Access"



@app.route("/enroll/<int:course_id>", methods=["POST"])
def enroll(course_id):
    if is_admin():
        return "Unauthorized Access"
    
    username = session.get("username")
    
    sql_get_student_id = "SELECT student_id FROM students WHERE username = :username"
    result = db.session.execute(text(sql_get_student_id), {"username": username})
    student_id = result.fetchone()

    if student_id:
        sql_check = "SELECT 1 FROM enrollments WHERE student_id = :student_id AND course_id = :course_id"
        already_enrolled = db.session.execute(text(sql_check), {"student_id": student_id[0], "course_id": course_id}).fetchone()
        
        if already_enrolled:
            return "You are already enrolled in this course"
        
    sql_insert = "INSERT INTO enrollments (student_id, course_id) VALUES (:student_id, :course_id)"
    db.session.execute(text(sql_insert), {"student_id": student_id[0], "course_id": course_id})
    db.session.commit()
    
    return redirect(url_for("enrollment_successful")) 
     



@app.route("/enrollment_successful")
def enrollment_successful():
    if is_admin():
        return "Unauthorized Access"
    
    return render_template("enrollment_successful.html")



@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
  



