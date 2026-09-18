-- ============================================================
-- EDUMATE DATABASE VERSION 3.3
-- INSERT / SAMPLE DATA
-- ============================================================

USE edumate_db3_3;

-- ============================================================
-- 1. ADMIN
-- ============================================================

INSERT INTO admin
(
    admin_name,
    email,
    password,
    status
)
VALUES
(
    'System Administrator',
    'admin@edumate.com',
    'admin123',
    'Active'
);


-- ============================================================
-- 2. INSTITUTIONS
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
    website,
    status
)
VALUES
(
    'Sunrise Public School',
    'SPS001',
    'School',
    'OBE',
    'MG Road',
    'Mumbai',
    'Maharashtra',
    '400001',
    'info@sunriseschool.edu',
    '9876543210',
    'https://www.sunriseschool.edu',
    'Active'
),
(
    'Bright Junior College',
    'BJC001',
    'Jr College',
    'Traditional',
    'College Road',
    'Mumbai',
    'Maharashtra',
    '400002',
    'info@brightjunior.edu',
    '9876543211',
    'https://www.brightjunior.edu',
    'Active'
),
(
    'Bright Future College',
    'BFC001',
    'Degree College',
    'OBE',
    'University Road',
    'Mumbai',
    'Maharashtra',
    '400003',
    'info@brightfuture.edu',
    '9876543212',
    'https://www.brightfuture.edu',
    'Active'
);


-- ============================================================
-- 3. STREAM MASTER
-- ============================================================

INSERT INTO stream_master
(
    stream_name,
    institution_category,
    status
)
VALUES

-- SCHOOL STREAMS
(
    'English Medium',
    'School',
    'Active'
),
(
    'Hindi Medium',
    'School',
    'Active'
),
(
    'Marathi Medium',
    'School',
    'Active'
),
(
    'Kannada Medium',
    'School',
    'Active'
),

-- JR COLLEGE STREAMS
(
    'Arts',
    'Jr College',
    'Active'
),
(
    'Science',
    'Jr College',
    'Active'
),
(
    'Commerce',
    'Jr College',
    'Active'
),

-- DEGREE COLLEGE STREAMS
(
    'Arts',
    'Degree College',
    'Active'
),
(
    'Science',
    'Degree College',
    'Active'
),
(
    'Commerce',
    'Degree College',
    'Active'
);


-- ============================================================
-- 4. COURSE MASTER
--
-- IMPORTANT:
-- School courses I-X are inserted ONLY ONCE.
-- ============================================================

INSERT INTO course_master
(
    course_name,
    institution_category,
    status
)
VALUES

-- SCHOOL COURSES
('I',   'School', 'Active'),
('II',  'School', 'Active'),
('III', 'School', 'Active'),
('IV',  'School', 'Active'),
('V',   'School', 'Active'),
('VI',  'School', 'Active'),
('VII', 'School', 'Active'),
('VIII','School', 'Active'),
('IX',  'School', 'Active'),
('X',   'School', 'Active'),

-- JR COLLEGE COURSES
('FY JC Arts',     'Jr College', 'Active'),
('SY JC Arts',     'Jr College', 'Active'),
('FY JC Science',  'Jr College', 'Active'),
('SY JC Science',  'Jr College', 'Active'),
('FY JC Commerce', 'Jr College', 'Active'),
('SY JC Commerce', 'Jr College', 'Active'),

-- DEGREE COLLEGE COURSES
('FY B Arts English Literature', 'Degree College', 'Active'),
('SY B Arts English Literature', 'Degree College', 'Active'),
('TY B Arts English Literature', 'Degree College', 'Active'),

('FY B Science Computer Science', 'Degree College', 'Active'),
('SY B Science Computer Science', 'Degree College', 'Active'),
('TY B Science Computer Science', 'Degree College', 'Active'),

('FY B Commerce Financial Accounting', 'Degree College', 'Active'),
('SY B Commerce Financial Accounting', 'Degree College', 'Active'),
('TY B Commerce Financial Accounting', 'Degree College', 'Active');


-- ============================================================
-- 5. COURSE - STREAM MAPPING
-- ============================================================

-- ------------------------------------------------------------
-- SCHOOL COURSES
-- Every school course can be offered in every school medium.
-- ------------------------------------------------------------

INSERT INTO course_stream
(
    course_id,
    stream_id
)
SELECT
    c.course_id,
    s.stream_id
FROM course_master c
CROSS JOIN stream_master s
WHERE c.institution_category = 'School'
  AND s.institution_category = 'School';


-- ------------------------------------------------------------
-- JR COLLEGE COURSES
-- ------------------------------------------------------------

INSERT INTO course_stream
(
    course_id,
    stream_id
)
SELECT
    c.course_id,
    s.stream_id
FROM course_master c
JOIN stream_master s
    ON s.institution_category = 'Jr College'
   AND (
        (c.course_name IN ('FY JC Arts', 'SY JC Arts')
         AND s.stream_name = 'Arts')

        OR

        (c.course_name IN ('FY JC Science', 'SY JC Science')
         AND s.stream_name = 'Science')

        OR

        (c.course_name IN ('FY JC Commerce', 'SY JC Commerce')
         AND s.stream_name = 'Commerce')
   )
WHERE c.institution_category = 'Jr College';


-- ------------------------------------------------------------
-- DEGREE COLLEGE COURSES
-- ------------------------------------------------------------

INSERT INTO course_stream
(
    course_id,
    stream_id
)
SELECT
    c.course_id,
    s.stream_id
