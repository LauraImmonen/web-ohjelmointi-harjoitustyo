from db import db
from sqlalchemy.sql import text

def get_student_id(username):
    sql_get_student_id = """
    SELECT student_id
    FROM students
    WHERE username = :username"""
    result = db.session.execute(text(sql_get_student_id), {"username":username})
    return result.fetchone()

def get_student_courses(student_id):
    sql_get_student_courses = """
        SELECT courses.course, courses.course_description, grades.grade
        FROM courses
        JOIN enrollments ON courses.course_id = enrollments.course_id
        JOIN students ON enrollments.student_id = students.student_id
        LEFT JOIN grades ON courses.course_id = grades.course_id
        AND students.student_id = grades.student_id
        WHERE students.student_id = :student_id;
    """
    result = db.session.execute(text(sql_get_student_courses), {"student_id":student_id})
    return result.fetchall()

def get_course_information():
    result = db.session.execute(text("SELECT course_id, course, course_description FROM courses"))
    return result.fetchall()

def check_enrollment(student_id, course_id):
    sql_check = """
    SELECT 1 FROM enrollments
    WHERE student_id = :student_id
    AND course_id = :course_id"""
    return db.session.execute(text(sql_check), {"student_id":student_id[0], "course_id":course_id}).fetchone()

def enroll_for_course(student_id, course_id):
    sql_insert = """
    INSERT INTO enrollments
    (student_id, course_id)
    VALUES (:student_id, :course_id)"""
    db.session.execute(text(sql_insert), {"student_id":student_id[0], "course_id":course_id})
    db.session.commit()