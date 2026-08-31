-- ============================================================
-- EDUMATE DATABASE VERSION 3
-- INSERT / SAMPLE DATA SCRIPT
-- ============================================================

USE edumate_db3_2;


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
-- 2. COURSE MASTER
-- ============================================================

-- ------------------------------------------------------------
-- SCHOOL COURSES
-- ------------------------------------------------------------

INSERT INTO course_master
(
    course_name,
    institution_category,
    course_level
)
VALUES
('STD I', 'School', 'Primary'),
('STD II', 'School', 'Primary'),
('STD III', 'School', 'Primary'),
('STD IV', 'School', 'Primary'),
('STD V', 'School', 'Secondary'),
('STD VI', 'School', 'Secondary'),
('STD VII', 'School', 'Secondary'),
('STD VIII', 'School', 'Secondary'),
('STD IX', 'School', 'Secondary'),
('STD X', 'School', 'Secondary');


-- ------------------------------------------------------------
-- JUNIOR COLLEGE COURSES
-- ------------------------------------------------------------

INSERT INTO course_master
(
    course_name,
    institution_category,
    course_level,
    stream
)
VALUES
('FYJC ARTS', 'Jr College', 'Higher Secondary', 'Arts'),
('FYJC COMMERCE', 'Jr College', 'Higher Secondary', 'Commerce'),
('FYJC SCIENCE', 'Jr College', 'Higher Secondary', 'Science'),
('SYJC ARTS', 'Jr College', 'Higher Secondary', 'Arts'),
('SYJC COMMERCE', 'Jr College', 'Higher Secondary', 'Commerce'),
('SYJC SCIENCE', 'Jr College', 'Higher Secondary', 'Science');

-- ------------------------------------------------------------
-- DEGREE COLLEGE COURSES
-- ------------------------------------------------------------

INSERT INTO course_master
(
    course_name,
    institution_category,
    course_level,
    stream,
    specialization
)
VALUES

-- B.A.
(
    'F.Y.B.Arts - English Literature',
    'Degree College',
    'Undergraduate',
    'B.Arts',
    'English Literature'
),

(
    'F.Y.B.Arts - Journalism and Mass Communication',
    'Degree College',
    'Undergraduate',
    'B.Arts',
    'Journalism and Mass Communication'
),

(
    'S.Y.B.Arts - English Literature',
    'Degree College',
    'Undergraduate',
    'B.Arts',
    'English Literature'
),

(
    'S.Y.B.Arts - Journalism and Mass Communication',
    'Degree College',
    'Undergraduate',
    'B.Arts',
    'Journalism and Mass Communication'
),

(
    'T.Y.B.Arts - English Literature',
    'Degree College',
    'Undergraduate',
    'B.Arts',
    'English Literature'
),

(
    'T.Y.B.Arts - Journalism and Mass Communication',
    'Degree College',
    'Undergraduate',
    'B.Arts',
    'Journalism and Mass Communication'
),

-- B.Commerce
(
    'F.Y.B.Commerce - Financial Accounting',
    'Degree College',
    'Undergraduate',
    'B.Commerce',
    'Financial Accounting'
),

(
    'F.Y.B.Commerce - Business Administration',
    'Degree College',
    'Undergraduate',
    'B.Commerce',
    'Business Administration'
),

(
    'S.Y.B.Commerce - Financial Accounting',
    'Degree College',
    'Undergraduate',
    'B.Commerce',
    'Financial Accounting'
),

(
    'S.Y.B.Commerce - Business Administration',
    'Degree College',
    'Undergraduate',
    'B.Commerce',
    'Business Administration'
),

(
    'T.Y.B.Commerce - Financial Accounting',
    'Degree College',
    'Undergraduate',
    'B.Commerce',
    'Financial Accounting'
),

(
    'T.Y.B.Commerce - Business Administration',
    'Degree College',
    'Undergraduate',
    'B.Commerce',
    'Business Administration'
),

-- B.Science
(
    'F.Y.B.Science - Computer Science',
    'Degree College',
    'Undergraduate',
    'B.Science',
    'Computer Science'
),

