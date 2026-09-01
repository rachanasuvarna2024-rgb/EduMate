-- ============================================================
-- EDUMATE DATABASE VERSION 3.3
-- COMPLETE INSERT / SAMPLE DATA SCRIPT
-- ============================================================

USE edumate_db3_3;

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
),
(
    'Bright Junior College',
    'BJC001',
    'Jr College',
    'Traditional',
    '25 College Road',
    'Mumbai',
    'Maharashtra',
    '400071',
    'info@brightjunior.edu',
    '9876543212',
    'www.brightjunior.edu'
);


-- ============================================================
-- 2. STREAM MASTER
-- ============================================================

INSERT INTO stream_master
(
    stream_name,
    institution_category
)
VALUES

-- SCHOOL
('English Medium', 'School'),
('Hindi Medium', 'School'),
('Marathi Medium', 'School'),
('Kannada Medium', 'School'),

-- JR COLLEGE
('Arts', 'Jr College'),
('Science', 'Jr College'),
('Commerce', 'Jr College'),

-- DEGREE COLLEGE
('Arts', 'Degree College'),
('Science', 'Degree College'),
('Commerce', 'Degree College');


-- ============================================================
-- 3. COURSE MASTER
-- ============================================================


-- ============================================================
-- SCHOOL COURSES
-- ============================================================

INSERT INTO course_master
(
    course_name,
    stream_id,
    institution_category
)
SELECT
    c.course_name,
    s.stream_id,
    'School'
FROM
(
    SELECT 'I' AS course_name
    UNION ALL SELECT 'II'
    UNION ALL SELECT 'III'
    UNION ALL SELECT 'IV'
    UNION ALL SELECT 'V'
    UNION ALL SELECT 'VI'
    UNION ALL SELECT 'VII'
    UNION ALL SELECT 'VIII'
    UNION ALL SELECT 'IX'
    UNION ALL SELECT 'X'
) c
CROSS JOIN stream_master s
WHERE s.institution_category = 'School';


-- ============================================================
-- JR COLLEGE COURSES
-- ============================================================

INSERT INTO course_master
(
    course_name,
    stream_id,
    institution_category
)
SELECT
    c.course_name,
    s.stream_id,
    'Jr College'
FROM
(
    SELECT 'FY JC Arts' AS course_name, 'Arts' AS stream_name
    UNION ALL SELECT 'SY JC Arts', 'Arts'

    UNION ALL SELECT 'FY JC Science', 'Science'
    UNION ALL SELECT 'SY JC Science', 'Science'

    UNION ALL SELECT 'FY JC Commerce', 'Commerce'
    UNION ALL SELECT 'SY JC Commerce', 'Commerce'
) c
JOIN stream_master s
    ON s.stream_name = c.stream_name
    AND s.institution_category = 'Jr College';


-- ============================================================
-- DEGREE COLLEGE COURSES
-- ============================================================

INSERT INTO course_master
(
    course_name,
    stream_id,
    institution_category
)
SELECT
    c.course_name,
    s.stream_id,
    'Degree College'
FROM
(
    SELECT
        'FY B Arts English Literature' AS course_name,
        'Arts' AS stream_name

    UNION ALL
    SELECT
        'SY B Arts English Literature',
        'Arts'

    UNION ALL
    SELECT
        'TY B Arts English Literature',
        'Arts'

    UNION ALL
    SELECT
        'FY B Science Computer Science',
        'Science'

    UNION ALL
    SELECT
        'SY B Science Computer Science',
        'Science'

    UNION ALL
    SELECT
        'TY B Science Computer Science',
        'Science'

    UNION ALL
    SELECT
        'FY B Commerce Financial Accounting',
        'Commerce'

    UNION ALL
    SELECT
        'SY B Commerce Financial Accounting',
        'Commerce'

    UNION ALL
    SELECT
        'TY B Commerce Financial Accounting',
        'Commerce'
) c
JOIN stream_master s
    ON s.stream_name = c.stream_name
    AND s.institution_category = 'Degree College';


-- ============================================================
-- 4. SUBJECT MASTER
-- ============================================================


-- ============================================================
-- SCHOOL SUBJECTS
--
-- English
-- Maths
-- Science
-- Social Science
-- Hindi
--
-- Applied to every school course.
-- ============================================================

INSERT INTO subject_master
(
    subject_name,
    course_id,
    institution_category
)
SELECT
    sub.subject_name,
    c.course_id,
    'School'
FROM course_master c
JOIN
(
    SELECT 'English' AS subject_name
    UNION ALL SELECT 'Maths'
    UNION ALL SELECT 'Science'
    UNION ALL SELECT 'Social Science'
    UNION ALL SELECT 'Hindi'
) sub
WHERE c.institution_category = 'School';


