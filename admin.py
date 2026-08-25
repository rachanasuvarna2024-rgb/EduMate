import json
import re
from flask import Blueprint, render_template, request, redirect, url_for, session
from session_utils import role_required
from db import conn, cursor

# ============================================================
# ADMIN BLUEPRINT
# ============================================================

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

# ============================================================
# COMMON VALIDATION HELPERS
# ============================================================

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)
NAME_PATTERN = re.compile(
    r"^[A-Za-z][A-Za-z .'-]{1,99}$"
)
PHONE_PATTERN = re.compile(
    r"^[0-9]{10}$"
)
PINCODE_PATTERN = re.compile(
    r"^[0-9]{6}$"
)
INSTITUTION_CODE_PATTERN = re.compile(
    r"^[A-Za-z0-9_-]{2,30}$"
)
TEXT_NAME_PATTERN = re.compile(
    r"^[A-Za-z][A-Za-z .'-]{0,99}$"
)


def get_parents():
    cursor.execute("""
        SELECT parent_id, name
        FROM parent
        ORDER BY name ASC
    """)
    return cursor.fetchall()


def get_standards():
    cursor.execute("""
        SELECT standard_id, standard_name
        FROM standard
        ORDER BY standard_id ASC
    """)
    return cursor.fetchall()


def get_subjects():
    cursor.execute("""
        SELECT
            sub.subject_id,
            sub.subject_name,
            std.standard_name
        FROM subject sub
        JOIN standard std
            ON sub.standard_id = std.standard_id
        ORDER BY
            std.standard_name ASC,
            sub.subject_name ASC
    """)
    return cursor.fetchall()


# ============================================================
# ADMIN HOME / DASHBOARD
# ============================================================

@admin_bp.route("/")
@admin_bp.route("/dashboard")
@role_required("Admin")
def admin_home():
    return render_template("admin_home.html")


# ============================================================
# VIEW INSTITUTIONS
# ============================================================

@admin_bp.route("/view_institutions")
@role_required("Admin")
def view_institutions():
    cursor.execute("""
        SELECT
            institution_id,
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
        FROM institution
        ORDER BY institution_id DESC
    """)

    institutions = cursor.fetchall()

    return render_template(
        "view_institutions.html",
        institutions=institutions
    )


# ============================================================
# MANAGE INSTITUTIONS
# ============================================================

@admin_bp.route("/manage_institutions")
@role_required("Admin")
def manage_institutions():
    cursor.execute("""
        SELECT
            institution_id,
            institution_name,
            institution_code,
            institution_category,
            institution_type,
            city,
            state,
            email,
            phone
        FROM institution
        ORDER BY institution_name ASC
    """)

    institutions = cursor.fetchall()

    return render_template(
        "manage_institution.html",
        institutions=institutions
    )


# ============================================================
# ADD INSTITUTION
# ============================================================