(
    'F.Y.B.Science - Information Technology',
    'Degree College',
    'Undergraduate',
    'B.Science',
    'Information Technology'
),

(
    'S.Y.B.Science - Computer Science',
    'Degree College',
    'Undergraduate',
    'B.Science',
    'Computer Science'
),

(
    'S.Y.B.Science - Information Technology',
    'Degree College',
    'Undergraduate',
    'B.Science',
    'Information Technology'
),

(
    'T.Y.B.Science - Computer Science',
    'Degree College',
    'Undergraduate',
    'B.Science',
    'Computer Science'
),

(
    'T.Y.B.Science - Information Technology',
    'Degree College',
    'Undergraduate',
    'B.Science',
    'Information Technology'
);


-- ============================================================
-- 3. DEPARTMENT MASTER
-- GLOBAL MASTER LIST
-- ============================================================

INSERT INTO department_master
(
    department_name,
    institution_category
)
VALUES

-- School Departments
('English', 'School'),
('Hindi', 'School'),
('Science', 'School'),
('Mathematics', 'School'),
('Social Studies', 'School'),

-- Junior College Departments
('Arts', 'Jr College'),
('Science', 'Jr College'),
('Commerce', 'Jr College'),

-- Degree College Departments
('Computer Science', 'Degree College'),
('Information Technology', 'Degree College'),
('Data Science', 'Degree College'),
('BMS', 'Degree College');


-- ============================================================
-- 4. DESIGNATION MASTER
-- GLOBAL MASTER LIST
-- ============================================================

INSERT INTO designation_master
(
    designation_name,
    institution_category
)
VALUES

-- School
('Principal', 'School'),
('Vice Principal', 'School'),
('Head Master', 'School'),
('Head Mistress', 'School'),
('Teacher', 'School'),

-- Degree College
('Principal', 'Degree College'),
('Vice Principal', 'Degree College'),
('Head of Department', 'Degree College'),
('Professor', 'Degree College'),
('Assistant Professor', 'Degree College');


-- ============================================================
-- 5. INSTITUTION COURSE
-- COURSES OFFERED BY SUNRISE PUBLIC SCHOOL
-- ============================================================

INSERT INTO institution_course
(
    institution_id,
    course_id
)
SELECT
    i.institution_id,
    c.course_id
FROM institution i
JOIN course_master c
    ON c.institution_category = i.institution_category
WHERE i.institution_code = 'SPS001'
AND c.course_name IN
(
    'STD IX',
    'STD X'
);


-- ============================================================
-- 6. INSTITUTION COURSE
-- COURSES OFFERED BY BRIGHT FUTURE COLLEGE
-- ============================================================

INSERT INTO institution_course
(
    institution_id,
    course_id
)
SELECT
    i.institution_id,
    c.course_id
FROM institution i
JOIN course_master c
    ON c.institution_category = i.institution_category
WHERE i.institution_code = 'BFC001'
AND c.course_name IN
(
    'F.Y.B.Science - Computer Science',
    'S.Y.B.Science - Computer Science',
    'T.Y.B.Science - Computer Science',
    'F.Y.B.Science - Information Technology',
    'S.Y.B.Science - Information Technology',
    'T.Y.B.Science - Information Technology'
);


-- ============================================================
-- 7. INSTITUTION DEPARTMENT
-- SUNRISE PUBLIC SCHOOL
-- ============================================================

INSERT INTO institution_department
(
    institution_id,
    department_id
)
SELECT
    i.institution_id,
    d.department_id
FROM institution i
JOIN department_master d
    ON d.institution_category = i.institution_category
WHERE i.institution_code = 'SPS001'
AND d.department_name IN
(
    'English',
    'Hindi',
    'Science',
    'Mathematics',
    'Social Studies'
);


-- ============================================================
-- 8. INSTITUTION DEPARTMENT
-- BRIGHT FUTURE COLLEGE
-- ============================================================

INSERT INTO institution_department
(
    institution_id,
    department_id
)
SELECT
    i.institution_id,
    d.department_id
