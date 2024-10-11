from db import db
from sqlalchemy.sql import text


def new_user(username, hash_value, admin):
    sql_insert = """INSERT INTO users (username, password, admin)
    VALUES (:username, :password, :admin)"""
    db.session.execute(text(sql_insert), {"username": username, "password": hash_value, "admin": admin})
    db.session.commit()

def get_user_id(username):
    sql_get_user_id = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(text(sql_get_user_id), {"username": username})
    user_id = result.fetchone()
    if user_id:
        return user_id
    False

def add_teacher(user_id, username):
    sql_insert = "INSERT INTO teachers (teacher_id, username) VALUES (:teacher_id, :username)"
    db.session.execute(text(sql_insert), {"teacher_id": user_id, "username": username})
    db.session.commit()

def add_student(user_id, username):
    sql_insert = "INSERT INTO students (student_id, username) VALUES (:student_id, :username)"
    db.session.execute(text(sql_insert), {"student_id": user_id, "username": username})
    db.session.commit()

def get_user_admin_status(username):
    sql_get_user_admin = "SELECT admin FROM users WHERE username = :username"
    result = db.session.execute(text(sql_get_user_admin), {"username": username})
    return result.fetchone()

def get_user_by_username(username):
    sql_get_user = text("SELECT id, password FROM users WHERE username = :username")
    result = db.session.execute(sql_get_user, {"username": username})
    return result.fetchone()

def get_course_id(course_name):
    sql_get_course_id = "SELECT course_id FROM courses WHERE course = :course_name"
    result = db.session.execute(text(sql_get_course_id), {"course_name": course_name})
    return result.fetchone()

def get_coursename_by_id(course_id):
    sql_get_course_name = "SELECT course, course_id FROM courses WHERE course_id = :course_id"
    result = db.session.execute(text(sql_get_course_name), {"course_id": course_id})
    return result.fetchone()

def get_course_name_description(course_id):
    sql_get_course = "SELECT course, course_description FROM courses WHERE course_id = :course_id"
    result = db.session.execute(text(sql_get_course), {"course_id": course_id})
    return result.fetchone()

def get_course_description(course_id):
    sql_get_course = "SELECT course_description FROM courses WHERE course_id = :course_id"
    result = db.session.execute(text(sql_get_course), {"course_id": course_id})
    return result.fetchone()