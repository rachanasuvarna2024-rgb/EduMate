-- ============================================================
-- EDUMATE DATABASE VERSION 3
-- Institution Management + Academic Structure
-- ============================================================

DROP DATABASE IF EXISTS edumate_db3;

CREATE DATABASE edumate_db3;

USE edumate_db3;


-- ============================================================
-- 1. INSTITUTION MASTER TABLE
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
-- 2. COURSE MASTER TABLE
-- Predefined courses available in EduMate
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

    course_level VARCHAR(50),

    stream VARCHAR(100),

    specialization VARCHAR(150),

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    UNIQUE (
        course_name,
        institution_category
    )
);


-- ============================================================
-- 3. INSTITUTION COURSE TABLE
-- Stores courses offered by each institution
-- ============================================================

CREATE TABLE institution_course
(
    institution_course_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    course_id INT NOT NULL,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE,

    FOREIGN KEY (course_id)
        REFERENCES course_master(course_id)
        ON DELETE RESTRICT,

    UNIQUE (
        institution_id,
        course_id
    )
);


-- ============================================================
-- 4. DEPARTMENT MASTER TABLE
-- Institution-specific departments
-- ============================================================

CREATE TABLE department_master
(
    department_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    department_name VARCHAR(100) NOT NULL,

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE,

    UNIQUE (
        institution_id,
        department_name
    )
);


-- ============================================================
-- 5. DESIGNATION MASTER TABLE
-- Institution-specific teaching designations
-- ============================================================

CREATE TABLE designation_master
(
    designation_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    designation_name VARCHAR(100) NOT NULL,

    status ENUM(
        'Active',
        'Inactive'
    ) DEFAULT 'Active',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (institution_id)
        REFERENCES institution(institution_id)
        ON DELETE CASCADE,

    UNIQUE (
        institution_id,
        designation_name
    )
);


-- ============================================================
-- 6. ADMIN TABLE
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
-- 7. TEACHER TABLE
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
-- 8. PARENT TABLE
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
-- 9. STANDARD TABLE
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
-- 10. STUDENT TABLE
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
-- 11. SUBJECT TABLE
-- ============================================================

CREATE TABLE subject
(
    subject_id INT AUTO_INCREMENT PRIMARY KEY,

    institution_id INT NOT NULL,

    standard_id INT NOT NULL,

    subject_name VARCHAR(100) NOT NULL,

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

    UNIQUE (
        standard_id,
        subject_name
    )
);


-- ============================================================
-- 12. TEACHER_SUBJECT TABLE
-- Many-to-many relationship
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
-- 13. CHAPTER TABLE
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
-- 14. COURSE OUTCOME TABLE
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
-- 15. QUESTION TABLE
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

    CHECK (correct_option IN ('A','B','C','D'))
);


-- ============================================================
-- 16. TEST TABLE
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
-- 17. TEST_QUESTION TABLE
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
-- 18. TEST_ATTEMPT TABLE
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
-- 19. STUDENT_ANSWER TABLE
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
-- 20. LOGIN_HISTORY TABLE
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
-- 21. NOTIFICATION TABLE
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

