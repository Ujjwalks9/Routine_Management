USE routine_management;

-- Teachers
INSERT INTO timetable_teacher (name, availability) VALUES
('Dr. Alice Smith', '{"Monday": ["08:00-12:00"], "Tuesday": ["09:00-11:00"]}'),
('Prof. Bob Jones', '{"Monday": ["10:00-14:00"], "Wednesday": ["08:00-10:00"]}'),
('Ms. Carol White', '{"Tuesday": ["08:00-12:00"], "Friday": ["09:00-11:00"]}');

-- Subjects
INSERT INTO timetable_subject (name, department) VALUES
('Mathematics', 'CS'),
('Physics', 'Physics'),
('Algorithms', 'CS');

-- Classes
INSERT INTO timetable_class (name, department) VALUES
('CS101', 'CS'),
('PHY201', 'Physics');

-- Rooms
INSERT INTO timetable_room (name, capacity) VALUES
('Room A', 30),
('Room B', 40);

-- Time Slots
INSERT INTO timetable_timeslot (day, start_time, end_time) VALUES
('Monday', '08:00:00', '09:00:00'),
('Monday', '09:00:00', '10:00:00'),
('Tuesday', '08:00:00', '09:00:00');

-- Teacher Preferences
INSERT INTO timetable_teacherpreference (teacher_id, subject_id, priority) VALUES
(1, 1, 1), -- Alice prefers Mathematics
(1, 2, 3), -- Alice less prefers Physics
(2, 3, 1), -- Bob prefers Algorithms
(3, 2, 1); -- Carol prefers Physics