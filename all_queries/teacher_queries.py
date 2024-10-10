from db import db
from sqlalchemy.sql import text

def get_teacher_id(teacher_username):
    sql_get_teacher_id = "SELECT teacher_id FROM teachers WHERE username = :username"
    result = db.session.execute(text(sql_get_teacher_id ), {"username": teacher_username})
    return result.fetchone()[0]


def existing_course(course_name):
    sql_get_course = "SELECT course FROM courses WHERE course = :course_name"
    result = db.session.execute(text(sql_get_course), {"course_name": course_name})
    return result.fetchone()

def insert_into_courses(course_name, course_description,teacher_id):
    sql_insert = "INSERT INTO courses (course, course_description, teacher_id) VALUES (:course_name, :course_description, :teacher_id)"
    db.session.execute(text(sql_insert), {"course_name": course_name,"course_description": course_description,"teacher_id": teacher_id})
    db.session.commit()

def get_course_by_teacher_id(teacher_id):
    sql_get_courses = "SELECT course_id, course, course_description FROM courses WHERE teacher_id = :teacher_id ORDER BY course_id"
    result = db.session.execute(text(sql_get_courses), {"teacher_id": teacher_id})
    return result.fetchall()

def update_course(course_id, course_name, course_description):
    sql_update_course = "UPDATE courses SET course = :course_name, course_description = :course_description WHERE course_id = :course_id"
    db.session.execute(text(sql_update_course), {
        "course_id": course_id,
        "course_name": course_name,
        "course_description": course_description
    })
    db.session.commit()

def check_enrollments(course_id):
    sql_check_enrollments = "SELECT COUNT(*) FROM enrollments WHERE course_id = :course_id"
    result = db.session.execute(text(sql_check_enrollments), {"course_id": course_id})
    return result.scalar()

def delete_course(course_id):
    sql_delete = "DELETE FROM courses WHERE course_id = :course_id"
    db.session.execute(text(sql_delete), {"course_id": course_id})
    db.session.commit()

def get_students_by_course_id(course_id):
    sql_get_students = """
        SELECT s.student_id, u.username
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN users u ON s.username = u.username
        WHERE e.course_id = :course_id"""
    result = db.session.execute(text(sql_get_students), {"course_id" : course_id})
    return result.fetchall()

def check_existing_grade(student_id, course_id):
    sql_check_existing_grade = """SELECT COUNT(*) FROM grades WHERE student_id = :student_id AND course_id = :course_id"""
    return db.session.execute(text(sql_check_existing_grade),{"student_id": student_id, "course_id": course_id}).scalar()

def insert_grade(student_id, course_id, teacher_id, grade):
    sql_insert_grade = """
            INSERT INTO grades (student_id, course_id, teacher_id, grade)
            VALUES (:student_id, :course_id, :teacher_id, :grade)"""
    db.session.execute(text(sql_insert_grade), {"student_id": student_id, "course_id": course_id, "teacher_id": teacher_id, "grade": grade})

def delete_enrollment(course_id, student_id):
    sql_delete_enrollment = "DELETE FROM enrollments WHERE course_id = :course_id AND student_id = :student_id"
    db.session.execute(text(sql_delete_enrollment), {"course_id": course_id, "student_id": student_id})
    db.session.commit()