FROM course_master c
JOIN stream_master s
    ON s.institution_category = 'Degree College'
   AND (
        (
            c.course_name IN
            (
                'FY B Arts English Literature',
                'SY B Arts English Literature',
                'TY B Arts English Literature'
            )
            AND s.stream_name = 'Arts'
        )

        OR

        (
            c.course_name IN
            (
                'FY B Science Computer Science',
                'SY B Science Computer Science',
                'TY B Science Computer Science'
            )
            AND s.stream_name = 'Science'
        )

        OR

        (
            c.course_name IN
            (
                'FY B Commerce Financial Accounting',
                'SY B Commerce Financial Accounting',
                'TY B Commerce Financial Accounting'
            )
            AND s.stream_name = 'Commerce'
        )
   )
WHERE c.institution_category = 'Degree College';

-- ============================================================
-- 5. COURSE ACADEMIC YEAR
--
-- Maps each course to its academic year/level.
--
-- IMPORTANT:
-- Academic year here means the academic level of the course,
-- NOT the calendar academic year such as 2026-27.
--
-- School:
--     Not Applicable
--
-- Jr College:
--     FY
--     SY
--
-- Degree College:
--     FY
--     SY
--     TY
--     4th Year
--
-- Academic year is NOT stored in course_master.
-- It is stored separately in course_academic_year.
-- ============================================================

-- ============================================================
-- SCHOOL COURSES
-- ============================================================
-- School courses from I to X do not have FY/SY/TY etc.
-- Therefore, their academic year is "Not Applicable".
-- ============================================================

INSERT INTO course_academic_year
(
    course_id,
    academic_year,
    status
)
SELECT
    course_id,
    'Not Applicable',
    'Active'
FROM course_master
WHERE institution_category = 'School'
  AND course_name IN
  (
      'I',
      'II',
      'III',
      'IV',
      'V',
      'VI',
      'VII',
      'VIII',
      'IX',
      'X'
  );


-- ============================================================
-- JR COLLEGE COURSES
-- ============================================================
-- FY JC courses → FY
-- SY JC courses → SY
-- ============================================================

INSERT INTO course_academic_year
(
    course_id,
    academic_year,
    status
)
SELECT
    course_id,
    'FY',
    'Active'
FROM course_master
WHERE institution_category = 'Jr College'
  AND course_name IN
  (
      'FY JC Arts',
      'FY JC Science',
      'FY JC Commerce'
  );


INSERT INTO course_academic_year
(
    course_id,
    academic_year,
    status
)
SELECT
    course_id,
    'SY',
    'Active'
FROM course_master
WHERE institution_category = 'Jr College'
  AND course_name IN
  (
      'SY JC Arts',
      'SY JC Science',
      'SY JC Commerce'
  );


-- ============================================================
-- DEGREE COLLEGE COURSES
-- ============================================================
-- FY Degree College courses → FY
-- SY Degree College courses → SY
-- TY Degree College courses → TY
-- 4th Year Degree College courses → 4th Year
-- ============================================================


-- ------------------------------------------------------------
-- FY DEGREE COLLEGE
-- ------------------------------------------------------------

INSERT INTO course_academic_year
(
    course_id,
    academic_year,
    status
)
SELECT
    course_id,
    'FY',
    'Active'
FROM course_master
WHERE institution_category = 'Degree College'
  AND course_name IN
  (
      'FY B Arts English Literature',
      'FY B Science Computer Science',
      'FY B Commerce Financial Accounting'
  );


-- ------------------------------------------------------------
-- SY DEGREE COLLEGE
-- ------------------------------------------------------------

INSERT INTO course_academic_year
(
    course_id,
    academic_year,
    status
)
SELECT
    course_id,
    'SY',
    'Active'
FROM course_master
WHERE institution_category = 'Degree College'
  AND course_name IN
  (
      'SY B Arts English Literature',
      'SY B Science Computer Science',
      'SY B Commerce Financial Accounting'
  );


-- ------------------------------------------------------------
-- TY DEGREE COLLEGE
-- ------------------------------------------------------------

INSERT INTO course_academic_year
(
    course_id,
    academic_year,
    status
)
SELECT
    course_id,
    'TY',
    'Active'
FROM course_master
WHERE institution_category = 'Degree College'
  AND course_name IN
  (
      'TY B Arts English Literature',
      'TY B Science Computer Science',
      'TY B Commerce Financial Accounting'
  );


-- ------------------------------------------------------------
-- 4TH YEAR DEGREE COLLEGE
-- ------------------------------------------------------------
-- This will insert mappings only if 4th Year courses exist
-- in course_master.
--
-- Example course names can be added later.
-- ------------------------------------------------------------

INSERT INTO course_academic_year
(
    course_id,
    academic_year,
    status
)
SELECT
    course_id,
    '4th Year',
    'Active'
FROM course_master
WHERE institution_category = 'Degree College'
  AND course_name LIKE '4th Year%';

-- ============================================================
-- SEMESTER MASTER DATA
-- ============================================================

INSERT INTO semester_master
(
    academic_year,
    semester_number,
    semester_name,
    institution_category,
    status
)
VALUES

-- ============================================================
-- SCHOOL
-- ============================================================
-- Schools do not use semesters in EduMate.

(
    'Not Applicable',
    0,
    'Not Applicable',
    'School',
    'Active'
),


-- ============================================================
-- JR COLLEGE
-- ============================================================

-- FY JC
(
    'FY',
    1,
    'Semester 1',
    'Jr College',
    'Active'
),
(
    'FY',
    2,
    'Semester 2',
    'Jr College',
    'Active'
),

-- SY JC
(
    'SY',
    3,
    'Semester 3',
    'Jr College',
    'Active'
),
(
    'SY',
    4,
    'Semester 4',
    'Jr College',
    'Active'
),


-- ============================================================
-- DEGREE COLLEGE
-- ============================================================

