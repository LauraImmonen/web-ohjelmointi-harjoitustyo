from flask import request, render_template, redirect, url_for, flash, abort
from all_queries import queries
from all_queries import student_queries
from flask import render_template
from flask import session
from flask import Blueprint, redirect, url_for

student_routes = Blueprint('student_routes', __name__)

@student_routes.route('/logout')
def logout_student():
    del session["username"]
    return redirect(url_for('main_routes.index'))


def is_admin():
    username = session.get('username')

    if not username:
        return False

    user_admin = queries.get_user_admin_status(username)

    if user_admin and user_admin[0] == "True":
        return True

    return False


@student_routes.route("/student_front_page")
def student_front_page():
    if not is_admin():
        return render_template("student_page.html")
    else:
        return "Luvaton pääsy!"


@student_routes.route("/students_courses", methods=["GET"])
def students_courses():
    if is_admin():
        return "Luvaton pääsy!"

    username = session.get("username")

    student_id = student_queries.get_student_id(username)[0]

    courses = student_queries.get_student_courses(student_id)

    if not courses:
        flash("Et ole vielä ilmoittautunut yhdellekään kurssille.")
        return redirect(url_for("student_routes.student_front_page"))

    return render_template("students_courses.html", courses=courses)


@student_routes.route("/apply_for_course")
def apply_for_course():
    if not is_admin():
        courses = student_queries.get_course_information()
        if not courses:
            flash("Tällä hetkellä ei ole kursseja, joille ilmoittautua.")
            return redirect(url_for("student_queries.student_front_page"))

        return render_template("apply_for_course.html", courses=courses)

    return "Luvaton pääsy!"


@student_routes.route("/enroll/<int:course_id>", methods=["POST"])
def enroll(course_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if is_admin():
        return "Luvaton pääsy!"

    username = session.get("username")

    student_id = student_queries.get_student_id(username)

    if student_id:
        already_enrolled = student_queries.check_enrollment(student_id, course_id)

        if already_enrolled:
            flash("Olet jo ilmoittautunut kurssille.")
            return redirect(url_for("student_routes.apply_for_course"))

    student_queries.enroll_for_course(student_id, course_id)

    return redirect(url_for("student_routes.enrollment_successful"))


@student_routes.route("/enrollment_successful")
def enrollment_successful():
    if is_admin():
        return "Luvaton pääsy!"

    return render_template("enrollment_successful.html")

