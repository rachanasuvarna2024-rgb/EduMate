-- ============================================================
-- EDUMATE DATABASE VERSION 3.3
-- Institution Management + Academic Structure
-- ============================================================

DROP DATABASE IF EXISTS edumate_db3_3;

CREATE DATABASE edumate_db3_3;

USE edumate_db3_3;


-- ============================================================
-- 1. ADMIN TABLE
-- ============================================================

CREATE TABLE admin
(
    admin_id INT AUTO_INCREMENT PRIMARY KEY,

    admin_name VARCHAR(100) NOT NULL,

    email VARCHAR(150) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    status ENUM('Active','Inactive')
        DEFAULT 'Active',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


-- ============================================================
-- 2. INSTITUTION MASTER TABLE
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

    address VARCHAR(255),

    city VARCHAR(100),

    state VARCHAR(100),

    pincode VARCHAR(10),

    email VARCHAR(150) UNIQUE,

    phone VARCHAR(20),

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
-- 3. STREAM MASTER TABLE
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
-- 4. COURSE MASTER TABLE
-- IMPORTANT:
-- A course is NOT directly linked to one stream.
-- A course can belong to multiple streams.
-- Example:
-- I can belong to English Medium, Hindi Medium,
-- Marathi Medium and Kannada Medium.
-- ============================================================

CREATE TABLE course_master
(
    course_id INT AUTO_INCREMENT PRIMARY KEY,

    course_name VARCHAR(200) NOT NULL,

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
        course_name,
        institution_category
    )
);


-- ============================================================
-- 5. COURSE - STREAM MAPPING TABLE
-- Many-to-Many relationship
--
-- One course can belong to many streams.
-- One stream can contain many courses.
-- ============================================================