-- FY
(
    'FY',
    1,
    'Semester 1',
    'Degree College',
    'Active'
),
(
    'FY',
    2,
    'Semester 2',
    'Degree College',
    'Active'
),

-- SY
(
    'SY',
    3,
    'Semester 3',
    'Degree College',
    'Active'
),
(
    'SY',
    4,
    'Semester 4',
    'Degree College',
    'Active'
),

-- TY
(
    'TY',
    5,
    'Semester 5',
    'Degree College',
    'Active'
),
(
    'TY',
    6,
    'Semester 6',
    'Degree College',
    'Active'
),

-- 4th Year
(
    '4th Year',
    7,
    'Semester 7',
    'Degree College',
    'Active'
),
(
    '4th Year',
    8,
    'Semester 8',
    'Degree College',
    'Active'
);

-- ============================================================
-- 6. SUBJECT MASTER
-- ============================================================

-- ------------------------------------------------------------
-- SCHOOL SUBJECTS
-- ------------------------------------------------------------

INSERT INTO subject_master
(
    subject_name,
    course_id,
    institution_category,
    status
)
SELECT
    sub.subject_name,
    c.course_id,
    'School',
    'Active'
FROM course_master c
CROSS JOIN
(
    SELECT 'English' AS subject_name
    UNION ALL
    SELECT 'Mathematics'
    UNION ALL
    SELECT 'Science'
    UNION ALL
    SELECT 'Social Science'
    UNION ALL
    SELECT 'Hindi'
) sub
WHERE c.institution_category = 'School';


-- ------------------------------------------------------------
-- JR COLLEGE SUBJECTS
-- ------------------------------------------------------------

INSERT INTO subject_master
(
    subject_name,
    course_id,
    institution_category,
    status
)
SELECT
    x.subject_name,
    c.course_id,
    'Jr College',
    'Active'
FROM course_master c
JOIN
(
    SELECT
        'FY JC Arts' AS course_name,
        'English' AS subject_name
    UNION ALL
    SELECT 'FY JC Arts', 'History'
    UNION ALL
    SELECT 'FY JC Arts', 'Political Science'
    UNION ALL
    SELECT 'FY JC Arts', 'Economics'

    UNION ALL
    SELECT 'SY JC Arts', 'English'
    UNION ALL
    SELECT 'SY JC Arts', 'History'
    UNION ALL
    SELECT 'SY JC Arts', 'Political Science'
    UNION ALL
    SELECT 'SY JC Arts', 'Economics'

    UNION ALL
    SELECT 'FY JC Science', 'English'
    UNION ALL
    SELECT 'FY JC Science', 'Physics'
    UNION ALL
    SELECT 'FY JC Science', 'Chemistry'
    UNION ALL
    SELECT 'FY JC Science', 'Mathematics'

    UNION ALL
    SELECT 'SY JC Science', 'English'
    UNION ALL
    SELECT 'SY JC Science', 'Physics'
    UNION ALL
    SELECT 'SY JC Science', 'Chemistry'
    UNION ALL
    SELECT 'SY JC Science', 'Mathematics'

    UNION ALL
    SELECT 'FY JC Commerce', 'English'
    UNION ALL
    SELECT 'FY JC Commerce', 'Economics'
    UNION ALL
    SELECT 'FY JC Commerce', 'Accountancy'
    UNION ALL
    SELECT 'FY JC Commerce', 'Organisation of Commerce'

    UNION ALL
    SELECT 'SY JC Commerce', 'English'
    UNION ALL
    SELECT 'SY JC Commerce', 'Economics'
    UNION ALL
    SELECT 'SY JC Commerce', 'Accountancy'
    UNION ALL
    SELECT 'SY JC Commerce', 'Organisation of Commerce'
) x
    ON x.course_name = c.course_name
WHERE c.institution_category = 'Jr College';


-- ------------------------------------------------------------
-- DEGREE COLLEGE SUBJECTS
-- ------------------------------------------------------------

INSERT INTO subject_master
(
    subject_name,
    course_id,
    institution_category,
    status
)
SELECT
    x.subject_name,
    c.course_id,
    'Degree College',
    'Active'
FROM course_master c
JOIN
(
    SELECT
        'FY B Arts English Literature' AS course_name,
        'English Literature' AS subject_name
    UNION ALL
    SELECT 'FY B Arts English Literature', 'History'
    UNION ALL
    SELECT 'FY B Arts English Literature', 'Political Science'

    UNION ALL
    SELECT 'SY B Arts English Literature', 'English Literature'
    UNION ALL
    SELECT 'SY B Arts English Literature', 'History'
    UNION ALL
    SELECT 'SY B Arts English Literature', 'Political Science'

    UNION ALL
    SELECT 'TY B Arts English Literature', 'English Literature'
    UNION ALL
    SELECT 'TY B Arts English Literature', 'History'
    UNION ALL
    SELECT 'TY B Arts English Literature', 'Political Science'

    UNION ALL
    SELECT 'FY B Science Computer Science', 'Computer Science'
    UNION ALL
    SELECT 'FY B Science Computer Science', 'Mathematics'
    UNION ALL
    SELECT 'FY B Science Computer Science', 'Physics'

    UNION ALL
    SELECT 'SY B Science Computer Science', 'Computer Science'
    UNION ALL
    SELECT 'SY B Science Computer Science', 'Mathematics'
    UNION ALL
    SELECT 'SY B Science Computer Science', 'Physics'

    UNION ALL
    SELECT 'TY B Science Computer Science', 'Computer Science'
    UNION ALL
    SELECT 'TY B Science Computer Science', 'Mathematics'
    UNION ALL
    SELECT 'TY B Science Computer Science', 'Physics'

    UNION ALL
    SELECT 'FY B Commerce Financial Accounting', 'Financial Accounting'
    UNION ALL
    SELECT 'FY B Commerce Financial Accounting', 'Economics'
    UNION ALL
    SELECT 'FY B Commerce Financial Accounting', 'Business Law'

    UNION ALL
    SELECT 'SY B Commerce Financial Accounting', 'Financial Accounting'
    UNION ALL
    SELECT 'SY B Commerce Financial Accounting', 'Economics'
    UNION ALL
    SELECT 'SY B Commerce Financial Accounting', 'Business Law'

    UNION ALL
    SELECT 'TY B Commerce Financial Accounting', 'Financial Accounting'
    UNION ALL
    SELECT 'TY B Commerce Financial Accounting', 'Economics'
    UNION ALL
    SELECT 'TY B Commerce Financial Accounting', 'Business Law'
) x
    ON x.course_name = c.course_name