-- ============================================================
-- JR COLLEGE SUBJECTS
-- ============================================================

INSERT INTO subject_master
(
    subject_name,
    course_id,
    institution_category
)
SELECT
    sub.subject_name,
    c.course_id,
    'Jr College'
FROM course_master c
JOIN
(
    SELECT 'FY JC Arts' AS course_name,
           'JC Arts - Economics' AS subject_name

    UNION ALL
    SELECT 'FY JC Arts',
           'JC Arts - Political Science'

    UNION ALL
    SELECT 'SY JC Arts',
           'JC Arts - Economics'

    UNION ALL
    SELECT 'SY JC Arts',
           'JC Arts - Political Science'

    UNION ALL
    SELECT 'FY JC Science',
           'JC Science - Physics'

    UNION ALL
    SELECT 'FY JC Science',
           'JC Science - Chemistry'

    UNION ALL
    SELECT 'FY JC Science',
           'JC Science - Biology'

    UNION ALL
    SELECT 'SY JC Science',
           'JC Science - Physics'

    UNION ALL
    SELECT 'SY JC Science',
           'JC Science - Chemistry'

    UNION ALL
    SELECT 'SY JC Science',
           'JC Science - Biology'

    UNION ALL
    SELECT 'FY JC Commerce',
           'JC Commerce - Organization of Commerce and Management'

    UNION ALL
    SELECT 'FY JC Commerce',
           'JC Commerce - Book Keeping'

    UNION ALL
    SELECT 'SY JC Commerce',
           'JC Commerce - Organization of Commerce and Management'

    UNION ALL
    SELECT 'SY JC Commerce',
           'JC Commerce - Book Keeping'
) sub
    ON sub.course_name = c.course_name
WHERE c.institution_category = 'Jr College';


-- ============================================================
-- DEGREE COLLEGE SUBJECTS
-- ============================================================

INSERT INTO subject_master
(
    subject_name,
    course_id,
    institution_category
)
SELECT
    sub.subject_name,
    c.course_id,
    'Degree College'
FROM course_master c
JOIN
(
    SELECT
        'FY B Arts English Literature' AS course_name,
        'English Literature' AS subject_name

    UNION ALL
    SELECT
        'SY B Arts English Literature',
        'English Literature'

    UNION ALL
    SELECT
        'TY B Arts English Literature',
        'English Literature'

    UNION ALL
    SELECT
        'FY B Science Computer Science',
        'Computer Networks'

    UNION ALL
    SELECT
        'FY B Science Computer Science',
        'Programming in Python'

    UNION ALL
    SELECT
        'FY B Science Computer Science',
        'Database Management Systems'

    UNION ALL
    SELECT
        'SY B Science Computer Science',
        'Computer Networks'

    UNION ALL
    SELECT
        'SY B Science Computer Science',
        'Programming in Python'

    UNION ALL
    SELECT
        'SY B Science Computer Science',
        'Database Management Systems'

    UNION ALL
    SELECT
        'TY B Science Computer Science',
        'Computer Networks'

    UNION ALL
    SELECT
        'TY B Science Computer Science',
        'Programming in Python'

    UNION ALL
    SELECT
        'TY B Science Computer Science',
        'Database Management Systems'

    UNION ALL
    SELECT
        'FY B Commerce Financial Accounting',
        'Financial Accounting'

    UNION ALL
    SELECT
        'SY B Commerce Financial Accounting',
        'Financial Accounting'

    UNION ALL
    SELECT
        'TY B Commerce Financial Accounting',
        'Financial Accounting'
) sub
    ON sub.course_name = c.course_name
WHERE c.institution_category = 'Degree College';


-- ============================================================
-- 5. DEPARTMENT MASTER
-- ============================================================

INSERT INTO department_master
(
    department_name,
    institution_category
)
VALUES

-- SCHOOL
('English', 'School'),
('Hindi', 'School'),
('Science', 'School'),
('Mathematics', 'School'),
('Social Studies', 'School'),

-- JR COLLEGE
('Arts', 'Jr College'),
('Science', 'Jr College'),
('Commerce', 'Jr College'),

-- DEGREE COLLEGE
('Computer Science', 'Degree College'),
('Information Technology', 'Degree College'),
('Data Science', 'Degree College'),
('BMS', 'Degree College');


-- ============================================================
-- 6. DESIGNATION MASTER
-- ============================================================

INSERT INTO designation_master
(
    designation_name,
    institution_category
)
VALUES

-- SCHOOL
('Principal', 'School'),
('Vice Principal', 'School'),
('Head Master', 'School'),
('Head Mistress', 'School'),
('Teacher', 'School'),

-- JR COLLEGE
('Principal', 'Jr College'),
('Vice Principal', 'Jr College'),
('Head Master', 'Jr College'),
('Head Mistress', 'Jr College'),
('Teacher', 'Jr College'),

