from flask import Blueprint, render_template, request, redirect, url_for
from session_utils import role_required
from db import conn, cursor

# ---------------------------------
# ADMIN BLUEPRINT
# ---------------------------------
admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

# ---------------------------------
# ADMIN DASHBOARD
# ---------------------------------
@admin_bp.route("/")
def admin_home():

    check = role_required("Admin")
    if check:
        return check

    return render_template("admin_home.html")


# ---------------------------------
# ADMIN FUNCTIONS
# ---------------------------------
@admin_bp.route("/add_teacher", methods=["GET", "POST"])
def add_teacher():
    check = role_required("Admin")
    if check:
        return check
    
    # ---------------------------------
    # DISPLAY FORM
    # ---------------------------------
    if request.method == "GET":
        return render_template("add_teacher.html")
    
    # ---------------------------------
    # PROCESS FORM
    # ---------------------------------
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    mobile = request.form["mobile"]
    department = request.form["department"]
    designation = request.form["designation"]

    # ---------------------------------
    # INSERT TEACHER INTO DATABASE
    # ---------------------------------
    try:

        query = """
            INSERT INTO teacher
            (name, email, password, mobile, department, designation)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            name,
            email,
            password,
            mobile,
            department,
            designation
        )

        cursor.execute(query, values)

        conn.commit()

        return render_template(
            "add_teacher.html",
            message="Teacher added successfully!"
        )


    except Exception as e:

        conn.rollback()

        return render_template(
            "add_teacher.html",
            message="Error adding teacher: " + str(e)
        )

#---------------------------------
# VIEW TEACHERS
#---------------------------------
@admin_bp.route("/view_teachers")
def view_teachers():

    check = role_required("Admin")
    if check:
        return check

    query = """
        SELECT
            teacher_id,
            name,
            email,
            mobile,
            department,
            designation
        FROM teacher
        ORDER BY teacher_id
    """

    cursor.execute(query)

    teachers = cursor.fetchall()

    return render_template(
        "view_teachers.html",
        teachers=teachers
    )

    # ---------------------------------
    # EDIT TEACHERS
    # ---------------------------------
@admin_bp.route("/edit_teacher/<int:teacher_id>", methods=["GET", "POST"])
def edit_teacher(teacher_id):

    check = role_required("Admin")
    if check:
        return check

    # ---------------------------------
    # GET EXISTING TEACHER
    # ---------------------------------

    query = """
        SELECT
            teacher_id,
            name,
            email,
            mobile,
            department,
            designation
        FROM teacher
        WHERE teacher_id = %s
    """

    cursor.execute(query, (teacher_id,))

    teacher = cursor.fetchone()

    if not teacher:
        return "Teacher not found"


    # ---------------------------------
    # DISPLAY EDIT FORM
    # ---------------------------------

    if request.method == "GET":

        return render_template(
            "edit_teacher.html",
            teacher=teacher
        )


    # ---------------------------------
    # GET UPDATED DETAILS
    # ---------------------------------

    name = request.form["name"]
    email = request.form["email"]
    mobile = request.form["mobile"]
    department = request.form["department"]
    designation = request.form["designation"]


    # ---------------------------------
    # UPDATE DATABASE
    # ---------------------------------

    try:

        query = """
            UPDATE teacher
            SET
                name = %s,
                email = %s,
                mobile = %s,
                department = %s,
                designation = %s
            WHERE teacher_id = %s
        """

        values = (
            name,
            email,
            mobile,
            department,
            designation,
            teacher_id
        )

        cursor.execute(query, values)

        conn.commit()


        return redirect(
            url_for("admin.view_teachers")
        )


    except Exception as e:

        conn.rollback()

        return render_template(
            "edit_teacher.html",
            teacher=teacher,
            message="Error updating teacher: " + str(e)
        )

# ---------------------------------
# DELETE TEACHER
# ---------------------------------
@admin_bp.route("/delete_teacher/<int:teacher_id>", methods=["POST"])
def delete_teacher(teacher_id):

    check = role_required("Admin")
    if check:
        return check

    try:

        query = """
            DELETE FROM teacher
            WHERE teacher_id = %s
        """

        cursor.execute(query, (teacher_id,))

        conn.commit()

        return redirect(
            url_for("admin.view_teachers")
        )


    except Exception as e:

        conn.rollback()

        return "Error deleting teacher: " + str(e)

    # ---------------------------------
    # ADD PARENT
    # ---------------------------------
@admin_bp.route("/add_parent", methods=["GET", "POST"])
def add_parent():

    check = role_required("Admin")
    if check:
        return check

    # ---------------------------------
    # DISPLAY FORM
    # ---------------------------------

    if request.method == "GET":
        return render_template("add_parent.html")


    # ---------------------------------
    # PROCESS FORM
    # ---------------------------------

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    mobile = request.form["mobile"]


    # ---------------------------------
    # INSERT PARENT INTO DATABASE
    # ---------------------------------

    try:

        query = """
            INSERT INTO parent
            (name, email, password, mobile)
            VALUES (%s, %s, %s, %s)
        """

        values = (
            name,
            email,
            password,
            mobile
        )

        cursor.execute(query, values)

        conn.commit()

        return render_template(
            "add_parent.html",
            message="Parent added successfully!"
        )


    except Exception as e:

        conn.rollback()

        return render_template(
            "add_parent.html",
            message="Error adding parent: " + str(e)
        )

# ---------------------------------
# VIEW PARENTS  

@admin_bp.route("/view_parents")
def view_parents():

    check = role_required("Admin")
    if check:
        return check

    query = """
        SELECT
            parent_id,
            name,
            email,
            mobile
        FROM parent
        ORDER BY parent_id
    """

    cursor.execute(query)

    parents = cursor.fetchall()

    return render_template(
        "view_parents.html",
        parents=parents
    )

# ---------------------------------
# EDIT PARENT
# ---------------------------------
@admin_bp.route("/edit_parent/<int:parent_id>", methods=["GET", "POST"])
def edit_parent(parent_id):

    check = role_required("Admin")
    if check:
        return check

    # ---------------------------------
    # GET EXISTING PARENT
    # ---------------------------------

    query = """
        SELECT
            parent_id,
            name,
            email,
            mobile
        FROM parent
        WHERE parent_id = %s
    """

    cursor.execute(query, (parent_id,))

    parent = cursor.fetchone()

    if not parent:
        return "Parent not found"


    # ---------------------------------
    # DISPLAY EDIT FORM
    # ---------------------------------

    if request.method == "GET":

        return render_template(
            "edit_parent.html",
            parent=parent
        )


    # ---------------------------------
    # GET UPDATED DETAILS
    # ---------------------------------

    name = request.form["name"]
    email = request.form["email"]
    mobile = request.form["mobile"]


    # ---------------------------------
    # UPDATE DATABASE
    # ---------------------------------

    try:

        query = """
            UPDATE parent
            SET
                name = %s,
                email = %s,
                mobile = %s
            WHERE parent_id = %s
        """

        values = (
            name,
            email,
            mobile,
            parent_id
        )

        cursor.execute(query, values)

        conn.commit()

        return redirect(
            url_for("admin.view_parents")
        )


    except Exception as e:

        conn.rollback()

        return render_template(
            "edit_parent.html",
            parent=parent,
            message="Error updating parent: " + str(e)
        )

# ---------------------------------
# DELETE PARENT
# ---------------------------------
@admin_bp.route("/delete_parent/<int:parent_id>", methods=["POST"])
def delete_parent(parent_id):

    check = role_required("Admin")
    if check:
        return check

    try:

        query = """
            DELETE FROM parent
            WHERE parent_id = %s
        """

        cursor.execute(query, (parent_id,))

        conn.commit()

        return redirect(
            url_for("admin.view_parents")
        )


    except Exception as e:

        conn.rollback()

        return "Error deleting parent: " + str(e)

# ---------------------------------
# ADD STUDENT
# ---------------------------------
@admin_bp.route("/add_student", methods=["GET", "POST"])
def add_student():

    check = role_required("Admin")
    if check:
        return check

    # ---------------------------------
    # GET PARENTS
    # ---------------------------------

    cursor.execute("""
        SELECT parent_id, name
        FROM parent
        ORDER BY name
    """)

    parents = cursor.fetchall()

    # ---------------------------------
    # GET STANDARDS
    # ---------------------------------

    cursor.execute("""
        SELECT standard_id, standard_name
        FROM standard
        ORDER BY standard_id
    """)

    standards = cursor.fetchall()

    # ---------------------------------
    # DISPLAY FORM
    # ---------------------------------

    if request.method == "GET":

        return render_template(
            "add_student.html",
            parents=parents,
            standards=standards
        )

    # ---------------------------------
    # GET FORM DATA
    # ---------------------------------

    parent_id = request.form["parent_id"]
    standard_id = request.form["standard_id"]

    admission_no = request.form["admission_no"].strip()
    roll_no = request.form["roll_no"].strip()
    division = request.form["division"].strip()

    name = request.form["name"].strip()
    email = request.form["email"].strip()

    password = request.form["password"]
    mobile = request.form["mobile"].strip()

    # ---------------------------------
    # INSERT STUDENT INTO DATABASE
    # ---------------------------------

    try:

        query = """
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
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """

        values = (
            parent_id,
            standard_id,
            admission_no if admission_no else None,
            roll_no,
            division if division else None,
            name,
            email,
            password,
            mobile if mobile else None
        )

        cursor.execute(query, values)

        conn.commit()

        return render_template(
            "add_student.html",
            parents=parents,
            standards=standards,
            message="Student added successfully!"
        )

    except Exception as e:

        conn.rollback()

        return render_template(
            "add_student.html",
            parents=parents,
            standards=standards,
            message="Error adding student: " + str(e)
        )


# ---------------------------------
# VIEW STUDENTS
# ---------------------------------
@admin_bp.route("/view_students")
def view_students():

    check = role_required("Admin")
    if check:
        return check

    query = """
        SELECT
            s.student_id,
            s.admission_no,
            s.roll_no,
            s.division,
            s.name,
            s.email,
            s.mobile,
            p.name AS parent_name,
            st.standard_name
        FROM student s
        JOIN parent p
            ON s.parent_id = p.parent_id
        JOIN standard st
            ON s.standard_id = st.standard_id
        ORDER BY s.student_id
    """

    cursor.execute(query)

    students = cursor.fetchall()

    return render_template(
        "view_students.html",
        students=students
    )


# ---------------------------------
# EDIT STUDENT
# ---------------------------------
@admin_bp.route("/edit_student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):

    check = role_required("Admin")
    if check:
        return check

    # ---------------------------------
    # GET PARENTS
    # ---------------------------------

    cursor.execute("""
        SELECT parent_id, name
        FROM parent
        ORDER BY name
    """)

    parents = cursor.fetchall()

    # ---------------------------------
    # GET STANDARDS
    # ---------------------------------

    cursor.execute("""
        SELECT standard_id, standard_name
        FROM standard
        ORDER BY standard_id
    """)

    standards = cursor.fetchall()

    # ---------------------------------
    # GET EXISTING STUDENT
    # ---------------------------------

    query = """
        SELECT
            student_id,
            parent_id,
            standard_id,
            admission_no,
            roll_no,
            division,
            name,
            email,
            mobile
        FROM student
        WHERE student_id = %s
    """

    cursor.execute(query, (student_id,))

    student = cursor.fetchone()

    if not student:
        return "Student not found"

    # ---------------------------------
    # DISPLAY EDIT FORM
    # ---------------------------------

    if request.method == "GET":

        return render_template(
            "edit_student.html",
            student=student,
            parents=parents,
            standards=standards
        )

    # ---------------------------------
    # GET UPDATED DETAILS
    # ---------------------------------

    parent_id = request.form["parent_id"]
    standard_id = request.form["standard_id"]

    admission_no = request.form["admission_no"].strip()
    roll_no = request.form["roll_no"].strip()
    division = request.form["division"].strip()

    name = request.form["name"].strip()
    email = request.form["email"].strip()

    mobile = request.form["mobile"].strip()

    # ---------------------------------
    # UPDATE STUDENT
    # ---------------------------------

    try:

        query = """
            UPDATE student
            SET
                parent_id = %s,
                standard_id = %s,
                admission_no = %s,
                roll_no = %s,
                division = %s,
                name = %s,
                email = %s,
                mobile = %s
            WHERE student_id = %s
        """

        values = (
            parent_id,
            standard_id,
            admission_no if admission_no else None,
            roll_no,
            division if division else None,
            name,
            email,
            mobile if mobile else None,
            student_id
        )

        cursor.execute(query, values)

        conn.commit()

        return redirect(
            url_for("admin.view_students")
        )

    except Exception as e:

        conn.rollback()

        return render_template(
            "edit_student.html",
            student=student,
            parents=parents,
            standards=standards,
            message="Error updating student: " + str(e)
        )


# ---------------------------------
# DELETE STUDENT
# ---------------------------------
@admin_bp.route("/delete_student/<int:student_id>", methods=["POST"])
def delete_student(student_id):

    check = role_required("Admin")
    if check:
        return check

    try:

        query = """
            DELETE FROM student
            WHERE student_id = %s
        """

        cursor.execute(query, (student_id,))

        conn.commit()

        return redirect(
            url_for("admin.view_students")
        )

    except Exception as e:

        conn.rollback()

        return "Error deleting student: " + str(e)


# ---------------------------------
# ADD STANDARD
# ---------------------------------
@admin_bp.route('/add_standard', methods=['GET', 'POST'])
def add_standard():
    check = role_required("Admin")
    if check:
        return check

    msg = None
    err = None

    if request.method == 'POST':
        standard_name = request.form.get('standard_name', '').strip()

        if not standard_name:
            err = "Standard name is required."
        elif len(standard_name) > 50:
            err = "Standard name cannot exceed 50 characters."
        else:
            try:
                cursor.execute("INSERT INTO standard (standard_name) VALUES (%s)", (standard_name,))
                conn.commit()
                msg = "Standard added successfully!"
            except Exception as e:
                conn.rollback()
                err = "Standard name already exists or database error occurred."

    cursor.execute("SELECT * FROM standard ORDER BY standard_id ASC")
    standards = cursor.fetchall()

    return render_template('add_standard.html', msg=msg, err=err, standards=standards)


# ---------------------------------
# EDIT STANDARD
# ---------------------------------
@admin_bp.route('/edit_standard/<int:standard_id>', methods=['GET', 'POST'])
def edit_standard(standard_id):
    check = role_required("Admin")
    if check:
        return check

    err = None

    if request.method == 'POST':
        standard_name = request.form.get('standard_name', '').strip()

        if not standard_name:
            err = "Standard name is required."
        elif len(standard_name) > 50:
            err = "Standard name cannot exceed 50 characters."
        else:
            try:
                cursor.execute(
                    "UPDATE standard SET standard_name = %s WHERE standard_id = %s",
                    (standard_name, standard_id)
                )
                conn.commit()
                return redirect(url_for('admin.add_standard'))
            except Exception as e:
                conn.rollback()
                err = "Standard name already exists or database error occurred."

    cursor.execute("SELECT * FROM standard WHERE standard_id = %s", (standard_id,))
    standard = cursor.fetchone()

    if not standard:
        return redirect(url_for('admin.add_standard'))

    return render_template('edit_standard.html', standard=standard, err=err)


# ---------------------------------
# DELETE STANDARD
# ---------------------------------
@admin_bp.route('/delete_standard/<int:standard_id>', methods=['POST'])
def delete_standard(standard_id):
    check = role_required("Admin")
    if check:
        return check

    try:
        cursor.execute("DELETE FROM standard WHERE standard_id = %s", (standard_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()

    return redirect(url_for('admin.add_standard'))# ---------------------------------

import re

import re

# ---------------------------------
# ADD SUBJECT
# ---------------------------------
@admin_bp.route('/add_subject', methods=['GET', 'POST'])
def add_subject():
    check = role_required("Admin")
    if check:
        return check

    msg = None
    err = None

    if request.method == 'POST':
        standard_id = request.form.get('standard_id', '').strip()
        subject_name = request.form.get('subject_name', '').strip()
        assessment_type = request.form.get('assessment_type', 'Traditional').strip()

        if not standard_id:
            err = "Please select a standard."
        elif not subject_name:
            err = "Subject name is required."
        elif not re.match(r'^[A-Za-z0-9]{1,100}$', subject_name):
            err = "Subject name must contain only letters and numbers (no spaces or special characters)."
        elif assessment_type not in ['Traditional', 'OBE']:
            err = "Invalid assessment type selected."
        else:
            try:
                cursor.execute(
                    "INSERT INTO subject (standard_id, subject_name, assessment_type) VALUES (%s, %s, %s)",
                    (standard_id, subject_name, assessment_type)
                )
                conn.commit()
                msg = "Subject added successfully!"
            except Exception as e:
                conn.rollback()
                err = "Subject already exists for this standard or a database error occurred."

    cursor.execute("SELECT * FROM standard ORDER BY standard_name ASC")
    standards = cursor.fetchall()

    cursor.execute("""
        SELECT sub.subject_id, sub.subject_name, sub.assessment_type, std.standard_name 
        FROM subject sub
        JOIN standard std ON sub.standard_id = std.standard_id
        ORDER BY sub.subject_id ASC
    """)
    subjects = cursor.fetchall()

    return render_template('add_subject.html', msg=msg, err=err, standards=standards, subjects=subjects)


# ---------------------------------
# EDIT SUBJECT
# ---------------------------------
@admin_bp.route('/edit_subject/<int:subject_id>', methods=['GET', 'POST'])
def edit_subject(subject_id):
    check = role_required("Admin")
    if check:
        return check

    err = None

    if request.method == 'POST':
        standard_id = request.form.get('standard_id', '').strip()
        subject_name = request.form.get('subject_name', '').strip()
        assessment_type = request.form.get('assessment_type', 'Traditional').strip()

        if not standard_id:
            err = "Please select a standard."
        elif not subject_name:
            err = "Subject name is required."
        elif not re.match(r'^[A-Za-z0-9]{1,100}$', subject_name):
            err = "Subject name must contain only letters and numbers (no spaces or special characters)."
        elif assessment_type not in ['Traditional', 'OBE']:
            err = "Invalid assessment type selected."
        else:
            try:
                cursor.execute(
                    "UPDATE subject SET standard_id = %s, subject_name = %s, assessment_type = %s WHERE subject_id = %s",
                    (standard_id, subject_name, assessment_type, subject_id)
                )
                conn.commit()
                return redirect(url_for('admin.add_subject'))
            except Exception as e:
                conn.rollback()
                err = "Subject already exists for this standard or a database error occurred."

    cursor.execute("SELECT * FROM subject WHERE subject_id = %s", (subject_id,))
    subject = cursor.fetchone()

    if not subject:
        return redirect(url_for('admin.add_subject'))

    cursor.execute("SELECT * FROM standard ORDER BY standard_name ASC")
    standards = cursor.fetchall()

    return render_template('edit_subject.html', subject=subject, standards=standards, err=err)


# ---------------------------------
# DELETE SUBJECT
# ---------------------------------
@admin_bp.route('/delete_subject/<int:subject_id>', methods=['POST'])
def delete_subject(subject_id):
    check = role_required("Admin")
    if check:
        return check

    try:
        cursor.execute("DELETE FROM subject WHERE subject_id = %s", (subject_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()

    return redirect(url_for('admin.add_subject'))

import re

# ---------------------------------
# ADD CHAPTER
# ---------------------------------
@admin_bp.route('/add_chapter', methods=['GET', 'POST'])
def add_chapter():
    check = role_required("Admin")
    if check:
        return check

    msg = None
    err = None

    if request.method == 'POST':
        subject_id = request.form.get('subject_id', '').strip()
        chapter_number = request.form.get('chapter_number', '').strip()
        chapter_name = request.form.get('chapter_name', '').strip()

        # Backend validations
        if not subject_id:
            err = "Please select a subject."
        elif not chapter_name:
            err = "Chapter name is required."
        elif not re.match(r'^[A-Za-z0-9]{1,200}$', chapter_name):
            err = "Chapter name must contain only letters and numbers (no spaces or special characters)."
        elif chapter_number and (not chapter_number.isdigit() or int(chapter_number) <= 0):
            err = "Chapter number must be a valid positive integer."
        else:
            try:
                # Convert empty string to None for NULL handling in MySQL
                ch_num_val = int(chapter_number) if chapter_number else None

                cursor.execute(
                    "INSERT INTO chapter (subject_id, chapter_number, chapter_name) VALUES (%s, %s, %s)",
                    (subject_id, ch_num_val, chapter_name)
                )
                conn.commit()
                msg = "Chapter added successfully!"
            except Exception as e:
                conn.rollback()
                err = "Database error or chapter already exists for this subject."

    # Fetch subjects with standard names for proper label displaying
    cursor.execute("""
        SELECT sub.subject_id, sub.subject_name, std.standard_name 
        FROM subject sub
        JOIN standard std ON sub.standard_id = std.standard_id
        ORDER BY sub.subject_name ASC
    """)
    subjects = cursor.fetchall()

    # Fetch all chapters
    cursor.execute("""
        SELECT ch.chapter_id, ch.chapter_number, ch.chapter_name, sub.subject_name 
        FROM chapter ch
        JOIN subject sub ON ch.subject_id = sub.subject_id
        ORDER BY ch.chapter_id ASC
    """)
    chapters = cursor.fetchall()

    return render_template('add_chapter.html', msg=msg, err=err, subjects=subjects, chapters=chapters)


# ---------------------------------
# EDIT CHAPTER
# ---------------------------------
@admin_bp.route('/edit_chapter/<int:chapter_id>', methods=['GET', 'POST'])
def edit_chapter(chapter_id):
    check = role_required("Admin")
    if check:
        return check

    err = None

    if request.method == 'POST':
        subject_id = request.form.get('subject_id', '').strip()
        chapter_number = request.form.get('chapter_number', '').strip()
        chapter_name = request.form.get('chapter_name', '').strip()

        if not subject_id:
            err = "Please select a subject."
        elif not chapter_name:
            err = "Chapter name is required."
        elif not re.match(r'^[A-Za-z0-9]{1,200}$', chapter_name):
            err = "Chapter name must contain only letters and numbers (no spaces or special characters)."
        elif chapter_number and (not chapter_number.isdigit() or int(chapter_number) <= 0):
            err = "Chapter number must be a valid positive integer."
        else:
            try:
                ch_num_val = int(chapter_number) if chapter_number else None

                cursor.execute(
                    "UPDATE chapter SET subject_id = %s, chapter_number = %s, chapter_name = %s WHERE chapter_id = %s",
                    (subject_id, ch_num_val, chapter_name, chapter_id)
                )
                conn.commit()
                return redirect(url_for('admin.add_chapter'))
            except Exception as e:
                conn.rollback()
                err = "Database error occurred while updating chapter."

    cursor.execute("SELECT * FROM chapter WHERE chapter_id = %s", (chapter_id,))
    chapter = cursor.fetchone()

    if not chapter:
        return redirect(url_for('admin.add_chapter'))

    cursor.execute("""
        SELECT sub.subject_id, sub.subject_name, std.standard_name 
        FROM subject sub
        JOIN standard std ON sub.standard_id = std.standard_id
        ORDER BY sub.subject_name ASC
    """)
    subjects = cursor.fetchall()

    return render_template('edit_chapter.html', chapter=chapter, subjects=subjects, err=err)


# ---------------------------------
# DELETE CHAPTER
# ---------------------------------
@admin_bp.route('/delete_chapter/<int:chapter_id>', methods=['POST'])
def delete_chapter(chapter_id):
    check = role_required("Admin")
    if check:
        return check

    try:
        cursor.execute("DELETE FROM chapter WHERE chapter_id = %s", (chapter_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()

    return redirect(url_for('admin.add_chapter'))


@admin_bp.route("/student_progress_for_admin")
def student_progress_for_admin():

    check = role_required("Admin")
    if check:
        return check

    return render_template("student_progress_for_admin.html")

import re
from flask import render_template, request, session, redirect, url_for

# ---------------------------------
# ADMIN PROFILE & EDIT
# ---------------------------------
@admin_bp.route('/profile', methods=['GET', 'POST'])
def admin_profile():
    check = role_required("Admin")
    if check:
        return check

    # Assuming session stores the logged-in admin's ID
    admin_id = session.get('user_id')  # Adjust key name if you use session['admin_id']
    msg = None
    err = None

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()

        # Validation checks
        if not name or not email:
            err = "All required fields must be filled out."
        elif not re.match(r'^[A-Za-z0-9]{1,100}$', name):
            err = "Name must contain only letters and numbers (no spaces or special characters)."
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            err = "Please enter a valid email address."
        else:
            try:
                cursor.execute(
                    "UPDATE admin SET name = %s, email = %s WHERE admin_id = %s",
                    (name, email, admin_id)
                )
                conn.commit()
                # Update session data if needed
                session['name'] = name 
                msg = "Profile updated successfully!"
            except Exception as e:
                conn.rollback()
                err = "Email already in use or a database error occurred."

    # Fetch fresh admin details
    cursor.execute("SELECT admin_id, name, email FROM admin WHERE admin_id = %s", (admin_id,))
    admin_data = cursor.fetchone()

    if not admin_data:
        return redirect(url_for('admin.login'))

    return render_template('admin_profile.html', admin=admin_data, msg=msg, err=err)