FROM institution i
JOIN department_master d
    ON d.institution_category = i.institution_category
WHERE i.institution_code = 'BFC001'
AND d.department_name IN
(
    'Computer Science',
    'Information Technology',
    'Data Science',
    'BMS'
);


-- ============================================================
-- 9. INSTITUTION DESIGNATION
-- SUNRISE PUBLIC SCHOOL
-- ============================================================

INSERT INTO institution_designation
(
    institution_id,
    designation_id
)
SELECT
    i.institution_id,
    d.designation_id
FROM institution i
JOIN designation_master d
    ON d.institution_category = i.institution_category
WHERE i.institution_code = 'SPS001'
AND d.designation_name IN
(
    'Principal',
    'Vice Principal',
    'Head Master',
    'Head Mistress',
    'Teacher'
);


-- ============================================================
-- 10. INSTITUTION DESIGNATION
-- BRIGHT FUTURE COLLEGE
-- ============================================================

INSERT INTO institution_designation
(
    institution_id,
    designation_id
)
SELECT
    i.institution_id,
    d.designation_id
FROM institution i
JOIN designation_master d
    ON d.institution_category = i.institution_category
WHERE i.institution_code = 'BFC001'
AND d.designation_name IN
(
    'Principal',
    'Vice Principal',
    'Head of Department',
    'Professor',
    'Assistant Professor'
);

-- ============================================================
-- 11. ADMIN
-- ============================================================

INSERT INTO admin
(
    institution_id,
    name,
    email,
    password
)
SELECT
    institution_id,
    'Sunrise Admin',
    'admin@sunrise.edu',
    'admin123'
FROM institution
WHERE institution_code = 'SPS001';


INSERT INTO admin
(
    institution_id,
    name,
    email,
    password
)
SELECT
    institution_id,
    'Bright Future Admin',
    'admin@brightfuture.edu',
    'admin123'
FROM institution
WHERE institution_code = 'BFC001';


-- ============================================================
-- 12. TEACHERS
-- SUNRISE PUBLIC SCHOOL
-- ============================================================

-- Priya Sharma - Science Teacher

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
SELECT
    i.institution_id,
    d.department_id,
    des.designation_id,
    'Priya Sharma',
    'priya@sunriseschool.edu',
    'teacher123',
    '9876500001'
FROM institution i
JOIN department_master d
    ON d.department_name = 'Science'
    AND d.institution_category = 'School'
JOIN designation_master des
    ON des.designation_name = 'Teacher'
    AND des.institution_category = 'School'
WHERE i.institution_code = 'SPS001';


-- Rahul Mehta - Mathematics Teacher

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
SELECT
    i.institution_id,
    d.department_id,
    des.designation_id,
    'Rahul Mehta',
    'rahul@sunriseschool.edu',
    'teacher123',
    '9876500002'
FROM institution i
JOIN department_master d
    ON d.department_name = 'Mathematics'
    AND d.institution_category = 'School'
JOIN designation_master des
    ON des.designation_name = 'Teacher'
    AND des.institution_category = 'School'
WHERE i.institution_code = 'SPS001';


-- ============================================================
-- 13. TEACHERS
-- BRIGHT FUTURE COLLEGE
-- ============================================================

-- Amit Patil - Computer Science

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
SELECT
    i.institution_id,
    d.department_id,
    des.designation_id,
    'Amit Patil',
    'amit@brightfuture.edu',
    'teacher123',
    '9876500003'
FROM institution i
JOIN department_master d
    ON d.department_name = 'Computer Science'
    AND d.institution_category = 'Degree College'
JOIN designation_master des
    ON des.designation_name = 'Assistant Professor'
    AND des.institution_category = 'Degree College'
WHERE i.institution_code = 'BFC001';


-- Neha Joshi - Information Technology

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
SELECT
    i.institution_id,
    d.department_id,
    des.designation_id,
    'Neha Joshi',
    'neha@brightfuture.edu',
    'teacher123',
    '9876500004'
FROM institution i
JOIN department_master d
    ON d.department_name = 'Information Technology'
    AND d.institution_category = 'Degree College'