-- DEGREE COLLEGE
('Principal', 'Degree College'),
('Vice Principal', 'Degree College'),
('Head of Department', 'Degree College'),
('Professor', 'Degree College'),
('Assistant Professor', 'Degree College');


-- ============================================================
-- 7. INSTITUTION STREAM
-- SUNRISE PUBLIC SCHOOL
-- ============================================================

INSERT INTO institution_stream
(
    institution_id,
    stream_id
)
SELECT
    i.institution_id,
    s.stream_id
FROM institution i
JOIN stream_master s
    ON s.stream_name = 'English Medium'
    AND s.institution_category = 'School'
WHERE i.institution_code = 'SPS001';


-- ============================================================
-- BRIGHT JUNIOR COLLEGE STREAMS
-- ============================================================

INSERT INTO institution_stream
(
    institution_id,
    stream_id
)
SELECT
    i.institution_id,
    s.stream_id
FROM institution i
JOIN stream_master s
    ON s.institution_category = 'Jr College'
WHERE i.institution_code = 'BJC001';


-- ============================================================
-- BRIGHT FUTURE COLLEGE STREAM
-- ============================================================

INSERT INTO institution_stream
(
    institution_id,
    stream_id
)
SELECT
    i.institution_id,
    s.stream_id
FROM institution i
JOIN stream_master s
    ON s.stream_name = 'Science'
    AND s.institution_category = 'Degree College'
WHERE i.institution_code = 'BFC001';


-- ============================================================
-- 8. INSTITUTION COURSE
-- SUNRISE PUBLIC SCHOOL
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
    ON c.course_name IN ('IX', 'X')
JOIN stream_master s
    ON s.stream_id = c.stream_id
    AND s.stream_name = 'English Medium'
WHERE i.institution_code = 'SPS001';


-- ============================================================
-- BRIGHT JUNIOR COLLEGE
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
    ON c.course_name IN
    (
        'FY JC Arts',
        'SY JC Arts',
        'FY JC Science',
        'SY JC Science',
        'FY JC Commerce',
        'SY JC Commerce'
    )
WHERE i.institution_code = 'BJC001';


-- ============================================================
-- BRIGHT FUTURE COLLEGE
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
    ON c.course_name IN
    (
        'FY B Science Computer Science',
        'SY B Science Computer Science',
        'TY B Science Computer Science'
    )
WHERE i.institution_code = 'BFC001';


-- ============================================================
-- 9. INSTITUTION SUBJECT
-- SUNRISE PUBLIC SCHOOL
-- ============================================================

INSERT INTO institution_subject
(
    institution_id,
    subject_master_id
)
SELECT
    i.institution_id,
    sm.subject_master_id
FROM institution i
JOIN subject_master sm
    ON sm.institution_category = 'School'
JOIN course_master c
    ON c.course_id = sm.course_id
    AND c.course_name IN ('IX', 'X')
JOIN stream_master s
    ON s.stream_id = c.stream_id
    AND s.stream_name = 'English Medium'
WHERE i.institution_code = 'SPS001';


-- ============================================================
-- BRIGHT JUNIOR COLLEGE SUBJECTS
-- ============================================================

INSERT INTO institution_subject
(
    institution_id,
    subject_master_id
)
SELECT
    i.institution_id,
    sm.subject_master_id
FROM institution i
JOIN subject_master sm
JOIN course_master c
    ON c.course_id = sm.course_id
WHERE i.institution_code = 'BJC001'
AND c.course_name IN
(
    'FY JC Arts',
    'SY JC Arts',
    'FY JC Science',
    'SY JC Science',
    'FY JC Commerce',
    'SY JC Commerce'
);


-- ============================================================
-- BRIGHT FUTURE COLLEGE SUBJECTS
-- ============================================================

INSERT INTO institution_subject
(
    institution_id,
    subject_master_id
)
SELECT
    i.institution_id,
    sm.subject_master_id
FROM institution i
JOIN subject_master sm
JOIN course_master c
    ON c.course_id = sm.course_id
WHERE i.institution_code = 'BFC001'
AND c.course_name IN
(
    'FY B Science Computer Science',
    'SY B Science Computer Science',
    'TY B Science Computer Science'
);


-- ============================================================
-- 10. INSTITUTION DEPARTMENT
-- SUNRISE
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
    ON d.institution_category = 'School'
WHERE i.institution_code = 'SPS001';


-- ============================================================
-- BRIGHT JUNIOR COLLEGE
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
    ON d.institution_category = 'Jr College'
WHERE i.institution_code = 'BJC001';


-- ============================================================
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
    ON d.institution_category = 'Degree College'
WHERE i.institution_code = 'BFC001';


