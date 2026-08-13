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
# ADD STANDARD
# ---------------------------------
@admin_bp.route("/add_standard", methods=["GET", "POST"])
def add_standard():

    check = role_required("Admin")
    if check:
        return check

    # ---------------------------------
    # DISPLAY FORM
    # ---------------------------------

    if request.method == "GET":
        return render_template("add_standard.html")


    # ---------------------------------
    # GET STANDARD NAME
    # ---------------------------------

    standard_name = request.form["standard_name"]


    # ---------------------------------
    # INSERT STANDARD INTO DATABASE
    # ---------------------------------

    try:

        query = """
            INSERT INTO standard
            (standard_name)
            VALUES (%s)
        """

        cursor.execute(query, (standard_name,))

        conn.commit()

        return render_template(
            "add_standard.html",
            message="Standard added successfully!"
        )


    except Exception as e:

        conn.rollback()

        return render_template(
            "add_standard.html",
            message="Error adding standard: " + str(e)
        )

# ---------------------------------
# ADD SUBJECT

@admin_bp.route("/add_subject")
def add_subject():

    check = role_required("Admin")
    if check:
        return check

    return render_template("add_subject.html")


@admin_bp.route("/add_chapter")
def add_chapter():

    check = role_required("Admin")
    if check:
        return check

    return render_template("add_chapter.html")


@admin_bp.route("/student_progress_for_admin")
def student_progress_for_admin():

    check = role_required("Admin")
    if check:
        return check

    return render_template("student_progress_for_admin.html")


@admin_bp.route("/admin_profile")
def admin_profile():

    check = role_required("Admin")
    if check:
        return check

    return "Admin Profile Page"