JOIN designation_master des
    ON des.designation_name = 'Assistant Professor'
    AND des.institution_category = 'Degree College'
WHERE i.institution_code = 'BFC001';


-- ============================================================
-- 14. PARENTS
-- ============================================================

INSERT INTO parent
(
    institution_id,
    name,
    email,
    password,
    mobile
)
SELECT
    institution_id,
    'Ramesh Sharma',
    'ramesh@example.com',
    'parent123',
    '9876510001'
FROM institution
WHERE institution_code = 'SPS001';


INSERT INTO parent
(
    institution_id,
    name,
    email,
    password,
    mobile
)
SELECT
    institution_id,
    'Sunita Mehta',
    'sunita@example.com',
    'parent123',
    '9876510002'
FROM institution
WHERE institution_code = 'SPS001';


INSERT INTO parent
(
    institution_id,
    name,
    email,
    password,
    mobile
)
SELECT
    institution_id,
    'Suresh Patil',
    'suresh@example.com',
    'parent123',
    '9876510003'
FROM institution
WHERE institution_code = 'BFC001';


-- ============================================================
-- 15. STANDARDS
-- SUNRISE PUBLIC SCHOOL
-- ============================================================

INSERT INTO standard
(
    institution_id,
    course_id,
    standard_name,
    academic_year
)
SELECT
    i.institution_id,
    c.course_id,
    'Standard IX',
    '2026-27'
FROM institution i
JOIN course_master c
    ON c.course_name = 'STD IX'
    AND c.institution_category = 'School'
WHERE i.institution_code = 'SPS001';


INSERT INTO standard
(
    institution_id,
    course_id,
    standard_name,
    academic_year
)
SELECT
    i.institution_id,
    c.course_id,
    'Standard X',
    '2026-27'
FROM institution i
JOIN course_master c
    ON c.course_name = 'STD X'
    AND c.institution_category = 'School'
WHERE i.institution_code = 'SPS001';


-- ============================================================
-- 16. STANDARDS
-- BRIGHT FUTURE COLLEGE
-- ============================================================

INSERT INTO standard
(
    institution_id,
    course_id,
    standard_name,
    academic_year
)
SELECT
    i.institution_id,
    c.course_id,
    'FY',
    '2026-27'
FROM institution i
JOIN course_master c
    ON c.course_name = 'F.Y.B.Science - Computer Science'
    AND c.institution_category = 'Degree College'
WHERE i.institution_code = 'BFC001';


INSERT INTO standard
(
    institution_id,
    course_id,
    standard_name,
    academic_year
)
SELECT
    i.institution_id,
    c.course_id,
    'TY',
    '2026-27'
FROM institution i
JOIN course_master c
    ON c.course_name = 'T.Y.B.Science - Computer Science'
    AND c.institution_category = 'Degree College'
WHERE i.institution_code = 'BFC001';


-- ============================================================
-- 17. STUDENTS
-- SUNRISE PUBLIC SCHOOL
-- ============================================================

-- Aarav Sharma

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
    i.institution_id,
    p.parent_id,
    st.standard_id,
    'SPS1001',
    '1',
    'A',
    'Aarav Sharma',
    'aarav@sunriseschool.edu',
    'student123',
    NULL
FROM institution i
JOIN parent p
    ON p.email = 'ramesh@example.com'
JOIN standard st
    ON st.institution_id = i.institution_id
WHERE i.institution_code = 'SPS001'
AND st.standard_name = 'Standard X';


-- Ananya Mehta

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
    i.institution_id,
    p.parent_id,
    st.standard_id,
    'SPS1002',
    '2',
    'A',
    'Ananya Mehta',
    'ananya@sunriseschool.edu',
    'student123',
    NULL
FROM institution i
JOIN parent p
    ON p.email = 'sunita@example.com'
JOIN standard st
    ON st.institution_id = i.institution_id
WHERE i.institution_code = 'SPS001'
AND st.standard_name = 'Standard X';


