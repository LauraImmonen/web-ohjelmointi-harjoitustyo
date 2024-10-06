from flask import request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from all_queries import queries
from all_queries import teacher_queries
from flask import render_template
from db import db
from flask import session
from flask import Blueprint, redirect, url_for

teacher_routes = Blueprint('teacher_routes', __name__)

@teacher_routes.route('/logout', methods=["POST"])
def logout_teacher():
    del session["username"]
    return redirect(url_for('index')) 

def is_admin():
    username = session.get('username')

    if not username:
        return False

    user_admin = queries.get_user_admin_status(username)

    if user_admin and user_admin[0] == "True":
        return True
    
    return False


@teacher_routes.route("/teacher_front_page")
def teacher_front_page():
    if is_admin():
        return render_template("teacher_page.html")
    else:
        return "Unauthorized Access" 
    
    
@teacher_routes.route("/create_course", methods=["GET", "POST"])
def create_course():
    if not is_admin():
        return "Unauthorized Access" 
    
    if request.method == "POST":
        course_name = request.form["course_name"]
        course_description = request.form["course_description"]
        teacher_username = session.get("username")  
        
        existing_course = teacher_queries.existing_course(course_name)
            
        if existing_course:
            flash("There is already a course with this name, please choose a different name.")
            return redirect(url_for("teacher_routes.create_course"))
        
        teacher_id = teacher_queries.get_teacher_id(teacher_username)
        
        teacher_queries.insert_into_courses(course_name, course_description, teacher_id)
        
        return redirect(url_for("teacher_routes.course_created"))
    
    return render_template("create_course.html")
    
    
@teacher_routes.route("/course_created")
def course_created():
    if not is_admin():
        return "Unauthorized Access" 
    
    return render_template("course_created.html")
    
    
@teacher_routes.route("/courses_list_teachers", methods=["GET"])
def courses_list_teachers():
    if not is_admin():
        return "Unauthorized Access"
    
    username = session.get("username")
    
    teacher_id = teacher_queries.get_teacher_id(username)
    
    courses = teacher_queries.get_course_by_teacher_id(teacher_id)
    
    if not courses:
        flash("You haven't created any courses yet.")
        
    return render_template("courses_list_teachers.html", courses = courses)
     
    
@teacher_routes.route("/edit_course/<int:course_id>", methods=["GET", "POST"])      
def edit_course(course_id):
    if not is_admin():
        return "Unauthorized Access"
    
    if request.method == "GET":
        course = queries.get_coursename_by_id(course_id)  
        course_description = queries.get_course_description(course_id)[0]
        
        if course:
            
            course_name = course[0]  
           
            return render_template("edit_course.html", course_name = course_name,
                                   course_description = course_description, course_id = course_id)
    
    if request.method == "POST":
        course_name = request.form.get("course_name")
        course_description = request.form.get("course_description")
        
        teacher_queries.update_course(course_id, course_name, course_description)
        
        flash("Course updated successfully!")
        return redirect(url_for('teacher_routes.courses_list_teachers'))



@teacher_routes.route("/confirm_delete_course/<int:course_id>", methods=["GET","POST"])
def confirm_delete_course(course_id):
    if not is_admin():
        return "Unauthorized Access"
    
    course = queries.get_course_name_description(course_id)
    course_name = queries.get_coursename_by_id(course_id)[0]

    if not course:
        return "Course not found."

    return render_template("delete_course.html", course_id = course_id, course = course, course_name = course_name)

        
@teacher_routes.route("/delete_course/<int:course_id>", methods=["POST"])
def delete_course(course_id):
    if not is_admin():
        return "Unauthorized Access"
    
    student_count = teacher_queries.check_enrollments(course_id)
    student_count = teacher_queries.check_enrollments(course_id)
    print(f"Number of enrolled students: {student_count}") 
    
    if student_count > 0:
        flash("You can't delete this course because there are already students enrolled for this class.")
        return redirect(url_for("teacher_routes.courses_list_teachers"))
    
    teacher_queries.delete_course(course_id)
    flash("Course deleted successfully.")
    
    return redirect(url_for("teacher_routes.courses_list_teachers"))


@teacher_routes.route("/grade_course/<int:course_id>", methods = ["GET"])
def grade_course(course_id):
    if not is_admin():
        return "Unauthorized Access"
    
    course_name = queries.get_coursename_by_id(course_id)
    
    students = teacher_queries.get_students_by_course_id(course_id)
    
    if not students:
        flash("There are no students enrolled in your class yet.")
        return redirect(url_for("teacher_routes.courses_list_teachers"))
    
    return render_template("grade_course.html", course_id = course_id, course_name = course_name[0], students = students)
        

@teacher_routes.route("/save_grades/<int:course_id>", methods=["POST"])
def save_grades(course_id):
    if not is_admin():
        return "Unauthorized Access"

    username = session.get('username')
    
    teacher_id = teacher_queries.get_teacher_id(username)

    grades = request.form.getlist('grades')

    for grade_entry in grades:
        student_id, grade = grade_entry.split(',')
        
        existing_grade_count = teacher_queries.check_existing_grade(student_id, course_id)
        
        if existing_grade_count > 0:
            flash("This student has already received a grade from this course.")
            continue

        teacher_queries.insert_grade(student_id, course_id, teacher_id, grade)

    db.session.commit()
    db.session.commit()
    flash("Grades were saved succesfully.")
    
    return redirect(url_for('teacher_routes.courses_list_teachers'))


@teacher_routes.route("/delete_student/<int:course_id>", methods=["GET"])
def delete_student(course_id):
    if not is_admin():
        return "Unauthorized Access"
    
    course_name = queries.get_coursename_by_id(course_id)[0]
    
    students = teacher_queries.get_students_by_course_id(course_id)
    
    if not students:
        flash("There are no students enrolled in your class yet.")
        return redirect(url_for("teacher_routes.courses_list_teachers"))

    return render_template("delete_student.html", course_name=course_name, students=students, course_id=course_id)


@teacher_routes.route("/delete_student_confirm/<int:course_id>", methods=["POST"])
def delete_student_confirm(course_id):
    if not is_admin():
        return "Unauthorized Access"
    
    student_id = request.form.get('student_id')

    return render_template("confirm_delete_student.html", course_id=course_id, student_id=student_id)


@teacher_routes.route("/delete_student_final/<int:course_id>/<int:student_id>", methods=["POST"])
def delete_student_final(course_id, student_id):
    if not is_admin():
        return "Unauthorized Access"

    teacher_queries.delete_enrollment(course_id, student_id)

    return redirect(url_for('teacher_routes.delete_student', course_id=course_id))

