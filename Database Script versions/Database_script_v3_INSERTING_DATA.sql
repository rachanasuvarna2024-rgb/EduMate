-- INSERT SCRIPTS (edumatedb3)
USE edumate_db3;

-- ============================================================
-- 1. INSTITUTIONS
-- ============================================================

INSERT INTO institution
(
    institution_name,
    institution_code,
    institution_category,
    institution_type,
    address,
    city,
    state,
    pincode,
    email,
    phone,
    website
)
VALUES
(
    'Sunrise Public School',
    'SPS001',
    'School',
    'Traditional',
    '12 MG Road',
    'Mumbai',
    'Maharashtra',
    '400080',
    'info@sunriseschool.edu',
    '9876543210',
    'www.sunriseschool.edu'
),

(
    'Bright Future College',
    'BFC001',
    'Degree College',
    'OBE',
    '45 College Road',
    'Mumbai',
    'Maharashtra',
    '400070',
    'info@brightfuture.edu',
    '9876543211',
    'www.brightfuture.edu'
);

-- ============================================================
-- 2. SCHOOL COURSES
-- ============================================================

INSERT INTO course_master
(course_name, institution_category, course_level)
VALUES
('STD I', 'School', 'STD I'),
('STD II', 'School', 'STD II'),
('STD III', 'School', 'STD III'),
('STD IV', 'School', 'STD IV'),
('STD V', 'School', 'STD V'),
('STD VI', 'School', 'STD VI'),
('STD VII', 'School', 'STD VII'),
('STD VIII', 'School', 'STD VIII'),
('STD IX', 'School', 'STD IX'),
('STD X', 'School', 'STD X');


-- ============================================================
-- 3. JUNIOR COLLEGE COURSES
-- ============================================================

INSERT INTO course_master
(course_name, institution_category, course_level, stream)
VALUES
('FYJC ARTS', 'Jr College', 'FYJC', 'Arts'),
('FYJC COMMERCE', 'Jr College', 'FYJC', 'Commerce'),
('FYJC SCIENCE', 'Jr College', 'FYJC', 'Science'),
('SYJC ARTS', 'Jr College', 'SYJC', 'Arts'),
('SYJC COMMERCE', 'Jr College', 'SYJC', 'Commerce'),
('SYJC SCIENCE', 'Jr College', 'SYJC', 'Science');


-- ============================================================
-- 4. DEGREE COLLEGE COURSES
-- ============================================================

INSERT INTO course_master
(course_name, institution_category, course_level, stream, specialization)
VALUES

-- B.A.
('F.Y.B.Arts - English Literature',
 'Degree College', 'FY', 'B.Arts', 'English Literature'),

('F.Y.B.Arts - Journalism and Mass Communication',
 'Degree College', 'FY', 'B.Arts',
 'Journalism and Mass Communication'),

('S.Y.B.Arts - English Literature',
 'Degree College', 'SY', 'B.Arts', 'English Literature'),

('S.Y.B.Arts - Journalism and Mass Communication',
 'Degree College', 'SY', 'B.Arts',
 'Journalism and Mass Communication'),

('T.Y.B.Arts - English Literature',
 'Degree College', 'TY', 'B.Arts', 'English Literature'),

('T.Y.B.Arts - Journalism and Mass Communication',
 'Degree College', 'TY', 'B.Arts',
 'Journalism and Mass Communication'),


-- B.Commerce
('F.Y.B.Commerce - Financial Accounting',
 'Degree College', 'FY', 'B.Commerce',
 'Financial Accounting'),

('F.Y.B.Commerce - Business Administration',
 'Degree College', 'FY', 'B.Commerce',
 'Business Administration'),

('S.Y.B.Commerce - Financial Accounting',
 'Degree College', 'SY', 'B.Commerce',
 'Financial Accounting'),

('S.Y.B.Commerce - Business Administration',
 'Degree College', 'SY', 'B.Commerce',
 'Business Administration'),

('T.Y.B.Commerce - Financial Accounting',
 'Degree College', 'TY', 'B.Commerce',
 'Financial Accounting'),

