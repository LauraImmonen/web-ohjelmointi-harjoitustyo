from flask import Flask
from os import getenv
from all_routes.routes import main_routes  
from all_routes.teacher_routes import teacher_routes  
from all_routes.student_routes import student_routes  
from db import db, init_db 

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

init_db(app)  

app.register_blueprint(main_routes) 
app.register_blueprint(teacher_routes) 
app.register_blueprint(student_routes) 

if __name__ == "__main__":
    app.run()




