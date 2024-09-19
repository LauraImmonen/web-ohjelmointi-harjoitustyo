CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT, 
    admin TEXT
);

CREATE TABLE teachers (
    teacher_id INT PRIMARY KEY,
    username TEXT UNIQUE,
    course TEXT,
    FOREIGN KEY (teacher_id) REFERENCES users(id)
);

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    username TEXT UNIQUE,
    course TEXT,
    FOREIGN KEY (student_id) REFERENCES users(id)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course TEXT,
    student_id INT REFERENCES users,
    teacher_id INT REFERENCES users,
    course_description TEXT
);

CREATE TABLE grades (
    grade_id INT PRIMARY KEY,
    student_id INT REFERENCES students,
    teacher_id INT REFERENCES teachers,
    course_id INT REFERENCES courses,
    grade INT
);

CREATE TABLE enrollments (  
    course_id INT REFERENCES courses(course_id),
    student_id INT REFERENCES students(student_id),
    PRIMARY KEY (course_id, student_id)
);