('T.Y.B.Commerce - Business Administration',
 'Degree College', 'TY', 'B.Commerce',
 'Business Administration'),


-- B.Science
('F.Y.B.Science - Computer Science',
 'Degree College', 'FY', 'B.Science',
 'Computer Science'),

('F.Y.B.Science - Information Technology',
 'Degree College', 'FY', 'B.Science',
 'Information Technology'),

('S.Y.B.Science - Computer Science',
 'Degree College', 'SY', 'B.Science',
 'Computer Science'),

('S.Y.B.Science - Information Technology',
 'Degree College', 'SY', 'B.Science',
 'Information Technology'),

('T.Y.B.Science - Computer Science',
 'Degree College', 'TY', 'B.Science',
 'Computer Science'),

('T.Y.B.Science - Information Technology',
 'Degree College', 'TY', 'B.Science',
 'Information Technology');


-- ============================================================
-- 5. COURSES OFFERED BY SUNRISE PUBLIC SCHOOL
-- ============================================================

INSERT INTO institution_course
(institution_id, course_id)
SELECT
    1,
    course_id
FROM course_master
WHERE institution_category = 'School'
AND course_name IN
(
    'STD IX',
    'STD X'
);


-- ============================================================
-- 6. COURSES OFFERED BY BRIGHT FUTURE COLLEGE
-- ============================================================

INSERT INTO institution_course
(institution_id, course_id)
SELECT
    2,
    course_id
FROM course_master
WHERE institution_category = 'Degree College'
AND course_name IN
(
    'F.Y.B.Science - Computer Science',
    'S.Y.B.Science - Computer Science',
    'T.Y.B.Science - Computer Science',
    'F.Y.B.Science - Information Technology',
    'S.Y.B.Science - Information Technology',
    'T.Y.B.Science - Information Technology'
);

-- ============================================================
-- 7. DEPARTMENTS
-- ============================================================

-- Sunrise Public School
INSERT INTO department_master
(institution_id, department_name)
VALUES
(1, 'English'),
(1, 'Hindi'),
(1, 'Science'),
(1, 'Mathematics'),
(1, 'Social Studies');


-- Bright Future College
INSERT INTO department_master
(institution_id, department_name)
VALUES
(2, 'Computer Science'),
(2, 'Information Technology'),
(2, 'Data Science'),
(2, 'BMS');

-- ============================================================
-- 8. DESIGNATIONS
-- ============================================================

INSERT INTO designation_master
(institution_id, designation_name)
VALUES
(1, 'Principal'),
(1, 'Vice Principal'),
(1, 'Head Master'),
(1, 'Head Mistress'),
(1, 'Teacher'),

(2, 'Principal'),
(2, 'Vice Principal'),
(2, 'Head of Department'),
(2, 'Professor'),
(2, 'Assistant Professor');

-- ============================================================
-- 9. ADMIN
-- ============================================================

INSERT INTO admin
(
    institution_id,
    name,
    email,
    password
)
VALUES
(
    1,
    'Sunrise Admin',
    'admin@sunrise.edu',
    'admin123'
),

(
    2,
    'Bright Future Admin',
    'admin@brightfuture.edu',
    'admin123'
);

-- ============================================================
-- 10. TEACHERS
-- ============================================================

-- Sunrise School Teachers

INSERT INTO teacher
(
    institution_id,
    department_id,
    designation_id,
    name,
    email,
    password,
    mobile
)
VALUES
(
    1,
    3,
    5,
    'Priya Sharma',
    'priya@sunriseschool.edu',
    'teacher123',
    '9876500001'
),

(
    1,
    4,
    5,
    'Rahul Mehta',
    'rahul@sunriseschool.edu',
    'teacher123',
    '9876500002'
);


-- Bright Future College Teachers

INSERT INTO teacher
(
    institution_id,
    department_id,
    designation_id,
    name,
    email,
    password,
    mobile
)
VALUES
(
    2,
    6,
    10,
    'Amit Patil',
    'amit@brightfuture.edu',
    'teacher123',
    '9876500003'
),

(
    2,
    7,
    10,
    'Neha Joshi',
    'neha@brightfuture.edu',
    'teacher123',
    '9876500004'
);