-- ============================================================
-- 18. STUDENT
-- BRIGHT FUTURE COLLEGE
-- ============================================================

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
    i.institution_id,
    p.parent_id,
    st.standard_id,
    'BFC1001',
    '1',
    'A',
    'Rohan Patil',
    'rohan@brightfuture.edu',
    'student123',
    NULL
FROM institution i
JOIN parent p
    ON p.email = 'suresh@example.com'
JOIN standard st
    ON st.institution_id = i.institution_id
WHERE i.institution_code = 'BFC001'
AND st.standard_name = 'FY';


-- ============================================================
-- 19. SUBJECTS
-- SUNRISE PUBLIC SCHOOL - STANDARD X
-- ============================================================

INSERT INTO subject
(
    institution_id,
    standard_id,
    subject_name,
    assessment_type
)
SELECT
    st.institution_id,
    st.standard_id,
    'Mathematics',
    'Traditional'
FROM standard st
JOIN institution i
    ON i.institution_id = st.institution_id
WHERE i.institution_code = 'SPS001'
AND st.standard_name = 'Standard X';


INSERT INTO subject
(
    institution_id,
    standard_id,
    subject_name,
    assessment_type
)
SELECT
    st.institution_id,
    st.standard_id,
    'Science',
    'Traditional'
FROM standard st
JOIN institution i
    ON i.institution_id = st.institution_id
WHERE i.institution_code = 'SPS001'
AND st.standard_name = 'Standard X';


-- ============================================================
-- 20. SUBJECTS
-- BRIGHT FUTURE COLLEGE - FY
-- ============================================================

INSERT INTO subject
(
    institution_id,
    standard_id,
    subject_name,
    assessment_type
)
SELECT
    st.institution_id,
    st.standard_id,
    'Computer Networks',
    'OBE'
FROM standard st
JOIN institution i
    ON i.institution_id = st.institution_id
WHERE i.institution_code = 'BFC001'
AND st.standard_name = 'FY';


INSERT INTO subject
(
    institution_id,
    standard_id,
    subject_name,
    assessment_type
)
SELECT
    st.institution_id,
    st.standard_id,
    'Programming in Python',
    'OBE'
FROM standard st
JOIN institution i
    ON i.institution_id = st.institution_id
WHERE i.institution_code = 'BFC001'
AND st.standard_name = 'FY';


-- ============================================================
-- 21. TEACHER SUBJECT
-- SUNRISE
-- ============================================================

-- Rahul Mehta -> Mathematics

INSERT INTO teacher_subject
(
    teacher_id,
    subject_id
)
SELECT
    t.teacher_id,
    s.subject_id
FROM teacher t
JOIN subject s
    ON s.subject_name = 'Mathematics'
WHERE t.email = 'rahul@sunriseschool.edu'
AND s.institution_id = t.institution_id;


-- Priya Sharma -> Science

INSERT INTO teacher_subject
(
    teacher_id,
    subject_id
)
SELECT
    t.teacher_id,
    s.subject_id
FROM teacher t
JOIN subject s
    ON s.subject_name = 'Science'
WHERE t.email = 'priya@sunriseschool.edu'
AND s.institution_id = t.institution_id;


-- ============================================================
-- 22. TEACHER SUBJECT
-- BRIGHT FUTURE COLLEGE
-- ============================================================

-- Amit Patil -> Computer Networks

INSERT INTO teacher_subject
(
    teacher_id,
    subject_id
)
SELECT
    t.teacher_id,
    s.subject_id
FROM teacher t
JOIN subject s
    ON s.subject_name = 'Computer Networks'
WHERE t.email = 'amit@brightfuture.edu'
AND s.institution_id = t.institution_id;


-- Neha Joshi -> Programming in Python

INSERT INTO teacher_subject
(
    teacher_id,
    subject_id
)
SELECT
    t.teacher_id,
    s.subject_id
FROM teacher t
JOIN subject s
    ON s.subject_name = 'Programming in Python'
WHERE t.email = 'neha@brightfuture.edu'
AND s.institution_id = t.institution_id;


-- ============================================================
-- 23. CHAPTERS
-- MATHEMATICS
-- ============================================================

