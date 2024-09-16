from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///koulusovellus_db"
db = SQLAlchemy(app)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template("etusivu.html")


@app.route("/tunnus", methods=["POST"])
def onko_tunnusta():
    onko_tunnusta = request.form.get("onko_tunnusta")
    if onko_tunnusta == "Ei":
        return redirect(url_for("uusi_käyttäjä"))
    elif onko_tunnusta == "Kyllä":
        return redirect(url_for("login"))
    
    
@app.route("/uusi_käyttäjä", methods=["GET", "POST"])
def uusi_käyttäjä():
    if request.method == 'POST':
        name = request.form["username"]
        authority = request.form["authority"]
        password = request.form["salasana"]
        hash_value = generate_password_hash(password)

        
        sql = "INSERT INTO users (username, password, authority) VALUES (:username, :password, :authority)"
        db.session.execute(text(sql), {"username": name, "password": hash_value, "authority": authority})
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("luo_käyttäjä.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

      
        sql = "SELECT id, password, authority FROM users WHERE username=:username"
        result = db.session.execute(text(sql), {"username": username})
        user = result.fetchone()    

        if not user:
            return "Tällä nimellä ei vielä löydy tiliä"
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
               
                session["username"] = username
                session["authority"] = user.authority
                
                
                if user.authority == "admin":
                    return redirect(url_for("teacher_dashboard"))
                else:
                    return redirect(url_for("student_dashboard"))
            else:
                return "Invalid password"
    
    return render_template("login_html.html")


@app.route("/teacher_dashboard")
def teacher_dashboard():
    
    if "username" in session and session.get("authority") == "admin":
        return render_template("opettajan_sivut.html")
    else:
        return "Unauthorized Access"  

    

@app.route("/student_dashboard")
def student_dashboard():
 
    if "username" in session and session["authority"] == "user":
        return "Welcome to the Student's Dashboard"
    else:
        return "Unauthorized Access" 


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
  