-- ============================================================
-- 11. PARENTS
-- ============================================================

INSERT INTO parent
(
    institution_id,
    name,
    email,
    password,
    mobile
)
VALUES
(
    1,
    'Ramesh Sharma',
    'ramesh@example.com',
    'parent123',
    '9876510001'
),

(
    1,
    'Sunita Mehta',
    'sunita@example.com',
    'parent123',
    '9876510002'
),

(
    2,
    'Suresh Patil',
    'suresh@example.com',
    'parent123',
    '9876510003'
);

-- ============================================================
-- 12. STANDARDS
-- ============================================================

-- Sunrise Public School
-- STD IX course_id = obtained dynamically

INSERT INTO standard
(
    institution_id,
    course_id,
    standard_name,
    academic_year
)
SELECT
    1,
    course_id,
    'Standard IX',
    '2026-27'
FROM course_master
WHERE course_name = 'STD IX'
AND institution_category = 'School';


INSERT INTO standard
(
    institution_id,
    course_id,
    standard_name,
    academic_year
)
SELECT
    1,
    course_id,
    'Standard X',
    '2026-27'
FROM course_master
WHERE course_name = 'STD X'
AND institution_category = 'School';


-- Bright Future College

INSERT INTO standard
(
    institution_id,
    course_id,
    standard_name,
    academic_year
)
SELECT
    2,
    course_id,
    'FY',
    '2026-27'
FROM course_master
WHERE course_name = 'F.Y.B.Science - Computer Science';


INSERT INTO standard
(
    institution_id,
    course_id,
    standard_name,
    academic_year
)
SELECT
    2,
    course_id,
    'TY',
    '2026-27'
FROM course_master
WHERE course_name = 'T.Y.B.Science - Computer Science';

-- ============================================================
-- 13. STUDENTS
-- ============================================================

-- Sunrise students