WHERE c.institution_category = 'Degree College';


-- ============================================================
-- 7. DEPARTMENT MASTER
-- ============================================================

INSERT INTO department_master
(
    department_name,
    institution_category,
    status
)
VALUES

-- SCHOOL
('Primary Education', 'School', 'Active'),
('Secondary Education', 'School', 'Active'),

-- JR COLLEGE
('Arts', 'Jr College', 'Active'),
('Science', 'Jr College', 'Active'),
('Commerce', 'Jr College', 'Active'),

-- DEGREE COLLEGE
('English', 'Degree College', 'Active'),
('Computer Science', 'Degree College', 'Active'),
('Commerce', 'Degree College', 'Active');


-- ============================================================
-- 8. DESIGNATION MASTER
-- ============================================================

INSERT INTO designation_master
(
    designation_name,
    institution_category,
    status
)
VALUES

-- SCHOOL
('Principal', 'School', 'Active'),
('Vice Principal', 'School', 'Active'),
('Teacher', 'School', 'Active'),
('Head Teacher', 'School', 'Active'),

-- JR COLLEGE
('Principal', 'Jr College', 'Active'),
('Vice Principal', 'Jr College', 'Active'),
('Lecturer', 'Jr College', 'Active'),
('Head of Department', 'Jr College', 'Active'),

-- DEGREE COLLEGE
('Principal', 'Degree College', 'Active'),
('Vice Principal', 'Degree College', 'Active'),
('Assistant Professor', 'Degree College', 'Active'),
('Associate Professor', 'Degree College', 'Active'),
('Professor', 'Degree College', 'Active'),
('Head of Department', 'Degree College', 'Active');


-- ============================================================
-- 9. INSTITUTION - STREAM MAPPING
-- ============================================================

-- ------------------------------------------------------------
-- SUNRISE PUBLIC SCHOOL
-- English Medium only
-- ------------------------------------------------------------

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


-- ------------------------------------------------------------
-- BRIGHT JUNIOR COLLEGE
-- Arts + Science + Commerce
-- ------------------------------------------------------------

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


-- ------------------------------------------------------------
-- BRIGHT FUTURE COLLEGE
-- Science
-- ------------------------------------------------------------

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
-- 10. INSTITUTION - COURSE MAPPING
-- ============================================================

-- ------------------------------------------------------------
-- SUNRISE PUBLIC SCHOOL
-- Courses IX and X
-- ------------------------------------------------------------

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
   AND c.institution_category = 'School'
WHERE i.institution_code = 'SPS001';


-- ------------------------------------------------------------
-- BRIGHT JUNIOR COLLEGE
-- All six JC courses
-- ------------------------------------------------------------

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
    ON c.institution_category = 'Jr College'
WHERE i.institution_code = 'BJC001';


-- ------------------------------------------------------------
-- BRIGHT FUTURE COLLEGE
-- Science degree courses
-- ------------------------------------------------------------

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
   AND c.institution_category = 'Degree College'
WHERE i.institution_code = 'BFC001';


-- ============================================================
-- 11. INSTITUTION - SUBJECT MAPPING
-- ============================================================

-- ------------------------------------------------------------
-- SUNRISE PUBLIC SCHOOL
-- Subjects for IX and X
-- ------------------------------------------------------------

INSERT INTO institution_subject
(
    institution_id,
    subject_master_id
)
SELECT DISTINCT
    i.institution_id,
    sm.subject_master_id
FROM institution i
JOIN subject_master sm
    ON sm.institution_category = 'School'
JOIN course_master c
    ON c.course_id = sm.course_id
WHERE i.institution_code = 'SPS001'
  AND c.course_name IN ('IX', 'X');


-- ------------------------------------------------------------
-- BRIGHT JUNIOR COLLEGE
-- All subjects of all JC courses
-- ------------------------------------------------------------

INSERT INTO institution_subject
(
    institution_id,
    subject_master_id
)
SELECT DISTINCT
    i.institution_id,
    sm.subject_master_id
FROM institution i
JOIN subject_master sm
    ON sm.institution_category = 'Jr College'
JOIN course_master c
    ON c.course_id = sm.course_id
WHERE i.institution_code = 'BJC001';


-- ------------------------------------------------------------
-- BRIGHT FUTURE COLLEGE
-- Computer Science degree subjects
-- ------------------------------------------------------------

INSERT INTO institution_subject
(
    institution_id,
    subject_master_id
)
SELECT DISTINCT
    i.institution_id,
    sm.subject_master_id
FROM institution i
JOIN subject_master sm
    ON sm.institution_category = 'Degree College'
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
-- 12. INSTITUTION - DEPARTMENT MAPPING
-- ============================================================

-- SUNRISE PUBLIC SCHOOL

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