@admin_bp.route("/add_institution", methods=["GET", "POST"])
@role_required("Admin")
def add_institution():
    if request.method == 'POST':
        # Retrieve form data
        institution_name = request.form.get('institution_name', '').strip()
        institution_code = request.form.get('institution_code', '').strip().upper()
        institution_category = request.form.get('institution_category', '').strip()
        institution_type = request.form.get('institution_type', '').strip()
        address = request.form.get('address', '').strip()
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip()
        pincode = request.form.get('pincode', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        website = request.form.get('website', '').strip()

        # Simple backend validation check
        if not all([institution_name, institution_code, institution_category, 
                    institution_type, address, city, state, pincode, email]):
            return render_template('add_institution.html', err="Please fill out all required fields.")

        try:
            cursor = conn.cursor()
            
            # Insert institution into your institution table
            query = """
                INSERT INTO institution 
                (institution_name, institution_code, institution_category, institution_type, 
                 address, city, state, pincode, email, phone, website)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                institution_name, institution_code, institution_category, institution_type,
                address, city, state, pincode, email, phone or None, website or None
            ))
            
            conn.commit()
            cursor.close()

            return render_template('add_institution.html', msg="Institution added successfully!")

        except Exception as e:
            # Catch database errors (e.g., duplicate code/email)
            return render_template('add_institution.html', err=f"Error adding institution: {str(e)}")

    # GET Request: Simply render the form without querying any extra tables
    return render_template('add_institution.html')

@admin_bp.route('/manage_institution', methods=['GET', 'POST'])
def manage_institution():
    if request.method == 'POST':
        institution_id = request.form.get('institution_id')
        
        # Capture all checked values (including newly added items)
        selected_courses = request.form.getlist('courses')
        selected_departments = request.form.getlist('departments')
        selected_designations = request.form.getlist('designations')

        if not institution_id:
            return render_template('manage_institution.html', err="Please select an institution.")

        try:
            cursor = conn.cursor(dictionary=True)

            # Process Courses (Example insertion / linking logic)
            for course_name in selected_courses:
                # Insert course logic or linking logic goes here
                pass

            # Process Departments
            for dept_name in selected_departments:
                # Insert department logic or linking logic goes here
                pass

            # Process Designations
            for desig_name in selected_designations:
                # Insert designation logic or linking logic goes here
                pass

            conn.commit()
            cursor.close()

            # Reload institutions list for the page view after POST
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, institution_name, institution_code FROM institution")
            institutions = cursor.fetchall()
            cursor.close()

            return render_template(
                'manage_institution.html', 
                msg="Institution details updated successfully!", 
                institutions=institutions
            )

        except Exception as e:
            conn.rollback()
            return render_template('manage_institution.html', err=f"Database error: {str(e)}")

    # GET Request: Retrieve existing institutions for the dropdown
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, institution_name, institution_code FROM institution")
        institutions = cursor.fetchall()
        cursor.close()
    except Exception as e:
        institutions = []

    return render_template('manage_institution.html', institutions=institutions)

# ============================================================
# ADD TEACHER
# ============================================================

@admin_bp.route("/add_teacher", methods=["GET", "POST"])
@role_required("Admin")
def add_teacher():
    if request.method == "GET":
        return render_template("add_teacher.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    mobile = request.form.get("mobile", "").strip()
    department = request.form.get("department", "").strip()
    designation = request.form.get("designation", "").strip()

    if not name:
        return render_template("add_teacher.html", message="Name is required.")

    if not email or not EMAIL_PATTERN.fullmatch(email):
        return render_template("add_teacher.html", message="Please enter a valid email address.")

    if not password:
        return render_template("add_teacher.html", message="Password is required.")

    if mobile and not PHONE_PATTERN.fullmatch(mobile):
        return render_template("add_teacher.html", message="Mobile number must contain exactly 10 digits.")

    try:
        cursor.execute("SELECT teacher_id FROM teacher WHERE email = %s", (email,))
        if cursor.fetchone():
            return render_template("add_teacher.html", message="Teacher email already exists.")

        cursor.execute("""
            INSERT INTO teacher (name, email, password, mobile, department, designation)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            name, email, password,
            mobile if mobile else None,
            department if department else None,
            designation if designation else None
        ))
        conn.commit()
        return render_template("add_teacher.html", message="Teacher added successfully!")

    except Exception as e:
        conn.rollback()
        return render_template("add_teacher.html", message="Error adding teacher: " + str(e))


# ============================================================
# VIEW TEACHERS
# ============================================================

@admin_bp.route("/view_teachers")
@role_required("Admin")
def view_teachers():
    cursor.execute("""
        SELECT teacher_id, name, email, mobile, department, designation
        FROM teacher
        ORDER BY teacher_id ASC
    """)
    teachers = cursor.fetchall()
    return render_template("view_teachers.html", teachers=teachers)


# ============================================================
# EDIT TEACHER
# ============================================================

