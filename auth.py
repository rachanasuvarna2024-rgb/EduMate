from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from db import conn, cursor


# ---------------------------------
# AUTH BLUEPRINT
# ---------------------------------
auth_bp = Blueprint("auth", __name__)


# ---------------------------------
# ROLE TO TABLE MAPPING
# ---------------------------------
ROLE_MAP = {
    "Admin": ("admin", "admin_id", "admin_name"),
    "Teacher": ("teacher", "teacher_id", "teacher_name"),
    "Student": ("student", "student_id", "student_name"),
    "Parent": ("parent", "parent_id", "parent_name")
}


# ---------------------------------
# LOGIN PAGE
# ---------------------------------
@auth_bp.route("/")
def login_page():

    if "role" in session:

        if session["role"] == "Admin":
            return redirect(url_for("admin.admin_home"))

        elif session["role"] == "Teacher":
            return redirect(url_for("teacher.teacher_home"))

        elif session["role"] == "Student":
            return redirect(url_for("student.student_home"))

        elif session["role"] == "Parent":
            return redirect(url_for("parent.parent_home"))

    return render_template("login.html")


# ---------------------------------
# LOGIN PROCESS
# ---------------------------------
@auth_bp.route("/login", methods=["POST"])
def process_login():

    role = request.form["role"]
    username = request.form["username"]
    password = request.form["password"]

    # Validate role
    if role not in ROLE_MAP:

        return render_template(
            "login.html",
            error="Invalid role selected."
        )

    table, id_column, name_column = ROLE_MAP[role]


    # ---------------------------------
    # FETCH USER
    # ---------------------------------
    # The actual database tables have:
    #
    # admin    -> admin_name
    # teacher  -> teacher_name
    # student  -> student_name
    # parent   -> parent_name
    #
    # We alias the appropriate column as "name"
    # so the rest of the application can use
    # user["name"] consistently.
    # ---------------------------------

    query = f"""
        SELECT
            *,
            {name_column} AS name
        FROM {table}
        WHERE email = %s
        AND password = %s
    """

    cursor.execute(
        query,
        (username, password)
    )

    user = cursor.fetchone()


    # ---------------------------------
    # USER FOUND
    # ---------------------------------
    if user:

        # ---------------------------------
        # CREATE SESSION
        # ---------------------------------

        session["role"] = role
        session["user_id"] = user[id_column]
        session["user_name"] = user["name"]


        # ---------------------------------
        # STORE LOGIN HISTORY
        # ---------------------------------

        ip_address = request.remote_addr

        cursor.execute("""
            INSERT INTO login_history
            (
                user_role,
                user_id,
                ip_address
            )
            VALUES (%s, %s, %s)
        """,
        (
            role,
            user[id_column],
            ip_address
        ))


        conn.commit()


        # ---------------------------------
        # REDIRECT ACCORDING TO ROLE
        # ---------------------------------

        if role == "Admin":

            return redirect(
                url_for("admin.admin_home")
            )

        elif role == "Teacher":

            return redirect(
                url_for("teacher.teacher_home")
            )

        elif role == "Student":

            return redirect(
                url_for("student.student_home")
            )

        else:

            return redirect(
                url_for("parent.parent_home")
            )


    # ---------------------------------
    # INVALID LOGIN
    # ---------------------------------

    return render_template(
        "login.html",
        error="Invalid Email or Password"
    )


# ---------------------------------
# LOGOUT
# ---------------------------------
@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("auth.login_page")
    )


# ---------------------------------
# CACHE PROTECTION
# ---------------------------------
@auth_bp.after_request
def add_header(response):

    response.headers["Cache-Control"] = (
        "no-cache, no-store, must-revalidate"
    )

    response.headers["Pragma"] = "no-cache"

    response.headers["Expires"] = "0"

    return response