CREATE TABLE course_stream
(
    course_stream_id INT AUTO_INCREMENT PRIMARY KEY,

    course_id INT NOT NULL,

    stream_id INT NOT NULL,

    FOREIGN KEY (course_id)
        REFERENCES course_master(course_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (stream_id)
        REFERENCES stream_master(stream_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    UNIQUE (
        course_id,
        stream_id
    )
);

-- ============================================================
-- 5. COURSE - ACADEMIC YEAR MAPPING TABLE
-- ============================================================
-- One course can be offered in multiple academic years.
--
-- Example:
-- B.Sc. Computer Science -> 2025-26
-- B.Sc. Computer Science -> 2026-27
--
-- The course itself remains in course_master only once.
-- ============================================================

CREATE TABLE course_academic_year
(
    course_academic_year_id INT AUTO_INCREMENT PRIMARY KEY,

    course_id INT NOT NULL,

    academic_year VARCHAR(20) NOT NULL,

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
        ON DELETE CASCADE,

    UNIQUE (
        course_id,
        academic_year
    )
);

-- ============================================================
-- 29. SEMESTER MASTER TABLE
-- ============================================================
-- Defines semesters according to the academic year/level.
--
-- Degree College:
--     FY -> Semester 1, 2
--     SY -> Semester 3, 4
--     TY -> Semester 5, 6
--     4th Year -> Semester 7, 8
--
-- Jr College:
--     FY -> Semester 1, 2
--     SY -> Semester 3, 4
--
-- School:
--     Not Applicable
--
-- This table is a MASTER table.
-- It is not institution-specific.
-- ============================================================

CREATE TABLE semester_master
(
    semester_id INT AUTO_INCREMENT PRIMARY KEY,

    academic_year VARCHAR(20) NOT NULL,

    semester_number INT NOT NULL,

    semester_name VARCHAR(50) NOT NULL,

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
        academic_year,
        semester_number,
        institution_category
    )
);

-- ============================================================
-- 6. SUBJECT MASTER TABLE
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
-- 7. DEPARTMENT MASTER TABLE
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
-- 8. DESIGNATION MASTER TABLE
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
-- 9. INSTITUTION - STREAM MAPPING
-- ============================================================

CREATE TABLE institution_stream
(
    institution_stream_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    stream_id INT NOT NULL,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (stream_id)
        REFERENCES stream_master(stream_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    UNIQUE (
        institution_id,
        stream_id
    )
);


-- ============================================================
-- 10. INSTITUTION - COURSE MAPPING
-- ============================================================

CREATE TABLE institution_course
(
    institution_course_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    course_id INT NOT NULL,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (course_id)
        REFERENCES course_master(course_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    UNIQUE (
        institution_id,
        course_id
    )
);


-- ============================================================
-- 11. INSTITUTION - SUBJECT MAPPING
-- ============================================================

CREATE TABLE institution_subject
(
    institution_subject_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    subject_master_id INT NOT NULL,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (subject_master_id)
        REFERENCES subject_master(subject_master_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    UNIQUE (
        institution_id,
        subject_master_id
    )
);


-- ============================================================
-- 12. INSTITUTION - DEPARTMENT MAPPING
-- ============================================================

CREATE TABLE institution_department
(
    institution_department_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    department_id INT NOT NULL,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (department_id)
        REFERENCES department_master(department_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    UNIQUE (
        institution_id,
        department_id
    )
);


-- ============================================================
-- 13. INSTITUTION - DESIGNATION MAPPING
-- ============================================================

CREATE TABLE institution_designation
(
    institution_designation_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    designation_id INT NOT NULL,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (designation_id)
        REFERENCES designation_master(designation_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    UNIQUE (
        institution_id,
        designation_id
    )
);


-- ============================================================
-- 14. STANDARD TABLE
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
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (course_id)
        REFERENCES course_master(course_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    UNIQUE (
        institution_id,
        standard_name,
        course_id
    )
);


-- ============================================================
-- 15. SUBJECT TABLE
-- Institution-specific subject
-- ============================================================

CREATE TABLE subject
(
    subject_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    standard_id INT,

    subject_master_id INT,

    subject_name VARCHAR(150) NOT NULL,

    assessment_type ENUM(
        'Traditional',
        'OBE'
    ) DEFAULT 'Traditional',

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (standard_id)
        REFERENCES standard(standard_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    FOREIGN KEY (subject_master_id)
        REFERENCES subject_master(subject_master_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);


-- ============================================================
-- 16. TEACHER TABLE
-- ============================================================

CREATE TABLE teacher
(
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    department_id INT,

    designation_id INT,

    teacher_name VARCHAR(100) NOT NULL,

    email VARCHAR(150) NOT NULL UNIQUE,

    phone VARCHAR(20),

    password VARCHAR(255) NOT NULL,

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (department_id)
        REFERENCES department_master(department_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    FOREIGN KEY (designation_id)
        REFERENCES designation_master(designation_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);


-- ============================================================
-- 17. PARENT TABLE
-- ============================================================

CREATE TABLE parent
(
    parent_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    parent_name VARCHAR(100) NOT NULL,

    email VARCHAR(150) NOT NULL UNIQUE,

    phone VARCHAR(20),

    password VARCHAR(255) NOT NULL,

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


-- ============================================================
-- 18. STUDENT TABLE
-- ============================================================

CREATE TABLE student
(
    student_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    standard_id INT,

    parent_id INT,

    student_name VARCHAR(100) NOT NULL,

    email VARCHAR(150) NOT NULL UNIQUE,

    phone VARCHAR(20),

    password VARCHAR(255) NOT NULL,

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (standard_id)
        REFERENCES standard(standard_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    FOREIGN KEY (parent_id)
        REFERENCES parent(parent_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);


-- ============================================================
-- 19. TEACHER - SUBJECT MAPPING
-- ============================================================

CREATE TABLE teacher_subject
(
    teacher_subject_id INT AUTO_INCREMENT PRIMARY KEY,

    teacher_id INT NOT NULL,

    subject_id INT NOT NULL,

    FOREIGN KEY (teacher_id)
        REFERENCES teacher(teacher_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (subject_id)
        REFERENCES subject(subject_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    UNIQUE (
        teacher_id,
        subject_id
    )
);


-- ============================================================
-- 20. CHAPTER TABLE
-- ============================================================

CREATE TABLE chapter
(
    chapter_id INT AUTO_INCREMENT PRIMARY KEY,

    subject_id INT NOT NULL,

    chapter_name VARCHAR(200) NOT NULL,

    chapter_number INT,

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    FOREIGN KEY (subject_id)
        REFERENCES subject(subject_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


-- ============================================================
-- 21. COURSE OUTCOME TABLE
-- ============================================================

CREATE TABLE course_outcome
(
    co_id INT AUTO_INCREMENT PRIMARY KEY,

    subject_id INT NOT NULL,

    co_code VARCHAR(20) NOT NULL,

    co_description VARCHAR(500) NOT NULL,

    FOREIGN KEY (subject_id)
        REFERENCES subject(subject_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    UNIQUE (
        subject_id,
        co_code
    )
);


-- ============================================================
-- 22. QUESTION TABLE
-- ============================================================

-- ============================================================
-- QUESTION TABLE
-- ============================================================

CREATE TABLE question
(
    question_id INT AUTO_INCREMENT PRIMARY KEY,

    subject_id INT NOT NULL,

    chapter_id INT,

    co_id INT,

    question_text TEXT NOT NULL,

    question_image VARCHAR(255),

    option_a VARCHAR(500),

    option_b VARCHAR(500),

    option_c VARCHAR(500),

    option_d VARCHAR(500),

    correct_answer CHAR(1),

    difficulty ENUM(
        'Easy',
        'Medium',
        'Hard'
    ) DEFAULT 'Medium',

    marks DECIMAL(5,2) DEFAULT 1,

    question_type ENUM(
        'MCQ',
        'True/False',
        'Short Answer',
        'Long Answer'
    ) DEFAULT 'MCQ',

    is_pyq BOOLEAN DEFAULT FALSE,

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    FOREIGN KEY (subject_id)
        REFERENCES subject(subject_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (chapter_id)
        REFERENCES chapter(chapter_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    FOREIGN KEY (co_id)
        REFERENCES course_outcome(co_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);
-- ============================================================
-- 23. TEST TABLE
-- ============================================================

CREATE TABLE test
(
    test_id INT AUTO_INCREMENT PRIMARY KEY,

    teacher_id INT NOT NULL,

    subject_id INT NOT NULL,

    test_name VARCHAR(200) NOT NULL,

    description TEXT,

    total_marks DECIMAL(7,2),

    duration_minutes INT,

    start_datetime DATETIME,

    end_datetime DATETIME,

    status ENUM(
        'Draft',
        'Published',
        'Closed'
    ) DEFAULT 'Draft',

    FOREIGN KEY (teacher_id)
        REFERENCES teacher(teacher_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (subject_id)
        REFERENCES subject(subject_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


-- ============================================================
-- 24. TEST - QUESTION MAPPING
-- ============================================================

CREATE TABLE test_question
(
    test_question_id INT AUTO_INCREMENT PRIMARY KEY,

    test_id INT NOT NULL,

    question_id INT NOT NULL,

    question_order INT,

    FOREIGN KEY (test_id)
        REFERENCES test(test_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (question_id)
        REFERENCES question(question_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    UNIQUE (
        test_id,
        question_id
    )
);


-- ============================================================
-- 25. TEST ATTEMPT TABLE
-- ============================================================

CREATE TABLE test_attempt
(
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,

    test_id INT NOT NULL,

    student_id INT NOT NULL,

    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    submitted_at DATETIME,

    score DECIMAL(7,2),

    status ENUM(
        'In Progress',
        'Submitted'
    ) DEFAULT 'In Progress',

    FOREIGN KEY (test_id)
        REFERENCES test(test_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (student_id)
        REFERENCES student(student_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


-- ============================================================
-- 26. STUDENT ANSWER TABLE
-- ============================================================

CREATE TABLE student_answer
(
    answer_id INT AUTO_INCREMENT PRIMARY KEY,

    attempt_id INT NOT NULL,

    question_id INT NOT NULL,

    selected_answer CHAR(1),

    is_correct BOOLEAN,

    marks_obtained DECIMAL(5,2),

    FOREIGN KEY (attempt_id)
        REFERENCES test_attempt(attempt_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (question_id)
        REFERENCES question(question_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    UNIQUE (
        attempt_id,
        question_id
    )
);


-- ============================================================
-- 27. LOGIN HISTORY
-- ============================================================

CREATE TABLE login_history
(
    login_id INT AUTO_INCREMENT PRIMARY KEY,

    user_role ENUM(
        'Admin',
        'Teacher',
        'Student',
        'Parent'
    ) NOT NULL,

    user_id INT NOT NULL,

    institution_id INT,

    login_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    logout_time DATETIME,

    ip_address VARCHAR(45),

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- ============================================================
-- 28. NOTIFICATION
-- ============================================================

CREATE TABLE notification
(
    notification_id INT AUTO_INCREMENT PRIMARY KEY,

    user_role ENUM(
        'Admin',
        'Teacher',
        'Student',
        'Parent'
    ) NOT NULL,

    user_id INT NOT NULL,

    institution_id INT,

    title VARCHAR(200) NOT NULL,

    message TEXT NOT NULL,

    is_read BOOLEAN DEFAULT FALSE,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);


-- ============================================================
-- DATABASE CREATION COMPLETE
-- ============================================================

CREATE TABLE assign_academic_setup
(
    assign_academic_setup_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    course_academic_year_id INT NOT NULL,

    department_id INT,

    semester_id INT,

    subject_master_id INT NOT NULL,

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (course_academic_year_id)
        REFERENCES course_academic_year(course_academic_year_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (department_id)
        REFERENCES department_master(department_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    FOREIGN KEY (semester_id)
        REFERENCES semester_master(semester_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    FOREIGN KEY (subject_master_id)
        REFERENCES subject_master(subject_master_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    UNIQUE (
        institution_id,
        course_academic_year_id,
        department_id,
        semester_id,
        subject_master_id
    )
);