@admin_bp.route("/edit_teacher/<int:teacher_id>", methods=["GET", "POST"])
@role_required("Admin")
def edit_teacher(teacher_id):
    cursor.execute("""
        SELECT teacher_id, name, email, mobile, department, designation
        FROM teacher WHERE teacher_id = %s
    """, (teacher_id,))
    teacher = cursor.fetchone()

    if not teacher:
        return "Teacher not found", 404

    if request.method == "GET":
        return render_template("edit_teacher.html", teacher=teacher)

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    mobile = request.form.get("mobile", "").strip()
    department = request.form.get("department", "").strip()
    designation = request.form.get("designation", "").strip()

    if not name:
        return render_template("edit_teacher.html", teacher=teacher, message="Name is required.")

    if not email or not EMAIL_PATTERN.fullmatch(email):
        return render_template("edit_teacher.html", teacher=teacher, message="Please enter a valid email address.")

    if mobile and not PHONE_PATTERN.fullmatch(mobile):
        return render_template("edit_teacher.html", teacher=teacher, message="Mobile number must contain exactly 10 digits.")

    try:
        cursor.execute("SELECT teacher_id FROM teacher WHERE email = %s AND teacher_id != %s", (email, teacher_id))
        if cursor.fetchone():
            return render_template("edit_teacher.html", teacher=teacher, message="Email already exists.")

        cursor.execute("""
            UPDATE teacher
            SET name = %s, email = %s, mobile = %s, department = %s, designation = %s
            WHERE teacher_id = %s
        """, (
            name, email,
            mobile if mobile else None,
            department if department else None,
            designation if designation else None,
            teacher_id
        ))
        conn.commit()
        return redirect(url_for("admin.view_teachers"))

    except Exception as e:
        conn.rollback()
        return render_template("edit_teacher.html", teacher=teacher, message="Error updating teacher: " + str(e))


# ============================================================
# DELETE TEACHER
# ============================================================