-- BRIGHT JUNIOR COLLEGE

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


-- BRIGHT FUTURE COLLEGE

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
-- 13. INSTITUTION - DESIGNATION MAPPING
-- ============================================================

-- SUNRISE PUBLIC SCHOOL

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
    ON d.institution_category = 'School'
WHERE i.institution_code = 'SPS001';


-- BRIGHT JUNIOR COLLEGE

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
    ON d.institution_category = 'Jr College'
WHERE i.institution_code = 'BJC001';


-- BRIGHT FUTURE COLLEGE

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
    ON d.institution_category = 'Degree College'
WHERE i.institution_code = 'BFC001';


-- ============================================================
-- 14. STANDARD DATA
-- ============================================================

-- ------------------------------------------------------------
-- SUNRISE PUBLIC SCHOOL
-- ------------------------------------------------------------

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
    c.course_name,
    '2026-27'
FROM institution i
JOIN course_master c
    ON c.course_name IN ('IX', 'X')
   AND c.institution_category = 'School'
WHERE i.institution_code = 'SPS001';


-- ------------------------------------------------------------
-- BRIGHT JUNIOR COLLEGE
-- ------------------------------------------------------------

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
    c.course_name,
    '2026-27'
FROM institution i
JOIN course_master c
    ON c.institution_category = 'Jr College'
WHERE i.institution_code = 'BJC001';


-- ------------------------------------------------------------
-- BRIGHT FUTURE COLLEGE
-- ------------------------------------------------------------

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
    c.course_name,
    '2026-27'
FROM institution i
JOIN course_master c
    ON c.course_name IN
    (
        'FY B Science Computer Science',
        'SY B Science Computer Science',
        'TY B Science Computer Science'
    )
   AND c.institution_category = 'Degree College'
WHERE i.institution_code = 'BFC001';


-- ============================================================
-- 15. SUBJECT DATA
-- ============================================================

INSERT INTO subject
(
    institution_id,
    standard_id,
    subject_master_id,
    subject_name,
    assessment_type,
    status
)
SELECT
    st.institution_id,
    st.standard_id,
    sm.subject_master_id,
    sm.subject_name,
    i.institution_type,
    'Active'
FROM standard st
JOIN institution i
    ON i.institution_id = st.institution_id
JOIN subject_master sm
    ON sm.course_id = st.course_id
WHERE sm.institution_category = i.institution_category;


-- ============================================================
-- 16. TEACHERS
-- ============================================================

INSERT INTO teacher
(
    institution_id,
    department_id,
    designation_id,
    teacher_name,
    email,
    phone,
    password,
    status
)
SELECT
    i.institution_id,
    d.department_id,
    dg.designation_id,
    'Anita Sharma',
    'anita@sunriseschool.edu',
    '9876500001',
    'teacher123',
    'Active'
FROM institution i
JOIN department_master d
    ON d.department_name = 'Secondary Education'
   AND d.institution_category = 'School'
JOIN designation_master dg
    ON dg.designation_name = 'Teacher'
   AND dg.institution_category = 'School'
WHERE i.institution_code = 'SPS001';


INSERT INTO teacher
(
    institution_id,
    department_id,
    designation_id,
    teacher_name,
    email,
    phone,
    password,
    status
)
SELECT
    i.institution_id,
    d.department_id,
    dg.designation_id,
    'Rajesh Patil',
    'rajesh@brightjunior.edu',
    '9876500002',
    'teacher123',
    'Active'
FROM institution i
JOIN department_master d
    ON d.department_name = 'Science'
   AND d.institution_category = 'Jr College'
JOIN designation_master dg
    ON dg.designation_name = 'Lecturer'
   AND dg.institution_category = 'Jr College'
WHERE i.institution_code = 'BJC001';


INSERT INTO teacher
(
    institution_id,
    department_id,
    designation_id,
    teacher_name,
    email,
    phone,
    password,
    status
)
SELECT
    i.institution_id,
    d.department_id,
    dg.designation_id,
    'Meera Kulkarni',
    'meera@brightfuture.edu',
    '9876500003',
    'teacher123',
    'Active'
FROM institution i
JOIN department_master d
    ON d.department_name = 'Computer Science'
   AND d.institution_category = 'Degree College'
JOIN designation_master dg
    ON dg.designation_name = 'Assistant Professor'
   AND dg.institution_category = 'Degree College'
WHERE i.institution_code = 'BFC001';


-- ============================================================
-- 17. PARENTS
-- ============================================================
TRUNCATE TABLE parent;

INSERT INTO parent
    (student_id, parent_name, email, phone, password, status)
VALUES
    (1, 'Suresh Sharma', 'suresh.parent@sunriseschool.edu', '9876600001', 'parent123', 'Active'),
    (2, 'Meena Patil', 'meena.parent@brightfuture.edu', '9876600002', 'parent123', 'Active'),
    (3, 'Rajesh Mehta', 'rajesh.parent@sunriseschool.edu', '9876600003', 'parent123', 'Active');

-- ============================================================
-- 18. STUDENTS
-- IMPORTANT:
-- Student records are included so test attempts and answers
-- can reference valid students.
-- ============================================================

INSERT INTO student
(
    institution_id,
    standard_id,
    parent_id,
    student_name,
    email,
    phone,
    password,
    status
)
SELECT
    i.institution_id,
    st.standard_id,
    p.parent_id,
    'Rohan Sharma',
    'rohan@sunriseschool.edu',
    '9876700001',
    'student123',
    'Active'
FROM institution i
JOIN standard st
    ON st.institution_id = i.institution_id
   AND st.standard_name = 'IX'
JOIN parent p
    ON p.institution_id = i.institution_id
   AND p.email = 'rohan.parent@sunriseschool.edu'
