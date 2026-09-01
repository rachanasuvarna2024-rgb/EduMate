-- ============================================================
-- EDUMATE DATABASE VERSION 3.3
-- COMPLETE DATABASE CREATION SCRIPT
-- ============================================================

DROP DATABASE IF EXISTS edumate_db3_3;

CREATE DATABASE edumate_db3_3;

USE edumate_db3_3;


-- ============================================================
-- 1. INSTITUTION MASTER
-- ============================================================

CREATE TABLE institution
(
    institution_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_name VARCHAR(150) NOT NULL,

    institution_code VARCHAR(30) NOT NULL UNIQUE,

    institution_category ENUM(
        'School',
        'Jr College',
        'Degree College'
    ) NOT NULL,

    institution_type ENUM(
        'Traditional',
        'OBE'
    ) NOT NULL,

    address VARCHAR(255) NOT NULL,

    city VARCHAR(100) NOT NULL,

    state VARCHAR(100) NOT NULL,

    pincode VARCHAR(10) NOT NULL,

    email VARCHAR(150) NOT NULL UNIQUE,

    phone VARCHAR(20) NOT NULL,

    website VARCHAR(200),

    logo VARCHAR(255),

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


-- ============================================================
-- 2. STREAM MASTER
-- Global list of streams
--
-- School:
--   English Medium
--   Hindi Medium
--   Marathi Medium
--   Kannada Medium
--
-- Jr College:
--   Arts
--   Science
--   Commerce
--
-- Degree College:
--   Arts
--   Science
--   Commerce
-- ============================================================

CREATE TABLE stream_master
(
    stream_id INT AUTO_INCREMENT PRIMARY KEY,

    stream_name VARCHAR(100) NOT NULL,

    institution_category ENUM(
        'School',
        'Jr College',
        'Degree College'
    ) NOT NULL,

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE (
        stream_name,
        institution_category
    )
);


-- ============================================================
-- 3. COURSE MASTER
-- Global list of courses
-- Every course belongs to a stream.
-- ============================================================

CREATE TABLE course_master
(
    course_id INT AUTO_INCREMENT PRIMARY KEY,

    course_name VARCHAR(200) NOT NULL,

    stream_id INT NOT NULL,

    institution_category ENUM(
        'School',
        'Jr College',
        'Degree College'
    ) NOT NULL,

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (stream_id)
        REFERENCES stream_master(stream_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    UNIQUE (
        course_name,
        stream_id
    )
);


-- ============================================================
-- 4. SUBJECT MASTER
-- Global list of subjects
-- Every subject belongs to a course.
-- ============================================================

CREATE TABLE subject_master
(
    subject_master_id INT AUTO_INCREMENT PRIMARY KEY,

    subject_name VARCHAR(150) NOT NULL,

    course_id INT NOT NULL,

    institution_category ENUM(
        'School',
        'Jr College',
        'Degree College'
    ) NOT NULL,

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (course_id)
        REFERENCES course_master(course_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    UNIQUE (
        subject_name,
        course_id
    )
);


-- ============================================================
-- 5. DEPARTMENT MASTER
-- ============================================================

CREATE TABLE department_master
(
    department_id INT AUTO_INCREMENT PRIMARY KEY,

    department_name VARCHAR(150) NOT NULL,

    institution_category ENUM(
        'School',
        'Jr College',
        'Degree College'
    ) NOT NULL,

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE (
        department_name,
        institution_category
    )
);


-- ============================================================
-- 6. DESIGNATION MASTER
-- ============================================================

CREATE TABLE designation_master
(
    designation_id INT AUTO_INCREMENT PRIMARY KEY,

    designation_name VARCHAR(150) NOT NULL,

    institution_category ENUM(
        'School',
        'Jr College',
        'Degree College'
    ) NOT NULL,

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE (
        designation_name,
        institution_category
    )
);


-- ============================================================
-- 7. INSTITUTION STREAM
-- Which streams are offered by an institution
-- ============================================================

CREATE TABLE institution_stream
(
    institution_stream_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    stream_id INT NOT NULL,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (stream_id)
        REFERENCES stream_master(stream_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    UNIQUE (
        institution_id,
        stream_id
    )
);


-- ============================================================
-- 8. INSTITUTION COURSE
-- Which courses are offered by an institution
-- ============================================================

CREATE TABLE institution_course
(
    institution_course_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    course_id INT NOT NULL,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (course_id)
        REFERENCES course_master(course_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    UNIQUE (
        institution_id,
        course_id
    )
);


-- ============================================================
-- 9. INSTITUTION SUBJECT
-- Which subjects are offered by an institution
-- ============================================================

CREATE TABLE institution_subject
(
    institution_subject_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    subject_master_id INT NOT NULL,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (subject_master_id)
        REFERENCES subject_master(subject_master_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    UNIQUE (
        institution_id,
        subject_master_id
    )
);


-- ============================================================
-- 10. INSTITUTION DEPARTMENT
-- ============================================================

CREATE TABLE institution_department
(
    institution_department_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    department_id INT NOT NULL,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE,

    FOREIGN KEY (department_id)
        REFERENCES department_master(department_id)
        ON DELETE RESTRICT,

    UNIQUE (
        institution_id,
        department_id
    )
);


-- ============================================================
-- 11. INSTITUTION DESIGNATION
-- ============================================================

CREATE TABLE institution_designation
(
    institution_designation_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    designation_id INT NOT NULL,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE,

    FOREIGN KEY (designation_id)
        REFERENCES designation_master(designation_id)
        ON DELETE RESTRICT,

    UNIQUE (
        institution_id,
        designation_id
    )
);


-- ============================================================
-- 12. ADMIN
-- ============================================================

CREATE TABLE admin
(
    admin_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE
);


-- ============================================================
-- 13. TEACHER
-- ============================================================

CREATE TABLE teacher
(
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    department_id INT,

    designation_id INT,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    mobile VARCHAR(15),

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE,

    FOREIGN KEY (department_id)
        REFERENCES department_master(department_id)
        ON DELETE SET NULL,

    FOREIGN KEY (designation_id)
        REFERENCES designation_master(designation_id)
        ON DELETE SET NULL
);


-- ============================================================
-- 14. PARENT
-- ============================================================

CREATE TABLE parent
(
    parent_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    mobile VARCHAR(15),

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE
);


-- ============================================================
-- 15. STANDARD
--
-- Represents the actual academic class/year inside
-- an institution.
--
-- Example:
-- Institution = Sunrise Public School
-- Course = IX
-- Standard = Standard IX
-- Academic Year = 2026-27
-- ============================================================

CREATE TABLE standard
(
    standard_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    course_id INT NOT NULL,

    standard_name VARCHAR(50) NOT NULL,

    academic_year VARCHAR(20),

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE,

    FOREIGN KEY (course_id)
        REFERENCES course_master(course_id)
        ON DELETE RESTRICT,

    UNIQUE (
        institution_id,
        standard_name,
        course_id
    )
);


-- ============================================================
-- 16. SUBJECT
--
-- Actual subject configured for a particular institution
-- and standard.
--
-- subject_master = global definition
-- subject        = institution-specific implementation
-- ============================================================

CREATE TABLE subject
(
    subject_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    standard_id INT NOT NULL,

    subject_master_id INT,

    subject_name VARCHAR(150) NOT NULL,

    assessment_type ENUM(
        'Traditional',
        'OBE'
    ) DEFAULT 'Traditional',

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE,

    FOREIGN KEY (standard_id)
        REFERENCES standard(standard_id)
        ON DELETE CASCADE,

    FOREIGN KEY (subject_master_id)
        REFERENCES subject_master(subject_master_id)
        ON DELETE SET NULL,

    UNIQUE (
        standard_id,
        subject_name
    )
);


-- ============================================================
-- 17. STUDENT
-- ============================================================

CREATE TABLE student
(
    student_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    parent_id INT NOT NULL,

    standard_id INT NOT NULL,

    admission_no VARCHAR(30) UNIQUE,

    roll_no VARCHAR(20) NOT NULL,

    division VARCHAR(10),

    name VARCHAR(100) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    mobile VARCHAR(15),

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE,

    FOREIGN KEY (parent_id)
        REFERENCES parent(parent_id)
        ON DELETE CASCADE,

    FOREIGN KEY (standard_id)
        REFERENCES standard(standard_id)
        ON DELETE CASCADE
);


-- ============================================================
-- 18. TEACHER_SUBJECT
-- ============================================================

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

    UNIQUE (
        teacher_id,
        subject_id
    )
);


-- ============================================================
-- 19. CHAPTER
-- ============================================================

CREATE TABLE chapter
(
    chapter_id INT AUTO_INCREMENT PRIMARY KEY,

    subject_id INT NOT NULL,

    chapter_number INT,

    chapter_name VARCHAR(200) NOT NULL,

    FOREIGN KEY (subject_id)
        REFERENCES subject(subject_id)
        ON DELETE CASCADE,

    UNIQUE (
        subject_id,
        chapter_number
    )
);


-- ============================================================
-- 20. COURSE OUTCOME
-- ============================================================

CREATE TABLE course_outcome
(
    co_id INT AUTO_INCREMENT PRIMARY KEY,

    subject_id INT NOT NULL,

    co_code VARCHAR(20) NOT NULL,

    co_description VARCHAR(255) NOT NULL,

    FOREIGN KEY (subject_id)
        REFERENCES subject(subject_id)
        ON DELETE CASCADE,

    UNIQUE (
        subject_id,
        co_code
    )
);


-- ============================================================
-- 21. QUESTION
-- ============================================================

CREATE TABLE question
(
    question_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    teacher_id INT NOT NULL,

    chapter_id INT NOT NULL,

    co_id INT NULL,

    question_text TEXT NOT NULL,

    option_a VARCHAR(255) NOT NULL,

    option_b VARCHAR(255) NOT NULL,

    option_c VARCHAR(255) NOT NULL,

    option_d VARCHAR(255) NOT NULL,

    correct_option CHAR(1) NOT NULL,

    difficulty ENUM(
        'Easy',
        'Medium',
        'Hard'
    ) NOT NULL,

    source ENUM(
        'Teacher',
        'PYQ'
    ) DEFAULT 'Teacher',

    marks INT DEFAULT 1,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE,

    FOREIGN KEY (teacher_id)
        REFERENCES teacher(teacher_id)
        ON DELETE CASCADE,

    FOREIGN KEY (chapter_id)
        REFERENCES chapter(chapter_id)
        ON DELETE CASCADE,

    FOREIGN KEY (co_id)
        REFERENCES course_outcome(co_id)
        ON DELETE SET NULL,

    CHECK (
        correct_option IN ('A','B','C','D')
    )
);


-- ============================================================
-- 22. TEST
-- ============================================================

CREATE TABLE test
(
    test_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

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

    status ENUM(
        'Draft',
        'Published',
        'Closed'
    ) DEFAULT 'Draft',

    test_date DATETIME,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE,

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


-- ============================================================
-- 23. TEST_QUESTION
-- ============================================================

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

    UNIQUE (
        test_id,
        question_id
    )
);


-- ============================================================
-- 24. TEST_ATTEMPT
-- ============================================================

CREATE TABLE test_attempt
(
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,

    test_id INT NOT NULL,

    student_id INT NOT NULL,

    start_time DATETIME,

    end_time DATETIME,

    score DECIMAL(5,2),

    percentage DECIMAL(5,2),

    attempt_status ENUM(
        'Completed',
        'Auto Submitted'
    ) DEFAULT 'Completed',

    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (test_id)
        REFERENCES test(test_id)
        ON DELETE CASCADE,

    FOREIGN KEY (student_id)
        REFERENCES student(student_id)
        ON DELETE CASCADE
);


-- ============================================================
-- 25. STUDENT_ANSWER
-- ============================================================

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


-- ============================================================
-- 26. LOGIN_HISTORY
-- ============================================================

CREATE TABLE login_history
(
    login_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT,

    user_role ENUM(
        'Admin',
        'Teacher',
        'Student',
        'Parent'
    ) NOT NULL,

    user_id INT NOT NULL,

    login_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    ip_address VARCHAR(45),

    device_info VARCHAR(255),

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE SET NULL
);


-- ============================================================
-- 27. NOTIFICATION
-- ============================================================

CREATE TABLE notification
(
    notification_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    user_role ENUM(
        'Teacher',
        'Student',
        'Parent'
    ) NOT NULL,

    user_id INT NOT NULL,

    title VARCHAR(100) NOT NULL,

    message TEXT NOT NULL,

    is_read BOOLEAN DEFAULT FALSE,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE
);


-- ============================================================
-- END OF DATABASE CREATION SCRIPT
-- ============================================================