INSERT INTO student
(
    institution_id,
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
SELECT
    1,
    1,
    standard_id,
    'SPS1001',
    '1',
    'A',
    'Aarav Sharma',
    'aarav@sunriseschool.edu',
    'student123',
    NULL
FROM standard
WHERE institution_id = 1
AND standard_name = 'Standard X';


INSERT INTO student
(
    institution_id,
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
SELECT
    1,
    2,
    standard_id,
    'SPS1002',
    '2',
    'A',
    'Ananya Mehta',
    'ananya@sunriseschool.edu',
    'student123',
    NULL
FROM standard
WHERE institution_id = 1
AND standard_name = 'Standard X';


-- Bright Future student

INSERT INTO student
(
    institution_id,
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
SELECT
    2,
    3,
    standard_id,
    'BFC1001',
    '1',
    'A',
    'Rohan Patil',
    'rohan@brightfuture.edu',
    'student123',
    NULL
FROM standard
WHERE institution_id = 2
AND standard_name = 'FY';

-- ============================================================
-- 14. SUBJECTS
-- ============================================================

-- Sunrise Standard X

INSERT INTO subject
(
    institution_id,
    standard_id,
    subject_name,
    assessment_type
)
SELECT
    1,
    standard_id,
    'Mathematics',
    'Traditional'
FROM standard
WHERE institution_id = 1
AND standard_name = 'Standard X';


INSERT INTO subject
(
    institution_id,
    standard_id,
    subject_name,
    assessment_type
)
SELECT
    1,
    standard_id,
    'Science',
    'Traditional'
FROM standard
WHERE institution_id = 1
AND standard_name = 'Standard X';


-- Bright Future FY B.Sc Computer Science

INSERT INTO subject
(
    institution_id,
    standard_id,
    subject_name,
    assessment_type
)
SELECT
    2,
    standard_id,
    'Computer Networks',
    'OBE'
FROM standard
WHERE institution_id = 2
AND standard_name = 'FY';


INSERT INTO subject
(
    institution_id,
    standard_id,
    subject_name,
    assessment_type
)
SELECT
    2,
    standard_id,
    'Programming in Python',
    'OBE'
FROM standard
WHERE institution_id = 2
AND standard_name = 'FY';

-- ============================================================
-- 15. TEACHER SUBJECT
-- ============================================================

-- Sunrise Mathematics teacher

INSERT INTO teacher_subject
(teacher_id, subject_id)
SELECT
    2,
    subject_id
FROM subject
WHERE institution_id = 1
AND subject_name = 'Mathematics';


-- Sunrise Science teacher

INSERT INTO teacher_subject
(teacher_id, subject_id)
SELECT
    1,
    subject_id
FROM subject
WHERE institution_id = 1
AND subject_name = 'Science';


-- Bright Future Computer Networks teacher

INSERT INTO teacher_subject
(teacher_id, subject_id)
SELECT
    3,
    subject_id
FROM subject
WHERE institution_id = 2
AND subject_name = 'Computer Networks';


-- Bright Future Python teacher

INSERT INTO teacher_subject
(teacher_id, subject_id)
SELECT
    4,
    subject_id
FROM subject
WHERE institution_id = 2
AND subject_name = 'Programming in Python';

-- ============================================================
-- 16. CHAPTERS
-- ============================================================

-- Mathematics

INSERT INTO chapter
(subject_id, chapter_number, chapter_name)
SELECT
    subject_id,
    1,
    'Real Numbers'
FROM subject
WHERE institution_id = 1
AND subject_name = 'Mathematics';


INSERT INTO chapter
(subject_id, chapter_number, chapter_name)
SELECT
    subject_id,
    2,
    'Polynomials'
FROM subject
WHERE institution_id = 1
AND subject_name = 'Mathematics';


-- Science

INSERT INTO chapter
(subject_id, chapter_number, chapter_name)
SELECT
    subject_id,
    1,
    'Chemical Reactions'
FROM subject
WHERE institution_id = 1
AND subject_name = 'Science';


-- Computer Networks

INSERT INTO chapter
(subject_id, chapter_number, chapter_name)
SELECT
    subject_id,
    1,
    'Introduction to Computer Networks'
FROM subject
WHERE institution_id = 2
AND subject_name = 'Computer Networks';


INSERT INTO chapter
(subject_id, chapter_number, chapter_name)
SELECT
    subject_id,
    2,
    'Network Models'
FROM subject
WHERE institution_id = 2
AND subject_name = 'Computer Networks';


-- Python

INSERT INTO chapter
(subject_id, chapter_number, chapter_name)
SELECT
    subject_id,
    1,
    'Python Basics'
FROM subject
WHERE institution_id = 2
AND subject_name = 'Programming in Python';

-- ============================================================
-- 17. COURSE OUTCOMES
-- ============================================================

INSERT INTO course_outcome
(
    subject_id,
    co_code,
    co_description
)
SELECT
    subject_id,
    'CO1',
    'Understand fundamental concepts of computer networks'
FROM subject
WHERE institution_id = 2
AND subject_name = 'Computer Networks';


INSERT INTO course_outcome
(
    subject_id,
    co_code,
    co_description
)
SELECT
    subject_id,
    'CO2',
    'Explain different network models and protocols'
FROM subject
WHERE institution_id = 2
AND subject_name = 'Computer Networks';


INSERT INTO course_outcome
(
    subject_id,
    co_code,
    co_description
)
SELECT
    subject_id,
    'CO3',
    'Apply networking concepts to solve basic problems'
FROM subject
WHERE institution_id = 2
AND subject_name = 'Computer Networks';

-- ============================================================
-- 18. QUESTIONS
-- ============================================================

INSERT INTO question
(
    institution_id,
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
SELECT
    2,
    3,
    ch.chapter_id,
    co.co_id,
    'Which layer of the OSI model is responsible for routing?',
    'Physical',
    'Network',
    'Transport',
    'Session',
    'B',
    'Easy',
    'Teacher',
    1
FROM chapter ch
JOIN subject s
    ON ch.subject_id = s.subject_id
JOIN course_outcome co
    ON co.subject_id = s.subject_id
WHERE s.institution_id = 2
AND s.subject_name = 'Computer Networks'
AND ch.chapter_name = 'Network Models'
AND co.co_code = 'CO1';


INSERT INTO question
(
    institution_id,
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
SELECT
    2,
    3,
    ch.chapter_id,
    co.co_id,
    'Which protocol is connection oriented?',
    'UDP',
    'IP',
    'TCP',
    'ARP',
    'C',
    'Medium',
    'Teacher',
    1
FROM chapter ch
JOIN subject s
    ON ch.subject_id = s.subject_id
JOIN course_outcome co
    ON co.subject_id = s.subject_id
WHERE s.institution_id = 2
AND s.subject_name = 'Computer Networks'
AND ch.chapter_name = 'Introduction to Computer Networks'
AND co.co_code = 'CO2';

-- ============================================================
-- 19. TESTS
-- ============================================================

INSERT INTO test
(
    institution_id,
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
SELECT
    2,
    3,
    st.standard_id,
    s.subject_id,
    'Computer Networks Unit Test 1',
    2,
    2,
    1,
    1,
    0,
    20,
    'Answer all questions.',
    'Published',
    '2026-08-25 10:00:00'
FROM standard st
JOIN subject s
    ON s.standard_id = st.standard_id
WHERE st.institution_id = 2
AND st.standard_name = 'FY'
AND s.subject_name = 'Computer Networks';

-- ============================================================
-- 20. TEST QUESTIONS
-- ============================================================

INSERT INTO test_question
(test_id, question_id)

SELECT
    t.test_id,
    q.question_id

FROM test t

JOIN
(
    SELECT
        q.question_id
    FROM question q
    JOIN chapter ch
        ON q.chapter_id = ch.chapter_id
    JOIN subject s
        ON ch.subject_id = s.subject_id

    WHERE q.institution_id = 2
      AND s.subject_name = 'Computer Networks'

    ORDER BY q.question_id
    LIMIT 2
) AS q

WHERE t.test_name = 'Computer Networks Unit Test 1'
  AND t.institution_id = 2;
-- ============================================================
-- 21. TEST ATTEMPT
-- ============================================================

INSERT INTO test_attempt
(
    test_id,
    student_id,
    start_time,
    end_time,
    score,
    percentage,
    attempt_status,
    submitted_at
)
SELECT
    t.test_id,
    s.student_id,
    '2026-08-25 10:00:00',
    '2026-08-25 10:15:00',
    2,
    100,
    'Completed',
    '2026-08-25 10:15:00'
FROM test t
JOIN student s
    ON s.institution_id = t.institution_id
WHERE t.test_name = 'Computer Networks Unit Test 1'
AND s.name = 'Rohan Patil';

-- ============================================================
-- 22. STUDENT ANSWERS
-- ============================================================

INSERT INTO student_answer
(
    attempt_id,
    question_id,
    selected_option,
    is_correct,
    marks_obtained
)
SELECT
    ta.attempt_id,
    q.question_id,
    q.correct_option,
    TRUE,
    q.marks
FROM test_attempt ta
JOIN test_question tq
    ON tq.test_id = ta.test_id
JOIN question q
    ON q.question_id = tq.question_id
WHERE ta.attempt_id = 1;

-- ============================================================
-- 23. LOGIN HISTORY
-- ============================================================

INSERT INTO login_history
(
    institution_id,
    user_role,
    user_id,
    ip_address,
    device_info
)
VALUES
(
    1,
    'Admin',
    1,
    '127.0.0.1',
    'Chrome on Windows'
),

(
    2,
    'Teacher',
    3,
    '127.0.0.1',
    'Chrome on Windows'
),

(
    2,
    'Student',
    3,
    '127.0.0.1',
    'Chrome on Windows'
);

-- ============================================================
-- 24. NOTIFICATIONS
-- ============================================================

INSERT INTO notification
(
    institution_id,
    user_role,
    user_id,
    title,
    message
)
VALUES
(
    2,
    'Student',
    3,
    'New Test Available',
    'Computer Networks Unit Test 1 is now available.'
),

(
    2,
    'Teacher',
    3,
    'Test Published',
    'Your Computer Networks Unit Test 1 has been published successfully.'
),

(
    1,
    'Student',
    1,
    'Welcome',
    'Welcome to EduMate.'
);