WHERE i.institution_code = 'SPS001';

-- ============================================================
-- NEW STANDARD X STUDENT - SUNRISE PUBLIC SCHOOL
-- ============================================================

INSERT INTO student
(
    institution_id,
    standard_id,
    parent_id,
    student_name,
    email,
    phone,
    password,
    status
)
SELECT
    i.institution_id,
    st.standard_id,
    p.parent_id,
    'Neha Mehta',
    'neha@sunriseschool.edu',
    '9876700003',
    'student123',
    'Active'
FROM institution i
JOIN standard st
    ON st.institution_id = i.institution_id
   AND st.standard_name = 'X'
   AND st.academic_year = '2026-27'
JOIN parent p
    ON p.institution_id = i.institution_id
   AND p.email = 'neha.parent@sunriseschool.edu'
WHERE i.institution_code = 'SPS001';


INSERT INTO student
(
    institution_id,
    standard_id,
    parent_id,
    student_name,
    email,
    phone,
    password,
    status
)
SELECT
    i.institution_id,
    st.standard_id,
    p.parent_id,
    'Aarav Patil',
    'aarav@brightfuture.edu',
    '9876700002',
    'student123',
    'Active'
FROM institution i
JOIN standard st
    ON st.institution_id = i.institution_id
   AND st.standard_name = 'FY B Science Computer Science'
JOIN parent p
    ON p.institution_id = i.institution_id
   AND p.email = 'aarav.parent@brightfuture.edu'
WHERE i.institution_code = 'BFC001';


-- ============================================================
-- 19. TEACHER - SUBJECT MAPPING
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
    ON s.institution_id = t.institution_id
JOIN standard st
    ON st.standard_id = s.standard_id
WHERE t.email = 'anita@sunriseschool.edu'
  AND st.standard_name IN ('IX', 'X');


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
    ON s.institution_id = t.institution_id
JOIN standard st
    ON st.standard_id = s.standard_id
WHERE t.email = 'rajesh@brightjunior.edu'
  AND st.standard_name IN
  (
      'FY JC Science',
      'SY JC Science'
  );


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
    ON s.institution_id = t.institution_id
JOIN standard st
    ON st.standard_id = s.standard_id
WHERE t.email = 'meera@brightfuture.edu'
  AND st.standard_name IN
  (
      'FY B Science Computer Science',
      'SY B Science Computer Science',
      'TY B Science Computer Science'
  );

-- ============================================================
-- 20. CHAPTERS
-- 5 CHAPTERS FOR EVERY ACTIVE SUBJECT
-- ============================================================

INSERT INTO chapter
(
    subject_id,
    chapter_name,
    chapter_number,
    status
)
SELECT
    s.subject_id,

    CASE numbers.chapter_number

        WHEN 1 THEN CONCAT(
            'Introduction to ',
            sm.subject_name
        )

        WHEN 2 THEN CONCAT(
            'Fundamentals of ',
            sm.subject_name
        )

        WHEN 3 THEN CONCAT(
            'Core Concepts of ',
            sm.subject_name
        )

        WHEN 4 THEN CONCAT(
            'Applications of ',
            sm.subject_name
        )

        WHEN 5 THEN CONCAT(
            'Advanced Topics in ',
            sm.subject_name
        )

    END AS chapter_name,

    numbers.chapter_number,

    'Active'

FROM subject s

JOIN subject_master sm
    ON sm.subject_master_id = s.subject_master_id

JOIN
(
    SELECT 1 AS chapter_number
    UNION ALL
    SELECT 2
    UNION ALL
    SELECT 3
    UNION ALL
    SELECT 4
    UNION ALL
    SELECT 5
) numbers

WHERE s.status = 'Active';


-- ============================================================
-- 21. COURSE OUTCOMES
-- ONLY FOR OBE SUBJECTS
-- ============================================================

INSERT INTO course_outcome
(
    subject_id,
    co_code,
    co_description
)
SELECT
    s.subject_id,
    CONCAT('CO', numbers.co_number),

    CASE numbers.co_number

        WHEN 1 THEN CONCAT(
            'Understand the fundamental concepts of ',
            sm.subject_name,
            '.'
        )

        WHEN 2 THEN CONCAT(
            'Explain the basic principles and terminology of ',
            sm.subject_name,
            '.'
        )

        WHEN 3 THEN CONCAT(
            'Apply the concepts of ',
            sm.subject_name,
            ' to appropriate examples and problems.'
        )

        WHEN 4 THEN CONCAT(
            'Analyze and interpret concepts related to ',
            sm.subject_name,
            '.'
        )

        WHEN 5 THEN CONCAT(
            'Demonstrate knowledge and application of ',
            sm.subject_name,
            ' concepts.'
        )

    END AS co_description

FROM subject s

JOIN subject_master sm
    ON sm.subject_master_id = s.subject_master_id

JOIN
(
    SELECT 1 AS co_number
    UNION ALL
    SELECT 2
    UNION ALL
    SELECT 3
    UNION ALL
    SELECT 4
    UNION ALL
    SELECT 5
) numbers

WHERE s.status = 'Active'
  AND s.assessment_type = 'OBE';


-- ============================================================
-- 22. QUESTIONS
-- 12 QUESTIONS FOR EVERY ACTIVE SUBJECT
-- ============================================================

INSERT INTO question
(
    subject_id,
    chapter_id,
    co_id,
    question_text,
    option_a,
    option_b,
    option_c,
    option_d,
    correct_answer,
    difficulty,
    marks,
    question_type,
    is_pyq,
    status
)

