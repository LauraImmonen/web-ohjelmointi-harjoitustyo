from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from all_queries import queries
from flask import render_template
from flask import session
from werkzeug.security import check_password_hash
main_routes = Blueprint('main_routes', __name__)

@main_routes.route("/")
def index():
    return render_template("front_page.html")


@main_routes.route("/account", methods=["POST"])
def have_account():
    have_account = request.form.get("onko_tunnusta")
    if have_account == "Ei":
        return redirect(url_for("main_routes.new_account"))
    elif have_account == "Kyllä":
        return redirect(url_for("main_routes.login"))
    
    
@main_routes.route("/new_account", methods=["GET", "POST"])
def new_account():
    if request.method == 'POST':
        username = request.form["username"]
        admin = request.form["admin"]
        password = request.form["salasana"]
        hash_value = generate_password_hash(password)

        if queries.get_user_id(username):
            flash("Username already exists, please choose another username.")
            return redirect(url_for("main_routes.new_account"))
        else:
            queries.new_user(username, hash_value, admin)
        
        user_id = queries.get_user_id(username)[0]
        
        if admin == "True":
            queries.add_teacher(user_id, username)
        else:
            queries.add_student(user_id, username)

        return redirect(url_for("main_routes.login"))

    return render_template("create_user.html")


def is_admin():
    username = session.get('username')

    if not username:
        return False

    user_admin = queries.get_user_admin_status(username)

    if user_admin and user_admin[0] == "True":
        return True
    
    return False


@main_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = queries.get_user_by_username(username)
        
        if not user:
            flash("Invalid username")  
            return redirect(url_for("main_routes.login"))
        else:
            hash_value = user.password
            
            if check_password_hash(hash_value, password):
                session['username'] = username
                
                if is_admin():
                    return redirect(url_for("teacher_routes.teacher_front_page"))
                else:
                    return redirect(url_for("student_routes.student_front_page"))
            else:
                flash("Invalid password")  
                return redirect(url_for("main_routes.login"))
            
    
    return render_template("login_html.html")