-- ============================================================
-- 11. INSTITUTION DESIGNATIONS
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
WHERE i.institution_code IN
(
    'SPS001',
    'BJC001',
    'BFC001'
);


-- ============================================================
-- 12. ADMIN
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


INSERT INTO admin
(
    institution_id,
    name,
    email,
    password
)
SELECT
    institution_id,
    'Bright Junior Admin',
    'admin@brightjunior.edu',
    'admin123'
FROM institution
WHERE institution_code = 'BJC001';


-- ============================================================
-- 13. TEACHERS
-- SUNRISE
-- ============================================================

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
-- 14. TEACHERS
-- BRIGHT FUTURE COLLEGE
-- ============================================================

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
-- 15. PARENTS
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
-- 16. STANDARDS
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
    ON c.course_name = 'IX'
JOIN stream_master s
    ON s.stream_id = c.stream_id
    AND s.stream_name = 'English Medium'
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
    ON c.course_name = 'X'
JOIN stream_master s
    ON s.stream_id = c.stream_id
    AND s.stream_name = 'English Medium'
WHERE i.institution_code = 'SPS001';


-- ============================================================
-- 17. STANDARDS
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
    ON c.course_name = 'FY B Science Computer Science'
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
    'SY',
    '2026-27'
FROM institution i
JOIN course_master c
    ON c.course_name = 'SY B Science Computer Science'
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
    ON c.course_name = 'TY B Science Computer Science'
WHERE i.institution_code = 'BFC001';


-- ============================================================
-- 18. ACTUAL SUBJECTS
-- SUNRISE - STANDARD X
-- ============================================================

INSERT INTO subject
(
    institution_id,
    standard_id,
    subject_master_id,
    subject_name,
    assessment_type
)
SELECT
    st.institution_id,
    st.standard_id,
    sm.subject_master_id,
    sm.subject_name,
    'Traditional'
FROM standard st
JOIN course_master c
    ON c.course_id = st.course_id
JOIN subject_master sm
    ON sm.course_id = c.course_id
WHERE st.standard_name = 'Standard X'
AND st.institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'SPS001'
);


-- ============================================================
-- 19. ACTUAL SUBJECTS
-- BRIGHT FUTURE COLLEGE - FY
-- ============================================================

INSERT INTO subject
(
    institution_id,
    standard_id,
    subject_master_id,
    subject_name,
    assessment_type
)
SELECT
    st.institution_id,
    st.standard_id,
    sm.subject_master_id,
    sm.subject_name,
    'OBE'
FROM standard st
JOIN course_master c
    ON c.course_id = st.course_id
JOIN subject_master sm
    ON sm.course_id = c.course_id
WHERE st.standard_name = 'FY'
AND st.institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'BFC001'
);


-- ============================================================
-- 20. TEACHER SUBJECT
-- SUNRISE
-- ============================================================

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
    ON s.subject_name = 'Maths'
    AND s.institution_id = t.institution_id
WHERE t.email = 'rahul@sunriseschool.edu';


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
    AND s.institution_id = t.institution_id
WHERE t.email = 'priya@sunriseschool.edu';


-- ============================================================
-- 21. TEACHER SUBJECT
-- BRIGHT FUTURE COLLEGE
-- ============================================================

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
    AND s.institution_id = t.institution_id
WHERE t.email = 'amit@brightfuture.edu';


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
    AND s.institution_id = t.institution_id
WHERE t.email = 'neha@brightfuture.edu';


-- ============================================================
-- 22. CHAPTERS
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
WHERE subject_name = 'Maths'
AND institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'SPS001'
);


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
WHERE subject_name = 'Maths'
AND institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'SPS001'
);


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
WHERE subject_name = 'Science'
AND institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'SPS001'
);


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
WHERE subject_name = 'Computer Networks'
AND institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'BFC001'
);


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
WHERE subject_name = 'Computer Networks'
AND institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'BFC001'
);


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
WHERE subject_name = 'Programming in Python'
AND institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'BFC001'
);


-- ============================================================
-- 23. COURSE OUTCOMES
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
WHERE subject_name = 'Computer Networks'
AND institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'BFC001'
);


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
WHERE subject_name = 'Computer Networks'
AND institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'BFC001'
);


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
WHERE subject_name = 'Computer Networks'
AND institution_id =
(
    SELECT institution_id
    FROM institution
    WHERE institution_code = 'BFC001'
);


-- ============================================================
-- 24. QUESTIONS
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
-- 25. TEST
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
-- 26. TEST QUESTIONS
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
-- 27. TEST ATTEMPT
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
-- 28. STUDENT ANSWERS
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
-- 29. LOGIN HISTORY
-- ============================================================

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
-- 30. NOTIFICATIONS
-- ============================================================

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
-- END OF V3.3 INSERT SCRIPT
-- ============================================================