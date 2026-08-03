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
    "Admin": ("admin", "admin_id"),
    "Teacher": ("teacher", "teacher_id"),
    "Student": ("student", "student_id"),
    "Parent": ("parent", "parent_id")
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

    if role not in ROLE_MAP:
        return render_template(
            "login.html",
            error="Invalid role selected."
        )

    table, id_column = ROLE_MAP[role]

    query = f"""
        SELECT *
        FROM {table}
        WHERE email=%s
        AND password=%s
    """

    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:

        # Create Session
        session["role"] = role
        session["user_id"] = user[id_column]
        session["user_name"] = user["name"]

        # Store Login History
        ip_address = request.remote_addr
        device_info = request.user_agent.string

        cursor.execute("""
            INSERT INTO login_history
            (
                user_role,
                user_id,
                ip_address,
                device_info
            )
            VALUES (%s,%s,%s,%s)
        """,
        (
            role,
            user[id_column],
            ip_address,
            device_info
        ))

        conn.commit()

        # Redirect according to role
        if role == "Admin":
            return redirect(url_for("admin.admin_home"))

        elif role == "Teacher":
            return redirect(url_for("teacher.teacher_home"))

        elif role == "Student":
            return redirect(url_for("student.student_home"))

        else:
            return redirect(url_for("parent.parent_home"))

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

    return redirect(url_for("auth.login_page"))


# ---------------------------------
# CACHE PROTECTION
# ---------------------------------
@auth_bp.after_request
def add_header(response):

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response