DROP DATABASE IF EXISTS edumate_db;


-- CREATE AND USE DATABASE SQL STATEMENTS
DROP DATABASE IF EXISTS edumate_db2;
CREATE DATABASE edumate_db2;
USE edumate_db2;

-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-- ------------- 1. USER TABLES (4) -------------
-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

-- ------------- 1.1 ADMIN TABLE -------------
CREATE TABLE admin
(
    admin_id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL
);

-- ------------- 1.2 TEACHER TABLE -------------
CREATE TABLE teacher
(
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    mobile VARCHAR(15),

    department VARCHAR(100),

    designation VARCHAR(100)
);
-- ------------- 1.3 PARENT TABLE -------------
CREATE TABLE parent
(
    parent_id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    mobile VARCHAR(15)
);

-- ------------- 2.1 STANDARD TABLE -------------
CREATE TABLE standard
(
    standard_id INT AUTO_INCREMENT PRIMARY KEY,

    standard_name VARCHAR(50) NOT NULL UNIQUE
);
-- 

-- ------------- 1.4 STUDENT TABLE -------------
CREATE TABLE student
(
    student_id INT AUTO_INCREMENT PRIMARY KEY,

    parent_id INT NOT NULL,

    standard_id INT NOT NULL,

    admission_no VARCHAR(30) UNIQUE,

    roll_no VARCHAR(20) NOT NULL,

    division VARCHAR(10),

    name VARCHAR(100) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    mobile VARCHAR(15),

    FOREIGN KEY(parent_id)
        REFERENCES parent(parent_id)
        ON DELETE CASCADE,

    FOREIGN KEY(standard_id)
        REFERENCES standard(standard_id)
        ON DELETE CASCADE
);
-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
--------------- 2. ACADEMIC TABLES (5)-------------
-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

------------- 2.2 SUBJECT TABLE -------------
CREATE TABLE subject
(
    subject_id INT AUTO_INCREMENT PRIMARY KEY,

    standard_id INT NOT NULL,

    subject_name VARCHAR(100) NOT NULL,

    assessment_type ENUM('Traditional','OBE')
    DEFAULT 'Traditional',

    FOREIGN KEY (standard_id)
    REFERENCES standard(standard_id)
    ON DELETE CASCADE
);
-- ------------- 2.3 TEACHER_SUBJECT TABLE -------------
CREATE TABLE teacher_subject
(
    teacher_subject_id INT AUTO_INCREMENT PRIMARY KEY,

    teacher_id INT NOT NULL,

    subject_id INT NOT NULL,

    FOREIGN KEY (teacher_id)
    REFERENCES teacher(teacher_id)
    ON DELETE CASCADE,

    FOREIGN KEY (subject_id)
    REFERENCES subject(subject_id)
    ON DELETE CASCADE,

    UNIQUE (teacher_id, subject_id)
);
-- ------------- 2.4 CHAPTER TABLE -------------
CREATE TABLE chapter
(
    chapter_id INT AUTO_INCREMENT PRIMARY KEY,

    subject_id INT NOT NULL,

    chapter_number INT,

    chapter_name VARCHAR(200) NOT NULL,

    FOREIGN KEY (subject_id)
    REFERENCES subject(subject_id)
    ON DELETE CASCADE
);
-- ------------- 2.5 COURSE OUTCOME TABLE -------------
CREATE TABLE course_outcome
(
    co_id INT AUTO_INCREMENT PRIMARY KEY,

    subject_id INT NOT NULL,

    co_code VARCHAR(20) NOT NULL,

    co_description VARCHAR(255) NOT NULL,

    FOREIGN KEY (subject_id)
    REFERENCES subject(subject_id)
    ON DELETE CASCADE
);
-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-- ------------- 3. ASSESSMENT TABLES (4)-------------
-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

