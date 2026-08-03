-- =====================================================
-- EduMate Database Script
-- Project: EduMate - Smart Student Assessment and Progress Monitoring System
-- =====================================================
DROP DATABASE IF EXISTS edumate_db;
CREATE DATABASE edumate_db;
USE edumate_db;
-- =====================================================
-- TABLE CREATION
-- =====================================================
CREATE TABLE admin
(
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE teacher
(
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    mobile VARCHAR(15)
);

select * from admin;
CREATE TABLE parent
(
    parent_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    mobile VARCHAR(15)
);
CREATE TABLE standard
(
    standard_id INT AUTO_INCREMENT PRIMARY KEY,
    standard_name VARCHAR(20)
);

CREATE TABLE student
(
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    parent_id INT,
    standard_id INT,
    roll_no VARCHAR(20),
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    mobile VARCHAR(15),

    FOREIGN KEY(parent_id)
    REFERENCES parent(parent_id),

    FOREIGN KEY(standard_id)
    REFERENCES standard(standard_id)
);

CREATE TABLE subject
(
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    standard_id INT,
    subject_name VARCHAR(100),

    FOREIGN KEY(standard_id)
    REFERENCES standard(standard_id)
);

CREATE TABLE chapter
(
    chapter_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT,
    chapter_name VARCHAR(200),

    FOREIGN KEY(subject_id)
    REFERENCES subject(subject_id)
);

CREATE TABLE question
(
    question_id INT AUTO_INCREMENT PRIMARY KEY,

    teacher_id INT,
    chapter_id INT,

    question_text TEXT,

    option_a VARCHAR(255),
    option_b VARCHAR(255),
    option_c VARCHAR(255),
    option_d VARCHAR(255),

    correct_option CHAR(1),

    difficulty ENUM('Easy','Medium','Hard'),

    source ENUM('Teacher','PYQ'),

    marks INT DEFAULT 1,

    FOREIGN KEY(teacher_id)
    REFERENCES teacher(teacher_id),

    FOREIGN KEY(chapter_id)
    REFERENCES chapter(chapter_id)
);

CREATE TABLE test
(
    test_id INT AUTO_INCREMENT PRIMARY KEY,

    teacher_id INT,
    standard_id INT,
    subject_id INT,

    test_name VARCHAR(150),

    total_questions INT,

    easy_count INT,

    medium_count INT,

    hard_count INT,

    test_date DATETIME,

    FOREIGN KEY(teacher_id)
    REFERENCES teacher(teacher_id),

    FOREIGN KEY(standard_id)
    REFERENCES standard(standard_id),

    FOREIGN KEY(subject_id)
    REFERENCES subject(subject_id)
);

CREATE TABLE test_question
(
    id INT AUTO_INCREMENT PRIMARY KEY,

    test_id INT,

    question_id INT,

    FOREIGN KEY(test_id)
    REFERENCES test(test_id)
    ON DELETE CASCADE,

    FOREIGN KEY(question_id)
    REFERENCES question(question_id)
);

CREATE TABLE test_attempt
(
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,

    test_id INT,

    student_id INT,

    start_time DATETIME,

    end_time DATETIME,

    score DECIMAL(5,2),

    percentage DECIMAL(5,2),

    FOREIGN KEY(test_id)
    REFERENCES test(test_id),

    FOREIGN KEY(student_id)
    REFERENCES student(student_id)
);

CREATE TABLE student_answer
(
    answer_id INT AUTO_INCREMENT PRIMARY KEY,

    attempt_id INT,

    question_id INT,

    selected_option CHAR(1),

    is_correct BOOLEAN,

    marks_obtained DECIMAL(5,2),

    FOREIGN KEY(attempt_id)
    REFERENCES test_attempt(attempt_id)
    ON DELETE CASCADE,

    FOREIGN KEY(question_id)
    REFERENCES question(question_id)
);

-- =====================================================
-- MASTER DATA INSERTION
-- =====================================================
INSERT INTO admin(name,email,password)
VALUES
('Administrator','admin@edumate.com','admin123');

INSERT INTO teacher(name,email,password,mobile)
VALUES
('Asha Kotian','asha@edumate.com','teacher123','9876543210');
select * from admin;

INSERT INTO parent(name,email,password,mobile)
VALUES
('Yogish Suvarna','yogish@edumate.com','parent123','9876543222');

INSERT INTO standard(standard_name)
VALUES
('10');

INSERT INTO student
(parent_id,standard_id,roll_no,name,email,password,mobile)
VALUES
(1,1,'10A-01','Rahul Sharma',
'rahul@edumate.com','student123','9988776655');

INSERT INTO subject
(standard_id,subject_name)
VALUES
(1,'History');

INSERT INTO chapter
(subject_id,chapter_name)
VALUES
(1,'Historiography: Development in the West');

-- =====================================================
-- QUESTION BANK DATA
-- =====================================================
-- Question 1
INSERT INTO question
(
teacher_id,
chapter_id,
question_text,
option_a,
option_b,
option_c,
option_d,
correct_option,
difficulty,
source,
marks
)
VALUES
(
1,
1,
'Who is known as the Father of History?',
'Herodotus',
'Plato',
'Aristotle',
'Socrates',
'A',
'Easy',
'Teacher',
1
);
-- Question 2
INSERT INTO question
VALUES
(
NULL,
1,
1,
'Who wrote the book "The Histories"?',
'Herodotus',
'Karl Marx',
'Voltaire',
'Leopold Ranke',
'A',
'Easy',
'Teacher',
1
);
-- Question 3
INSERT INTO question
VALUES
(
NULL,
1,
1,
'Who introduced the scientific method in history writing?',
'Ranke',
'Herodotus',
'Plato',
'Aristotle',
'A',
'Medium',
'Teacher',
1
);
-- Question 4
INSERT INTO question
VALUES
(
NULL,
1,
1,
'History mainly studies',
'Future',
'Past events',
'Current affairs',
'Mathematics',
'B',
'Easy',
'Teacher',
1
);
-- Question 5
INSERT INTO question
VALUES
(
NULL,
1,
1,
'Which historian emphasized the use of original sources?',
'Leopold Ranke',
'Karl Marx',
'E.H. Carr',
'Arnold Toynbee',
'A',
'Medium',
'Teacher',
1
);
-- Question 6
INSERT INTO question
VALUES
(
NULL,
1,
1,
'The word History is derived from',
'Historia',
'Historiae',
'Histor',
'Historian',
'A',
'Easy',
'Teacher',
1
);
-- Question 7
INSERT INTO question
VALUES
(
NULL,
1,
1,
'Who believed history should be written "as it actually happened"?',
'Ranke',
'Karl Marx',
'Herodotus',
'Hegel',
'A',
'Medium',
'Teacher',
1
);
-- Question 8
INSERT INTO question
VALUES
(
NULL,
1,
1,
'Which source is considered a primary historical source?',
'Newspaper article',
'Original letter',
'History textbook',
'Magazine',
'B',
'Easy',
'Teacher',
1
);
-- Question 9
INSERT INTO question
VALUES
(
NULL,
1,
1,
'Historiography means',
'Writing History',
'Reading History',
'Teaching History',
'Drawing Maps',
'A',
'Easy',
'Teacher',
1
);
-- Question 10
INSERT INTO question
VALUES
(
NULL,
1,
1,
'Which historian developed Materialistic Interpretation of History?',
'Karl Marx',
'Herodotus',
'Ranke',
'Plato',
'A',
'Hard',
'Teacher',
1
);
-- Question 11
INSERT INTO question
VALUES
(
NULL,
1,
1,
'Who emphasized economic factors in history?',
'Karl Marx',
'Herodotus',
'Ranke',
'Voltaire',
'A',
'Hard',
'Teacher',
1
);
-- Question 12
INSERT INTO question
VALUES
(
NULL,
1,
1,
'Historical sources are mainly classified into',
'Two',
'Three',
'Four',
'Five',
'B',
'Medium',
'Teacher',
1
);
-- Question 13
INSERT INTO question
VALUES
(
NULL,
1,
1,
'Which is NOT a literary source?',
'Coins',
'Travelogues',
'Biographies',
'Books',
'A',
'Medium',
'Teacher',
1
);
-- Question 14
INSERT INTO question
VALUES
(
NULL,
1,
1,
'Who is regarded as a modern scientific historian?',
'Leopold Ranke',
'Herodotus',
'Karl Marx',
'Hegel',
'A',
'Medium',
'Teacher',
1
);
-- Question 15
INSERT INTO question
VALUES
(
NULL,
1,
1,
'Historical research depends upon',
'Evidence',
'Guess',
'Stories',
'Rumours',
'A',
'Easy',
'Teacher',
1
);

-- =====================================================
-- TEST DATA
-- =====================================================
-- Create Sample Test
INSERT INTO test
(
teacher_id,
standard_id,
subject_id,
test_name,
total_questions,
easy_count,
medium_count,
hard_count,
test_date
)
VALUES
(
1,
1,
1,
'History Chapter 1 Practice Test',
10,
5,
3,
2,
NOW()
);
-- Map Questions to Test
INSERT INTO test_question(test_id,question_id)
VALUES
(1,1),
(1,2),
(1,3),
(1,4),
(1,5),
(1,6),
(1,7),
(1,8),
(1,9),
(1,10);
-- Record Student Test Attempt
INSERT INTO test_attempt
(
test_id,
student_id,
start_time,
end_time,
score,
percentage
)
VALUES
(
1,
1,
NOW(),
NOW(),
8,
80
);
-- Store Student Answers
INSERT INTO student_answer
(attempt_id,question_id,selected_option,is_correct,marks_obtained)
VALUES
(1,1,'A',1,1),
(1,2,'A',1,1),
(1,3,'B',0,0),
(1,4,'B',1,1),
(1,5,'A',1,1),
(1,6,'A',1,1),
(1,7,'A',1,1),
(1,8,'B',1,1),
(1,9,'A',1,1),
(1,10,'B',0,0);

CREATE TABLE course_outcome
(
    co_id INT AUTO_INCREMENT PRIMARY KEY,

    subject_id INT NOT NULL,

    co_code VARCHAR(10) NOT NULL,

    co_description VARCHAR(255) NOT NULL,

    FOREIGN KEY(subject_id)
    REFERENCES subject(subject_id)
    ON DELETE CASCADE
);

INSERT INTO course_outcome
(subject_id, co_code, co_description)
VALUES
(1, 'CO1', 'Understand the basic concepts of History and Historiography'),
(1, 'CO2', 'Analyze different approaches to historical writing'),
(1, 'CO3', 'Evaluate the importance of historical sources'),
(1, 'CO4', 'Apply historical knowledge to interpret events');