INSERT INTO chapter
(
    subject_id,
    chapter_number,
    chapter_name
)
SELECT
    subject_id,
    1,
    'Real Numbers'
FROM subject
WHERE institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'SPS001'
)
AND subject_name = 'Mathematics';


INSERT INTO chapter
(
    subject_id,
    chapter_number,
    chapter_name
)
SELECT
    subject_id,
    2,
    'Polynomials'
FROM subject
WHERE institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'SPS001'
)
AND subject_name = 'Mathematics';


-- ============================================================
-- 24. CHAPTERS
-- SCIENCE
-- ============================================================

INSERT INTO chapter
(
    subject_id,
    chapter_number,
    chapter_name
)
SELECT
    subject_id,
    1,
    'Chemical Reactions'
FROM subject
WHERE institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'SPS001'
)
AND subject_name = 'Science';


-- ============================================================
-- 25. CHAPTERS
-- COMPUTER NETWORKS
-- ============================================================

INSERT INTO chapter
(
    subject_id,
    chapter_number,
    chapter_name
)
SELECT
    subject_id,
    1,
    'Introduction to Computer Networks'
FROM subject
WHERE institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'BFC001'
)
AND subject_name = 'Computer Networks';


INSERT INTO chapter
(
    subject_id,
    chapter_number,
    chapter_name
)
SELECT
    subject_id,
    2,
    'Network Models'
FROM subject
WHERE institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'BFC001'
)
AND subject_name = 'Computer Networks';


-- ============================================================
-- 26. CHAPTERS
-- PYTHON
-- ============================================================

INSERT INTO chapter
(
    subject_id,
    chapter_number,
    chapter_name
)
SELECT
    subject_id,
    1,
    'Python Basics'
FROM subject
WHERE institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'BFC001'
)
AND subject_name = 'Programming in Python';


-- ============================================================
-- 27. COURSE OUTCOMES
-- COMPUTER NETWORKS
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
WHERE institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'BFC001'
)
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
WHERE institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'BFC001'
)
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
WHERE institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'BFC001'
)
AND subject_name = 'Computer Networks';


-- ============================================================
-- 28. QUESTIONS
-- COMPUTER NETWORKS - QUESTION 1
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
    i.institution_id,
    t.teacher_id,
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

FROM institution i

JOIN teacher t
    ON t.institution_id = i.institution_id
    AND t.email = 'amit@brightfuture.edu'

JOIN chapter ch
    ON ch.chapter_name = 'Network Models'

JOIN subject s
    ON s.subject_id = ch.subject_id
    AND s.subject_name = 'Computer Networks'
    AND s.institution_id = i.institution_id

JOIN course_outcome co
    ON co.subject_id = s.subject_id
    AND co.co_code = 'CO2'

WHERE i.institution_code = 'BFC001';


-- ============================================================
-- 29. QUESTIONS
-- COMPUTER NETWORKS - QUESTION 2
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
    i.institution_id,
    t.teacher_id,
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

FROM institution i

JOIN teacher t
    ON t.institution_id = i.institution_id
    AND t.email = 'amit@brightfuture.edu'

JOIN chapter ch
    ON ch.chapter_name = 'Introduction to Computer Networks'

JOIN subject s
    ON s.subject_id = ch.subject_id
    AND s.subject_name = 'Computer Networks'
    AND s.institution_id = i.institution_id

JOIN course_outcome co
    ON co.subject_id = s.subject_id
    AND co.co_code = 'CO1'

WHERE i.institution_code = 'BFC001';


-- ============================================================
-- 30. TEST
-- COMPUTER NETWORKS UNIT TEST 1
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
    i.institution_id,
    t.teacher_id,
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

FROM institution i

JOIN teacher t
    ON t.institution_id = i.institution_id
    AND t.email = 'amit@brightfuture.edu'

JOIN standard st
    ON st.institution_id = i.institution_id
    AND st.standard_name = 'FY'

JOIN subject s
    ON s.standard_id = st.standard_id
    AND s.subject_name = 'Computer Networks'

WHERE i.institution_code = 'BFC001';