-- ------------- 3.1 QUESTION TABLE -------------
CREATE TABLE question
(
    question_id INT AUTO_INCREMENT PRIMARY KEY,

    teacher_id INT NOT NULL,

    chapter_id INT NOT NULL,

    co_id INT NULL,

    question_text TEXT NOT NULL,

    option_a VARCHAR(255) NOT NULL,
    option_b VARCHAR(255) NOT NULL,
    option_c VARCHAR(255) NOT NULL,
    option_d VARCHAR(255) NOT NULL,

    correct_option CHAR(1) NOT NULL,

    difficulty ENUM('Easy','Medium','Hard') NOT NULL,

    source ENUM('Teacher','PYQ') DEFAULT 'Teacher',

    marks INT DEFAULT 1,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (teacher_id)
        REFERENCES teacher(teacher_id)
        ON DELETE CASCADE,

    FOREIGN KEY (chapter_id)
        REFERENCES chapter(chapter_id)
        ON DELETE CASCADE,

    FOREIGN KEY (co_id)
        REFERENCES course_outcome(co_id)
        ON DELETE SET NULL
);
-- ------------- 3.2 TEST TABLE -------------
CREATE TABLE test
(
    test_id INT AUTO_INCREMENT PRIMARY KEY,

    teacher_id INT NOT NULL,

    standard_id INT NOT NULL,

    subject_id INT NOT NULL,

    test_name VARCHAR(150) NOT NULL,

    total_questions INT NOT NULL,

    total_marks INT NOT NULL,

    easy_count INT DEFAULT 0,

    medium_count INT DEFAULT 0,

    hard_count INT DEFAULT 0,

    duration INT NOT NULL,

    instructions TEXT,

    status ENUM('Draft','Published','Closed')
    DEFAULT 'Draft',

    test_date DATETIME,

    FOREIGN KEY (teacher_id)
        REFERENCES teacher(teacher_id)
        ON DELETE CASCADE,

    FOREIGN KEY (standard_id)
        REFERENCES standard(standard_id)
        ON DELETE CASCADE,

    FOREIGN KEY (subject_id)
        REFERENCES subject(subject_id)
        ON DELETE CASCADE
);
-- ------------- 3.3 TEST_QUESTION TABLE -------------
CREATE TABLE test_question
(
    id INT AUTO_INCREMENT PRIMARY KEY,

    test_id INT NOT NULL,

    question_id INT NOT NULL,

    FOREIGN KEY (test_id)
        REFERENCES test(test_id)
        ON DELETE CASCADE,

    FOREIGN KEY (question_id)
        REFERENCES question(question_id)
        ON DELETE CASCADE,

    UNIQUE(test_id, question_id)
);
-- ------------- 3.4 TEST_ATTEMPT TABLE -------------
CREATE TABLE test_attempt
(
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,

    test_id INT NOT NULL,

    student_id INT NOT NULL,

    start_time DATETIME,

    end_time DATETIME,

    score DECIMAL(5,2),

    percentage DECIMAL(5,2),

    attempt_status
    ENUM('Completed','Auto Submitted')
    DEFAULT 'Completed',

    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (test_id)
        REFERENCES test(test_id)
        ON DELETE CASCADE,

    FOREIGN KEY (student_id)
        REFERENCES student(student_id)
        ON DELETE CASCADE
);
-- ------------- 3.5 STUDENT ANSWER TABLE -------------
CREATE TABLE student_answer
(
    answer_id INT AUTO_INCREMENT PRIMARY KEY,

    attempt_id INT NOT NULL,

    question_id INT NOT NULL,

    selected_option CHAR(1),

    is_correct BOOLEAN,

    marks_obtained DECIMAL(5,2),

    FOREIGN KEY (attempt_id)
        REFERENCES test_attempt(attempt_id)
        ON DELETE CASCADE,

    FOREIGN KEY (question_id)
        REFERENCES question(question_id)
        ON DELETE CASCADE
);
-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-- ------------- 4. NETWORKING/SMART FEATURES TABLES (2)-------------
-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