SELECT

    s.subject_id,

    ch.chapter_id,

    co.co_id,

    qt.question_text,

    qt.option_a,
    qt.option_b,
    qt.option_c,
    qt.option_d,

    qt.correct_answer,

    qt.difficulty,

    1,

    'MCQ',

    FALSE,

    'Active'

FROM subject s

JOIN subject_master sm
    ON sm.subject_master_id = s.subject_master_id

JOIN
(
    -- ========================================================
    -- QUESTION 1
    -- ========================================================

    SELECT
        1 AS question_number,
        1 AS chapter_number,
        'Easy' AS difficulty,
        'A' AS correct_answer,
        'What is the primary purpose of studying %s?' AS question_text,
        'To understand the fundamental concepts of %s' AS option_a,
        'To repair computer hardware' AS option_b,
        'To design electrical circuits' AS option_c,
        'To operate a printer' AS option_d

    UNION ALL

    -- ========================================================
    -- QUESTION 2
    -- ========================================================

    SELECT
        2,
        1,
        'Easy',
        'A',
        'Which of the following is most closely related to %s?',
        '%s concepts and applications',
        'Web browsing only',
        'Computer assembly only',
        'Network cabling only'

    UNION ALL

    -- ========================================================
    -- QUESTION 3
    -- ========================================================

    SELECT
        3,
        1,
        'Medium',
        'A',
        'Which statement best describes %s?',
        'It deals with concepts related to %s',
        'It is only about computer hardware',
        'It is only about internet services',
        'It is only about office software'

    UNION ALL

    -- ========================================================
    -- QUESTION 4
    -- ========================================================

    SELECT
        4,
        2,
        'Easy',
        'A',
        'Which skill is useful when learning %s?',
        'Understanding and applying its concepts',
        'Replacing a computer processor',
        'Installing network cables',
        'Repairing a printer'

    UNION ALL

    -- ========================================================
    -- QUESTION 5
    -- ========================================================

    SELECT
        5,
        2,
        'Medium',
        'A',
        'Which of the following would be an appropriate topic in %s?',
        'A concept directly related to %s',
        'Unrelated hardware repair',
        'Electrical wiring',
        'Printer maintenance'

    UNION ALL

    -- ========================================================
    -- QUESTION 6
    -- ========================================================

    SELECT
        6,
        2,
        'Hard',
        'A',
        'Why is %s important?',
        'It helps develop knowledge and understanding in its field',
        'It is used only to switch on computers',
        'It replaces all other subjects',
        'It is required only for gaming'

    UNION ALL

    -- ========================================================
    -- QUESTION 7
    -- ========================================================

    SELECT
        7,
        3,
        'Easy',
        'A',
        'Which option represents a basic concept of %s?',
        'A fundamental idea related to %s',
        'A random computer command',
        'A type of printer',
        'A network cable'

    UNION ALL

    -- ========================================================
    -- QUESTION 8
    -- ========================================================

    SELECT
        8,
        3,
        'Medium',
        'A',
        'What should a student do when studying %s?',
        'Understand concepts and apply them correctly',
        'Memorize unrelated hardware parts',
        'Avoid examples',
        'Ignore applications'

    UNION ALL

    -- ========================================================
    -- QUESTION 9
    -- ========================================================

    SELECT
        9,
        4,
        'Medium',
        'A',
        'Which statement about %s is correct?',
        'It has concepts that can be learned and applied',
        'It is unrelated to education',
        'It only concerns computer networks',
        'It only concerns operating systems'

    UNION ALL

    -- ========================================================
    -- QUESTION 10
    -- ========================================================

    SELECT
        10,
        4,
        'Hard',
        'A',
        'An assessment on %s would most likely test:',
        'Knowledge and application of %s concepts',
        'Computer power supply repair',
        'Printer installation',
        'Keyboard cleaning'

    UNION ALL

    -- ========================================================
    -- QUESTION 11
    -- ========================================================

    SELECT
        11,
        5,
        'Medium',
        'A',
        'Which approach is suitable for learning %s?',
        'Study its concepts, examples, and applications',
        'Study only computer hardware',
        'Study only network cables',
        'Study only typing speed'

    UNION ALL

    -- ========================================================
    -- QUESTION 12
    -- ========================================================

    SELECT
        12,
        5,
        'Hard',
        'A',
        'Which of the following is a valid learning outcome for %s?',
        'Explain and apply basic %s concepts',
        'Repair a computer monitor',
        'Configure a printer',
        'Replace a keyboard'

) qt

JOIN chapter ch
    ON ch.subject_id = s.subject_id
   AND ch.chapter_number = qt.chapter_number

LEFT JOIN course_outcome co
    ON co.subject_id = s.subject_id
   AND co.co_code = CONCAT(
        'CO',
        qt.chapter_number
   )

WHERE s.status = 'Active';


-- ============================================================
-- IMPORTANT:
-- REPLACE THE %s PLACEHOLDERS WITH THE SUBJECT NAME
-- ============================================================

UPDATE question q

JOIN subject s
    ON s.subject_id = q.subject_id

JOIN subject_master sm
    ON sm.subject_master_id = s.subject_master_id

SET

    q.question_text =
        REPLACE(
            q.question_text,
            '%s',
            sm.subject_name
        ),

    q.option_a =
        REPLACE(
            q.option_a,
            '%s',
            sm.subject_name
        ),

    q.option_b =
        REPLACE(
            q.option_b,
            '%s',
            sm.subject_name
        ),

    q.option_c =
        REPLACE(
            q.option_c,
            '%s',
            sm.subject_name
        ),

    q.option_d =
        REPLACE(
            q.option_d,
            '%s',
            sm.subject_name
        );


-- ============================================================
-- VERIFICATION
-- ============================================================