-- ============================================================
-- 31. TEST QUESTIONS
-- ============================================================

INSERT INTO test_question
(
    test_id,
    question_id
)
SELECT
    t.test_id,
    q.question_id

FROM test t

JOIN question q
    ON q.institution_id = t.institution_id

JOIN chapter ch
    ON ch.chapter_id = q.chapter_id

JOIN subject s
    ON s.subject_id = ch.subject_id
    AND s.subject_id = t.subject_id

WHERE t.test_name = 'Computer Networks Unit Test 1'
AND t.institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'BFC001'
)

ORDER BY q.question_id
LIMIT 2;


-- ============================================================
-- 32. TEST ATTEMPT
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
    AND s.email = 'rohan@brightfuture.edu'

WHERE t.test_name = 'Computer Networks Unit Test 1';


-- ============================================================
-- 33. STUDENT ANSWERS
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

JOIN student s
    ON s.student_id = ta.student_id

WHERE s.email = 'rohan@brightfuture.edu'
AND ta.test_id =
(
    SELECT test_id
    FROM test
    WHERE test_name = 'Computer Networks Unit Test 1'
);


-- ============================================================
-- 34. LOGIN HISTORY
-- ============================================================

-- Admin Login

INSERT INTO login_history
(
    institution_id,
    user_role,
    user_id,
    ip_address,
    device_info
)
SELECT
    i.institution_id,
    'Admin',
    a.admin_id,
    '127.0.0.1',
    'Chrome on Windows'

FROM institution i

JOIN admin a
    ON a.institution_id = i.institution_id

WHERE i.institution_code = 'SPS001';


-- Teacher Login

INSERT INTO login_history
(
    institution_id,
    user_role,
    user_id,
    ip_address,
    device_info
)
SELECT
    i.institution_id,
    'Teacher',
    t.teacher_id,
    '127.0.0.1',
    'Chrome on Windows'

FROM institution i

JOIN teacher t
    ON t.institution_id = i.institution_id
    AND t.email = 'amit@brightfuture.edu'

WHERE i.institution_code = 'BFC001';


-- Student Login

INSERT INTO login_history
(
    institution_id,
    user_role,
    user_id,
    ip_address,
    device_info
)
SELECT
    i.institution_id,
    'Student',
    s.student_id,
    '127.0.0.1',
    'Chrome on Windows'

FROM institution i

JOIN student s
    ON s.institution_id = i.institution_id
    AND s.email = 'rohan@brightfuture.edu'

WHERE i.institution_code = 'BFC001';


-- ============================================================
-- 35. NOTIFICATIONS
-- ============================================================

-- Student Notification

INSERT INTO notification
(
    institution_id,
    user_role,
    user_id,
    title,
    message
)
SELECT
    i.institution_id,
    'Student',
    s.student_id,
    'New Test Available',
    'Computer Networks Unit Test 1 is now available.'

FROM institution i

JOIN student s
    ON s.institution_id = i.institution_id
    AND s.email = 'rohan@brightfuture.edu'

WHERE i.institution_code = 'BFC001';


-- Teacher Notification

INSERT INTO notification
(
    institution_id,
    user_role,
    user_id,
    title,
    message
)
SELECT
    i.institution_id,
    'Teacher',
    t.teacher_id,
    'Test Published',
    'Your Computer Networks Unit Test 1 has been published successfully.'

FROM institution i

JOIN teacher t
    ON t.institution_id = i.institution_id
    AND t.email = 'amit@brightfuture.edu'

WHERE i.institution_code = 'BFC001';


-- Student Welcome Notification

INSERT INTO notification
(
    institution_id,
    user_role,
    user_id,
    title,
    message
)
SELECT
    i.institution_id,
    'Student',
    s.student_id,
    'Welcome',
    'Welcome to EduMate.'

FROM institution i

JOIN student s
    ON s.institution_id = i.institution_id
    AND s.email = 'aarav@sunriseschool.edu'

WHERE i.institution_code = 'SPS001';


-- ============================================================
-- END OF INSERT SCRIPT
-- ============================================================