@admin_bp.route("/delete_teacher/<int:teacher_id>", methods=["POST"])
@role_required("Admin")
def delete_teacher(teacher_id):
    try:
        cursor.execute("DELETE FROM teacher WHERE teacher_id = %s", (teacher_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return "Error deleting teacher: " + str(e)

    return redirect(url_for("admin.view_teachers"))


# ============================================================
# ADD PARENT
# ============================================================

@admin_bp.route("/add_parent", methods=["GET", "POST"])
@role_required("Admin")
def add_parent():
    if request.method == "GET":
        return render_template("add_parent.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    mobile = request.form.get("mobile", "").strip()

    if not name:
        return render_template("add_parent.html", message="Name is required.")

    if not email or not EMAIL_PATTERN.fullmatch(email):
        return render_template("add_parent.html", message="Please enter a valid email address.")

    if not password:
        return render_template("add_parent.html", message="Password is required.")

    if mobile and not PHONE_PATTERN.fullmatch(mobile):
        return render_template("add_parent.html", message="Mobile number must contain exactly 10 digits.")

    try:
        cursor.execute("SELECT parent_id FROM parent WHERE email = %s", (email,))
        if cursor.fetchone():
            return render_template("add_parent.html", message="Parent email already exists.")

        cursor.execute("""
            INSERT INTO parent (name, email, password, mobile)
            VALUES (%s, %s, %s, %s)
        """, (name, email, password, mobile if mobile else None))
        conn.commit()
        return render_template("add_parent.html", message="Parent added successfully!")

    except Exception as e:
        conn.rollback()
        return render_template("add_parent.html", message="Error adding parent: " + str(e))


# ============================================================
# VIEW PARENTS
# ============================================================

@admin_bp.route("/view_parents")
@role_required("Admin")
def view_parents():
    cursor.execute("SELECT parent_id, name, email, mobile FROM parent ORDER BY parent_id ASC")
    parents = cursor.fetchall()
    return render_template("view_parents.html", parents=parents)


# ============================================================
# EDIT PARENT
# ============================================================

@admin_bp.route("/edit_parent/<int:parent_id>", methods=["GET", "POST"])
@role_required("Admin")
def edit_parent(parent_id):
    cursor.execute("SELECT parent_id, name, email, mobile FROM parent WHERE parent_id = %s", (parent_id,))
    parent = cursor.fetchone()

    if not parent:
        return "Parent not found", 404

    if request.method == "GET":
        return render_template("edit_parent.html", parent=parent)

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    mobile = request.form.get("mobile", "").strip()

    if not name:
        return render_template("edit_parent.html", parent=parent, message="Name is required.")

    if not email or not EMAIL_PATTERN.fullmatch(email):
        return render_template("edit_parent.html", parent=parent, message="Please enter a valid email address.")

    if mobile and not PHONE_PATTERN.fullmatch(mobile):
        return render_template("edit_parent.html", parent=parent, message="Mobile number must contain exactly 10 digits.")

    try:
        cursor.execute("SELECT parent_id FROM parent WHERE email = %s AND parent_id != %s", (email, parent_id))
        if cursor.fetchone():
            return render_template("edit_parent.html", parent=parent, message="Email already exists.")

        cursor.execute("""
            UPDATE parent
            SET name = %s, email = %s, mobile = %s
            WHERE parent_id = %s
        """, (name, email, mobile if mobile else None, parent_id))
        conn.commit()

        return redirect(url_for("admin.view_parents"))

    except Exception as e:
        conn.rollback()
        return render_template("edit_parent.html", parent=parent, message="Error updating parent: " + str(e))


# ============================================================
# DELETE PARENT
# ============================================================

@admin_bp.route("/delete_parent/<int:parent_id>", methods=["POST"])
@role_required("Admin")
def delete_parent(parent_id):
    try:
        cursor.execute("DELETE FROM parent WHERE parent_id = %s", (parent_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return "Error deleting parent: " + str(e)

    return redirect(url_for("admin.view_parents"))


# ============================================================
# ADD STUDENT
# ============================================================

@admin_bp.route("/add_student", methods=["GET", "POST"])
@role_required("Admin")
def add_student():
    parents = get_parents()
    standards = get_standards()

    if request.method == "GET":
        return render_template("add_student.html", parents=parents, standards=standards)

    parent_id = request.form.get("parent_id", "").strip()
    standard_id = request.form.get("standard_id", "").strip()
    admission_no = request.form.get("admission_no", "").strip()
    roll_no = request.form.get("roll_no", "").strip()
    division = request.form.get("division", "").strip()
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    mobile = request.form.get("mobile", "").strip()

    if not parent_id:
        message = "Please select a parent."
    elif not standard_id:
        message = "Please select a standard."
    elif not name:
        message = "Student name is required."
    elif not email or not EMAIL_PATTERN.fullmatch(email):
        message = "Please enter a valid email address."
    elif not password:
        message = "Password is required."
    elif mobile and not PHONE_PATTERN.fullmatch(mobile):
        message = "Mobile number must contain exactly 10 digits."
    else:
        try:
            cursor.execute("SELECT student_id FROM student WHERE email = %s", (email,))
            if cursor.fetchone():
                message = "Student email already exists."
            else:
                cursor.execute("""
                    INSERT INTO student
                    (parent_id, standard_id, admission_no, roll_no, division, name, email, password, mobile)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    parent_id, standard_id,
                    admission_no if admission_no else None,
                    roll_no,
                    division if division else None,
                    name, email, password,
                    mobile if mobile else None
                ))
                conn.commit()
                message = "Student added successfully!"
        except Exception as e:
            conn.rollback()
            message = "Error adding student: " + str(e)

    return render_template(
        "add_student.html",
        parents=parents,
        standards=standards,
        message=message
    )


# ============================================================
# VIEW STUDENTS
# ============================================================

@admin_bp.route("/view_students")
@role_required("Admin")
def view_students():
    cursor.execute("""
        SELECT
            s.student_id, s.admission_no, s.roll_no, s.division,
            s.name, s.email, s.mobile, p.name AS parent_name, st.standard_name
        FROM student s
        JOIN parent p ON s.parent_id = p.parent_id
        JOIN standard st ON s.standard_id = st.standard_id
        ORDER BY s.student_id ASC
    """)
    students = cursor.fetchall()
    return render_template("view_students.html", students=students)


# ============================================================
# EDIT STUDENT
# ============================================================

@admin_bp.route("/edit_student/<int:student_id>", methods=["GET", "POST"])
@role_required("Admin")
def edit_student(student_id):
    parents = get_parents()
    standards = get_standards()

    cursor.execute("""
        SELECT student_id, parent_id, standard_id, admission_no, roll_no, division, name, email, mobile
        FROM student WHERE student_id = %s
    """, (student_id,))

    student = cursor.fetchone()

    if not student:
        return "Student not found", 404

    if request.method == "GET":
        return render_template(
            "edit_student.html",
            student=student,
            parents=parents,
            standards=standards
        )

    parent_id = request.form.get("parent_id", "").strip()
    standard_id = request.form.get("standard_id", "").strip()
    admission_no = request.form.get("admission_no", "").strip()
    roll_no = request.form.get("roll_no", "").strip()
    division = request.form.get("division", "").strip()
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    mobile = request.form.get("mobile", "").strip()

    message = None
    if not parent_id:
        message = "Please select a parent."
    elif not standard_id:
        message = "Please select a standard."
    elif not name:
        message = "Student name is required."
    elif not email or not EMAIL_PATTERN.fullmatch(email):
        message = "Please enter a valid email address."
    elif mobile and not PHONE_PATTERN.fullmatch(mobile):
        message = "Mobile number must contain exactly 10 digits."

    if message:
        return render_template(
            "edit_student.html",
            student=student,
            parents=parents,
            standards=standards,
            message=message
        )

    try:
        cursor.execute("SELECT student_id FROM student WHERE email = %s AND student_id != %s", (email, student_id))
        if cursor.fetchone():
            return render_template(
                "edit_student.html",
                student=student,
                parents=parents,
                standards=standards,
                message="Email already exists."
            )

        cursor.execute("""
            UPDATE student
            SET parent_id = %s, standard_id = %s, admission_no = %s, roll_no = %s,
                division = %s, name = %s, email = %s, mobile = %s
            WHERE student_id = %s
        """, (
            parent_id, standard_id,
            admission_no if admission_no else None,
            roll_no,
            division if division else None,
            name, email,
            mobile if mobile else None,
            student_id
        ))
        conn.commit()

        return redirect(url_for("admin.view_students"))

    except Exception as e:
        conn.rollback()
        return render_template(
            "edit_student.html",
            student=student,
            parents=parents,
            standards=standards,
            message="Error updating student: " + str(e)
        )


# ============================================================
# DELETE STUDENT
# ============================================================

@admin_bp.route("/delete_student/<int:student_id>", methods=["POST"])
@role_required("Admin")
def delete_student(student_id):
    try:
        cursor.execute("DELETE FROM student WHERE student_id = %s", (student_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return "Error deleting student: " + str(e)

    return redirect(url_for("admin.view_students"))


# ============================================================
# ADD STANDARD
# ============================================================

@admin_bp.route("/add_standard", methods=["GET", "POST"])
@role_required("Admin")
def add_standard():
    msg = None
    err = None

    if request.method == "POST":
        standard_name = request.form.get("standard_name", "").strip()

        if not standard_name:
            err = "Standard name is required."
        elif len(standard_name) > 50:
            err = "Standard name cannot exceed 50 characters."
        else:
            try:
                cursor.execute("SELECT standard_id FROM standard WHERE LOWER(standard_name) = LOWER(%s)", (standard_name,))
                if cursor.fetchone():
                    err = "This standard already exists."
                else:
                    cursor.execute("INSERT INTO standard (standard_name) VALUES (%s)", (standard_name,))
                    conn.commit()
                    msg = "Standard added successfully!"
            except Exception:
                conn.rollback()
                err = "Unable to add standard."

    cursor.execute("SELECT * FROM standard ORDER BY standard_id ASC")
    standards = cursor.fetchall()

    return render_template("add_standard.html", msg=msg, err=err, standards=standards)


# ============================================================
# EDIT STANDARD
# ============================================================

@admin_bp.route("/edit_standard/<int:standard_id>", methods=["GET", "POST"])
@role_required("Admin")
def edit_standard(standard_id):
    err = None

    if request.method == "POST":
        standard_name = request.form.get("standard_name", "").strip()

        if not standard_name:
            err = "Standard name is required."
        elif len(standard_name) > 50:
            err = "Standard name cannot exceed 50 characters."
        else:
            try:
                cursor.execute("""
                    SELECT standard_id FROM standard
                    WHERE LOWER(standard_name) = LOWER(%s) AND standard_id != %s
                """, (standard_name, standard_id))

                if cursor.fetchone():
                    err = "This standard already exists."
                else:
                    cursor.execute("""
                        UPDATE standard SET standard_name = %s WHERE standard_id = %s
                    """, (standard_name, standard_id))
                    conn.commit()
                    return redirect(url_for("admin.add_standard"))
            except Exception:
                conn.rollback()
                err = "Unable to update standard."

    cursor.execute("SELECT * FROM standard WHERE standard_id = %s", (standard_id,))
    standard = cursor.fetchone()

    if not standard:
        return redirect(url_for("admin.add_standard"))

    return render_template("edit_standard.html", standard=standard, err=err)


# ============================================================
# DELETE STANDARD
# ============================================================

@admin_bp.route("/delete_standard/<int:standard_id>", methods=["POST"])
@role_required("Admin")
def delete_standard(standard_id):
    try:
        cursor.execute("DELETE FROM standard WHERE standard_id = %s", (standard_id,))
        conn.commit()
    except Exception:
        conn.rollback()

    return redirect(url_for("admin.add_standard"))


# ============================================================
# ADD SUBJECT
# ============================================================

@admin_bp.route("/add_subject", methods=["GET", "POST"])
@role_required("Admin")
def add_subject():
    msg = None
    err = None

    if request.method == "POST":
        standard_id = request.form.get("standard_id", "").strip()
        subject_name = request.form.get("subject_name", "").strip()
        assessment_type = request.form.get("assessment_type", "Traditional").strip()

        if not standard_id:
            err = "Please select a standard."
        elif not subject_name:
            err = "Subject name is required."
        elif len(subject_name) > 100:
            err = "Subject name cannot exceed 100 characters."
        elif assessment_type not in ["Traditional", "OBE"]:
            err = "Invalid assessment type selected."
        else:
            try:
                cursor.execute("""
                    SELECT subject_id FROM subject
                    WHERE standard_id = %s AND LOWER(subject_name) = LOWER(%s)
                """, (standard_id, subject_name))

                if cursor.fetchone():
                    err = "This subject already exists for the selected standard."
                else:
                    cursor.execute("""
                        INSERT INTO subject (standard_id, subject_name, assessment_type)
                        VALUES (%s, %s, %s)
                    """, (standard_id, subject_name, assessment_type))
                    conn.commit()
                    msg = "Subject added successfully!"
            except Exception:
                conn.rollback()
                err = "Unable to add subject."

    standards = get_standards()
    cursor.execute("""
        SELECT sub.subject_id, sub.subject_name, sub.assessment_type, std.standard_name
        FROM subject sub
        JOIN standard std ON sub.standard_id = std.standard_id
        ORDER BY sub.subject_id ASC
    """)
    subjects = cursor.fetchall()

    return render_template("add_subject.html", msg=msg, err=err, standards=standards, subjects=subjects)


# ============================================================
# EDIT SUBJECT
# ============================================================

@admin_bp.route("/edit_subject/<int:subject_id>", methods=["GET", "POST"])
@role_required("Admin")
def edit_subject(subject_id):
    err = None

    if request.method == "POST":
        standard_id = request.form.get("standard_id", "").strip()
        subject_name = request.form.get("subject_name", "").strip()
        assessment_type = request.form.get("assessment_type", "Traditional").strip()

        if not standard_id:
            err = "Please select a standard."
        elif not subject_name:
            err = "Subject name is required."
        elif len(subject_name) > 100:
            err = "Subject name cannot exceed 100 characters."
        elif assessment_type not in ["Traditional", "OBE"]:
            err = "Invalid assessment type selected."
        else:
            try:
                cursor.execute("""
                    SELECT subject_id FROM subject
                    WHERE standard_id = %s AND LOWER(subject_name) = LOWER(%s) AND subject_id != %s
                """, (standard_id, subject_name, subject_id))

                if cursor.fetchone():
                    err = "This subject already exists for the selected standard."
                else:
                    cursor.execute("""
                        UPDATE subject
                        SET standard_id = %s, subject_name = %s, assessment_type = %s
                        WHERE subject_id = %s
                    """, (standard_id, subject_name, assessment_type, subject_id))
                    conn.commit()
                    return redirect(url_for("admin.add_subject"))
            except Exception:
                conn.rollback()
                err = "Unable to update subject."

    cursor.execute("SELECT * FROM subject WHERE subject_id = %s", (subject_id,))
    subject = cursor.fetchone()

    if not subject:
        return redirect(url_for("admin.add_subject"))

    standards = get_standards()
    return render_template("edit_subject.html", subject=subject, standards=standards, err=err)


# ============================================================
# DELETE SUBJECT
# ============================================================

@admin_bp.route("/delete_subject/<int:subject_id>", methods=["POST"])
@role_required("Admin")
def delete_subject(subject_id):
    try:
        cursor.execute("DELETE FROM subject WHERE subject_id = %s", (subject_id,))
        conn.commit()
    except Exception:
        conn.rollback()

    return redirect(url_for("admin.add_subject"))


# ============================================================
# ADD CHAPTER
# ============================================================

@admin_bp.route("/add_chapter", methods=["GET", "POST"])
@role_required("Admin")
def add_chapter():
    msg = None
    err = None

    if request.method == "POST":
        subject_id = request.form.get("subject_id", "").strip()
        chapter_number = request.form.get("chapter_number", "").strip()
        chapter_name = request.form.get("chapter_name", "").strip()

        if not subject_id:
            err = "Please select a subject."
        elif not chapter_name:
            err = "Chapter name is required."
        elif len(chapter_name) > 200:
            err = "Chapter name cannot exceed 200 characters."
        elif chapter_number and (not chapter_number.isdigit() or int(chapter_number) <= 0):
            err = "Chapter number must be a valid positive integer."
        else:
            try:
                chapter_num_value = int(chapter_number) if chapter_number else None
                cursor.execute("""
                    SELECT chapter_id FROM chapter
                    WHERE subject_id = %s AND (chapter_number = %s OR LOWER(chapter_name) = LOWER(%s))
                """, (subject_id, chapter_num_value, chapter_name))

                if cursor.fetchone():
                    err = "This chapter already exists for the selected subject."
                else:
                    cursor.execute("""
                        INSERT INTO chapter (subject_id, chapter_number, chapter_name)
                        VALUES (%s, %s, %s)
                    """, (subject_id, chapter_num_value, chapter_name))
                    conn.commit()
                    msg = "Chapter added successfully!"
            except Exception:
                conn.rollback()
                err = "Unable to add chapter."

    subjects = get_subjects()
    cursor.execute("""
        SELECT ch.chapter_id, ch.chapter_number, ch.chapter_name, sub.subject_name
        FROM chapter ch
        JOIN subject sub ON ch.subject_id = sub.subject_id
        ORDER BY ch.chapter_id ASC
    """)
    chapters = cursor.fetchall()

    return render_template("add_chapter.html", msg=msg, err=err, subjects=subjects, chapters=chapters)


# ============================================================
# EDIT CHAPTER
# ============================================================

@admin_bp.route("/edit_chapter/<int:chapter_id>", methods=["GET", "POST"])
@role_required("Admin")
def edit_chapter(chapter_id):
    err = None

    if request.method == "POST":
        subject_id = request.form.get("subject_id", "").strip()
        chapter_number = request.form.get("chapter_number", "").strip()
        chapter_name = request.form.get("chapter_name", "").strip()

        if not subject_id:
            err = "Please select a subject."
        elif not chapter_name:
            err = "Chapter name is required."
        elif len(chapter_name) > 200:
            err = "Chapter name cannot exceed 200 characters."
        elif chapter_number and (not chapter_number.isdigit() or int(chapter_number) <= 0):
            err = "Chapter number must be a valid positive integer."
        else:
            try:
                chapter_num_value = int(chapter_number) if chapter_number else None
                cursor.execute("""
                    SELECT chapter_id FROM chapter
                    WHERE subject_id = %s
                    AND (chapter_number = %s OR LOWER(chapter_name) = LOWER(%s))
                    AND chapter_id != %s
                """, (subject_id, chapter_num_value, chapter_name, chapter_id))

                if cursor.fetchone():
                    err = "Another chapter with these details already exists."
                else:
                    cursor.execute("""
                        UPDATE chapter
                        SET subject_id = %s, chapter_number = %s, chapter_name = %s
                        WHERE chapter_id = %s
                    """, (subject_id, chapter_num_value, chapter_name, chapter_id))
                    conn.commit()
                    return redirect(url_for("admin.add_chapter"))
            except Exception:
                conn.rollback()
                err = "Unable to update chapter."

    cursor.execute("SELECT * FROM chapter WHERE chapter_id = %s", (chapter_id,))
    chapter = cursor.fetchone()

    if not chapter:
        return redirect(url_for("admin.add_chapter"))

    subjects = get_subjects()
    return render_template("edit_chapter.html", chapter=chapter, subjects=subjects, err=err)


# ============================================================
# DELETE CHAPTER
# ============================================================

@admin_bp.route("/delete_chapter/<int:chapter_id>", methods=["POST"])
@role_required("Admin")
def delete_chapter(chapter_id):
    try:
        cursor.execute("DELETE FROM chapter WHERE chapter_id = %s", (chapter_id,))
        conn.commit()
    except Exception:
        conn.rollback()

    return redirect(url_for("admin.add_chapter"))


# ============================================================
# STUDENT PROGRESS
# ============================================================

@admin_bp.route("/student_progress_for_admin")
@role_required("Admin")
def student_progress_for_admin():
    return render_template("student_progress_for_admin.html")


# ============================================================
# ADMIN PROFILE
# ============================================================

@admin_bp.route("/profile", methods=["GET", "POST"])
@role_required("Admin")
def admin_profile():
    admin_id = session.get("user_id")
    msg = None
    err = None

    if not admin_id:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()

        if not name:
            err = "Name is required."
        elif len(name) > 100:
            err = "Name cannot exceed 100 characters."
        elif not EMAIL_PATTERN.fullmatch(email):
            err = "Please enter a valid email address."
        else:
            try:
                cursor.execute("""
                    SELECT admin_id FROM admin
                    WHERE email = %s AND admin_id != %s
                """, (email, admin_id))

                if cursor.fetchone():
                    err = "Email is already in use."
                else:
                    cursor.execute("""
                        UPDATE admin SET name = %s, email = %s WHERE admin_id = %s
                    """, (name, email, admin_id))
                    conn.commit()
                    session["name"] = name
                    msg = "Profile updated successfully!"
            except Exception:
                conn.rollback()
                err = "Unable to update profile."

    cursor.execute("SELECT admin_id, name, email FROM admin WHERE admin_id = %s", (admin_id,))
    admin_data = cursor.fetchone()

    if not admin_data:
        return redirect(url_for("auth.login"))

    return render_template("admin_profile.html", admin=admin_data, msg=msg, err=err)