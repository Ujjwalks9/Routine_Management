-- scripts/sample_data.sql
USE routine_management;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE timetable_allocation;
TRUNCATE TABLE timetable_teacherpreference;
TRUNCATE TABLE timetable_teacher;
TRUNCATE TABLE timetable_subject;
TRUNCATE TABLE timetable_class;
TRUNCATE TABLE timetable_room;
TRUNCATE TABLE timetable_timeslot;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO timetable_teacher (name, availability) VALUES
('Dr. Alice Smith', '{"Monday": ["08:00-12:00"], "Tuesday": ["09:00-11:00"]}'),
('Prof. Bob Jones', '{"Monday": ["10:00-14:00"], "Wednesday": ["08:00-10:00"]}'),
('Ms. Carol White', '{"Tuesday": ["08:00-12:00"], "Friday": ["09:00-11:00"]}');

INSERT INTO timetable_subject (name, department) VALUES
('Mathematics', 'CS'),
('Physics', 'Physics'),
('Algorithms', 'CS');

INSERT INTO timetable_class (name, department) VALUES
('CS101', 'CS'),
('PHY201', 'Physics');

INSERT INTO timetable_room (name, capacity) VALUES
('Room A', 30),
('Room B', 40);

INSERT INTO timetable_timeslot (day, start_time, end_time) VALUES
('Monday', '08:00:00', '09:00:00'),
('Monday', '09:00:00', '10:00:00'),
('Tuesday', '08:00:00', '09:00:00');

INSERT INTO timetable_teacherpreference (teacher_id, subject_id, priority) VALUES
(1, 1, 1), -- Alice prefers Mathematics
(1, 2, 3), -- Alice less prefers Physics
(2, 3, 1), -- Bob prefers Algorithms
(3, 2, 1); -- Carol prefers Physics