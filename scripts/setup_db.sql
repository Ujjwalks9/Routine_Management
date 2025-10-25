CREATE DATABASE routine_management;
USE routine_management;

CREATE TABLE timetable_teacher (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    availability JSON
);

CREATE TABLE timetable_subject (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50)
);

CREATE TABLE timetable_class (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    department VARCHAR(50)
);

CREATE TABLE timetable_room (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    capacity INT
);

CREATE TABLE timetable_timeslot (
    id INT AUTO_INCREMENT PRIMARY KEY,
    day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday') NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

CREATE TABLE timetable_allocation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT,
    subject_id INT,
    class_id INT,
    room_id INT,
    timeslot_id INT,
    FOREIGN KEY (teacher_id) REFERENCES timetable_teacher(id),
    FOREIGN KEY (subject_id) REFERENCES timetable_subject(id),
    FOREIGN KEY (class_id) REFERENCES timetable_class(id),
    FOREIGN KEY (room_id) REFERENCES timetable_room(id),
    FOREIGN KEY (timeslot_id) REFERENCES timetable_timeslot(id)
);

CREATE TABLE timetable_teacherpreference (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT,
    subject_id INT,
    priority INT,
    FOREIGN KEY (teacher_id) REFERENCES timetable_teacher(id),
    FOREIGN KEY (subject_id) REFERENCES timetable_subject(id)
);