SELECT
    s.subject_id,
    sm.subject_name,
    st.standard_name,
    s.assessment_type,
    COUNT(q.question_id) AS question_count

FROM subject s

JOIN subject_master sm
    ON sm.subject_master_id = s.subject_master_id

JOIN standard st
    ON st.standard_id = s.standard_id

LEFT JOIN question q
    ON q.subject_id = s.subject_id

WHERE s.status = 'Active'

GROUP BY
    s.subject_id,
    sm.subject_name,
    st.standard_name,
    s.assessment_type

ORDER BY
    st.standard_name,
    sm.subject_name;

-- ============================================================
-- 23. TEST
-- ============================================================

INSERT INTO test
(
    teacher_id,
    subject_id,
    test_name,
    description,
    total_marks,
    duration_minutes,
    start_datetime,
    end_datetime,
    status
)
SELECT
    t.teacher_id,
    s.subject_id,
    'Unit Test 1',
    'Sample assessment test',
    10,
    30,
    '2026-09-05 10:00:00',
    '2026-09-05 11:00:00',
    'Published'
FROM teacher t
JOIN subject s
    ON s.institution_id = t.institution_id
JOIN standard st
    ON st.standard_id = s.standard_id
WHERE t.email = 'anita@sunriseschool.edu'
  AND st.standard_name = 'IX'
LIMIT 1;


-- ============================================================
-- 24. TEST - QUESTION
-- ============================================================

INSERT INTO test_question
(
    test_id,
    question_id,
    question_order
)
SELECT
    t.test_id,
    q.question_id,
    1
FROM test t
JOIN question q
    ON q.subject_id = t.subject_id
LIMIT 1;


-- ============================================================
-- 25. TEST ATTEMPT
-- ============================================================

INSERT INTO test_attempt
(
    test_id,
    student_id,
    started_at,
    submitted_at,
    score,
    status
)
SELECT
    t.test_id,
    s.student_id,
    '2026-09-05 10:05:00',
    '2026-09-05 10:20:00',
    1,
    'Submitted'
FROM test t
JOIN student s
    ON s.email = 'rohan@sunriseschool.edu'
LIMIT 1;


-- ============================================================
-- 26. STUDENT ANSWER
-- ============================================================

INSERT INTO student_answer
(
    attempt_id,
    question_id,
    selected_answer,
    is_correct,
    marks_obtained
)
SELECT
    ta.attempt_id,
    tq.question_id,
    q.correct_answer,
    TRUE,
    q.marks
FROM test_attempt ta
JOIN test_question tq
    ON tq.test_id = ta.test_id
JOIN question q
    ON q.question_id = tq.question_id
WHERE ta.student_id =
(
    SELECT student_id
    FROM student
    WHERE email = 'rohan@sunriseschool.edu'
)
LIMIT 1;


-- ============================================================
-- 27. LOGIN HISTORY
-- ============================================================

INSERT INTO login_history
(
    user_role,
    user_id,
    institution_id,
    login_time,
    logout_time,
    ip_address
)
SELECT
    'Admin',
    admin_id,
    NULL,
    '2026-09-01 09:00:00',
    '2026-09-01 10:00:00',
    '127.0.0.1'
FROM admin
WHERE email = 'admin@edumate.com';


INSERT INTO login_history
(
    user_role,
    user_id,
    institution_id,
    login_time,
    logout_time,
    ip_address
)
SELECT
    'Teacher',
    t.teacher_id,
    t.institution_id,
    '2026-09-01 10:00:00',
    '2026-09-01 11:00:00',
    '127.0.0.1'
FROM teacher t
WHERE t.email = 'anita@sunriseschool.edu';


-- ============================================================
-- 28. NOTIFICATIONS
-- ============================================================

INSERT INTO notification
(
    user_role,
    user_id,
    institution_id,
    title,
    message,
    is_read
)
SELECT
    'Teacher',
    t.teacher_id,
    t.institution_id,
    'Welcome to EduMate',
    'Your teacher account has been successfully created.',
    FALSE
FROM teacher t
WHERE t.email = 'anita@sunriseschool.edu';


INSERT INTO notification
(
    user_role,
    user_id,
    institution_id,
    title,
    message,
    is_read
)
SELECT
    'Student',
    s.student_id,
    s.institution_id,
    'New Test Available',
    'A new test has been published for your subject.',
    FALSE
FROM student s
WHERE s.email = 'rohan@sunriseschool.edu';


-- ============================================================
-- VERIFICATION QUERIES
-- ============================================================

-- Courses should now show I-X only ONCE.

SELECT
    course_id,
    course_name,
    institution_category
FROM course_master
ORDER BY institution_category, course_id;


-- Show course-stream mappings

SELECT
    c.course_name,
    c.institution_category,
    s.stream_name
FROM course_stream cs
JOIN course_master c
    ON c.course_id = cs.course_id
JOIN stream_master s
    ON s.stream_id = cs.stream_id
ORDER BY
    c.institution_category,
    c.course_id,
    s.stream_name;


-- Show institution-course mappings

SELECT
    i.institution_name,
    i.institution_category,
    c.course_name
FROM institution_course ic
JOIN institution i
    ON i.institution_id = ic.institution_id
JOIN course_master c
    ON c.course_id = ic.course_id
ORDER BY
    i.institution_id,
    c.course_id;


-- Show institution-stream mappings

SELECT
    i.institution_name,
    i.institution_category,
    s.stream_name
FROM institution_stream ins
JOIN institution i
    ON i.institution_id = ins.institution_id
JOIN stream_master s
    ON s.stream_id = ins.stream_id
ORDER BY
    i.institution_id,
    s.stream_name;


-- ============================================================
-- INSERT DATA COMPLETE
-- ============================================================