--------------- 4.1 LOGIN_HISTORY TABLE -------------
CREATE TABLE login_history
(
    login_id INT AUTO_INCREMENT PRIMARY KEY,

    user_role ENUM('Admin','Teacher','Student','Parent') NOT NULL,

    user_id INT NOT NULL,

    login_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    ip_address VARCHAR(45),

    device_info VARCHAR(255)
);
-- ------------- 4.2 NOTIFICATION TABLE -------------
CREATE TABLE notification
(
    notification_id INT AUTO_INCREMENT PRIMARY KEY,

    user_role ENUM('Teacher','Student','Parent') NOT NULL,

    user_id INT NOT NULL,

    title VARCHAR(100) NOT NULL,

    message TEXT NOT NULL,

    is_read BOOLEAN DEFAULT FALSE,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
-- XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-- ------------INSERTING DATA IN USER TABLES ADMIN, TEACHER, PARENT--------------
INSERT INTO admin
(name, email, password)
VALUES
(
'Administrator',
'admin@edumate.com',
'admin123'
);

INSERT INTO teacher
(name, email, password, mobile, department, designation)
VALUES
(
'Asha Kotian',
'asha@edumate.com',
'teacher123',
'9876543210',
'Social Science',
'Teacher'
),

(
'Ravi Shetty',
'ravi@edumate.com',
'teacher123',
'9876543211',
'Computer Science',
'Assistant Professor'
);

INSERT INTO parent
(name, email, password, mobile)
VALUES
(
'Yogish Suvarna',
'yogish@edumate.com',
'parent123',
'9876543222'
),

(
'Priya Sharma',
'priya@edumate.com',
'parent123',
'9876543223'
);

-- ------------INSERTING DATA IN ACADEMIC TABLE STANDARD--------------
INSERT INTO standard
(standard_name)
VALUES
('10'),
('FYBSc'),
('SYBSc'),
('TYBSc');
-- ------------INSERTING DATA IN USER TABLE STUDENT--------------
INSERT INTO student
(
parent_id,
standard_id,
admission_no,
roll_no,
division,
name,
email,
password,
mobile
)
VALUES
(
1,
1,
'GR1001',
'01',
'A',
'Rahul Sharma',
'rahul@edumate.com',
'student123',
'9988776655'
),

(
2,
4,
'TYCS2026001',
'12',
'A',
'Neha Patil',
'neha@edumate.com',
'student123',
'9988776656'
);
-- ---------------INSERTING DATA IN ACADEMIC TABLES SUBJECT, TEACHER_SUBJECT, CHAPTER, course_outcome----------------
INSERT INTO subject
(
standard_id,
subject_name,
assessment_type
)
VALUES
(
1,
'History',
'Traditional'
),

(
4,
'Computer Networks',
'OBE'
),

(
4,
'Natural Language Processing',
'OBE'
);

INSERT INTO teacher_subject
(
teacher_id,
subject_id
)
VALUES
(1,1),
(2,2),
(2,3);

INSERT INTO chapter
(
subject_id,
chapter_number,
chapter_name
)
VALUES
(
1,
1,
'Historiography: Development in the West'
),

(
1,
2,
'Applied History'
),

(
2,
1,
'Introduction to Computer Networks'
),

(
2,
2,
'Network Models'
),

(
3,
1,
'Introduction to NLP'
),

(
3,
2,
'Text Preprocessing'
);

INSERT INTO course_outcome
(
subject_id,
co_code,
co_description
)
VALUES
(
2,
'CO1',
'Understand the fundamentals of Computer Networks'
),

(
2,
'CO2',
'Analyze network models and protocols'
),

(
2,
'CO3',
'Apply networking concepts to solve communication problems'
);

-- ------------INSERTING DATA IN ASSESSMENT TABLES--------------
INSERT INTO question
(
teacher_id,
chapter_id,
co_id,
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
(1,1,NULL,'Who is known as the Father of History?','Herodotus','Plato','Aristotle','Socrates','A','Easy','Teacher',1),

(1,1,NULL,'Who wrote "The Histories"?','Herodotus','Karl Marx','Voltaire','Leopold Ranke','A','Easy','Teacher',1),

(1,1,NULL,'Who introduced the scientific method in history writing?','Leopold Ranke','Herodotus','Plato','Aristotle','A','Medium','Teacher',2),

(1,1,NULL,'History mainly studies','Future','Past Events','Current Affairs','Mathematics','B','Easy','Teacher',1),

(1,1,NULL,'Which historian emphasized original sources?','Leopold Ranke','Karl Marx','E.H. Carr','Toynbee','A','Medium','Teacher',2),

(1,1,NULL,'The word History is derived from','Historia','Historiae','Histor','Historian','A','Easy','Teacher',1),

(1,1,NULL,'Who believed history should be written "as it actually happened"?','Ranke','Marx','Herodotus','Hegel','A','Medium','Teacher',2),

(1,1,NULL,'Which is a primary historical source?','Newspaper','Original Letter','Magazine','History Textbook','B','Easy','Teacher',1),

(1,1,NULL,'Historiography means','Writing History','Reading History','Teaching History','Drawing Maps','A','Easy','Teacher',1),

(1,1,NULL,'Who developed Materialistic Interpretation of History?','Karl Marx','Herodotus','Ranke','Plato','A','Hard','Teacher',3);

INSERT INTO test
(
teacher_id,
standard_id,
subject_id,
test_name,
total_questions,
total_marks,
easy_count,
medium_count,
hard_count,
duration,
instructions,
status,
test_date
)
VALUES
(
1,
1,
1,
'History Chapter 1 Test',
10,
15,
5,
3,
2,
30,
'Read each question carefully before answering.',
'Published',
NOW()
);

INSERT INTO test_question
(test_id,question_id)
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

INSERT INTO test_attempt
(
test_id,
student_id,
start_time,
end_time,
score,
percentage,
attempt_status
)
VALUES
(
1,
1,
NOW(),
NOW(),
12,
80,
'Completed'
);

INSERT INTO student_answer
(
attempt_id,
question_id,
selected_option,
is_correct,
marks_obtained
)
VALUES
(1,1,'A',1,1),
(1,2,'A',1,1),
(1,3,'A',1,2),
(1,4,'B',1,1),
(1,5,'A',1,2),
(1,6,'A',1,1),
(1,7,'B',0,0),
(1,8,'B',1,1),
(1,9,'A',1,1),
(1,10,'B',0,0);

-- ------------INSERTING DATA IN NETWORKING/SMART FEATURES TABLES --------------

INSERT INTO login_history
(
user_role,
user_id,
ip_address,
device_info
)
VALUES
(
'Admin',
1,
'192.168.1.2',
'Chrome on Windows 11'
),

(
'Teacher',
1,
'192.168.1.5',
'Microsoft Edge on Windows 11'
),

(
'Student',
1,
'192.168.1.10',
'Chrome on Android'
),

(
'Parent',
1,
'192.168.1.15',
'Chrome on Android'
);

INSERT INTO notification
(
user_role,
user_id,
title,
message
)
VALUES
(
'Student',
1,
'New Test Available',
'History Chapter 1 Test has been published.'
),

(
'Parent',
1,
'Test Published',
'Your child has a new History test to attempt.'
),

(
'Student',
1,
'Result Published',
'Your History Chapter 1 Test result is now available.'
),

(
'Teacher',
1,
'Test Attempted',
'Rahul Sharma has completed the History Chapter 1 Test.'
);