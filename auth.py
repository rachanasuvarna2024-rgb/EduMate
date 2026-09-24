from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from db import conn, cursor, get_db_connection
from session_utils import role_required


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
# COMMON PROFILE
# ---------------------------------
@auth_bp.route("/profile")
def profile():

    role = session.get("role")
    user_id = session.get("user_id")

    if not role or not user_id:
        return redirect(url_for("auth.login_page"))

    conn_local = None
    cursor_local = None
    user = None

    try:

        conn_local = get_db_connection()
        cursor_local = conn_local.cursor(dictionary=True)

        # ---------------------------------
        # ADMIN
        # ---------------------------------
        if role == "Admin":

            cursor_local.execute("""
                SELECT
                    admin_id AS user_id,
                    admin_name AS name,
                    email,
                    NULL AS phone,
                    NULL AS institution_name,
                    NULL AS department_name,
                    NULL AS designation_name,
                    NULL AS standard_name,
                    status
                FROM admin
                WHERE admin_id = %s
            """, (user_id,))

            user = cursor_local.fetchone()


        # ---------------------------------
        # TEACHER
        # ---------------------------------
        elif role == "Teacher":

            cursor_local.execute("""
                SELECT
                    t.teacher_id AS user_id,
                    t.teacher_name AS name,
                    t.email,
                    t.phone,
                    i.institution_name,
                    d.department_name,
                    dg.designation_name,
                    NULL AS standard_name,
                    t.status
                FROM teacher t

                LEFT JOIN institution i
                    ON i.institution_id = t.institution_id

                LEFT JOIN department_master d
                    ON d.department_id = t.department_id

                LEFT JOIN designation_master dg
                    ON dg.designation_id = t.designation_id

                WHERE t.teacher_id = %s
            """, (user_id,))

            user = cursor_local.fetchone()


        # ---------------------------------
        # STUDENT
        # ---------------------------------
        elif role == "Student":

            cursor_local.execute("""
                SELECT
                    s.student_id AS user_id,
                    s.student_name AS name,
                    s.email,
                    s.phone,
                    i.institution_name,
                    NULL AS department_name,
                    NULL AS designation_name,
                    st.standard_name,
                    s.status
                FROM student s

                LEFT JOIN institution i
                    ON i.institution_id = s.institution_id

                LEFT JOIN standard st
                    ON st.standard_id = s.standard_id

                WHERE s.student_id = %s
            """, (user_id,))

            user = cursor_local.fetchone()


        # ---------------------------------
        # PARENT
        # ---------------------------------
        elif role == "Parent":

            cursor_local.execute("""
                SELECT
                    p.parent_id AS user_id,
                    p.parent_name AS name,
                    p.email,
                    p.phone,
                    i.institution_name,
                    NULL AS department_name,
                    NULL AS designation_name,
                    NULL AS standard_name,
                    p.status
                FROM parent p

                LEFT JOIN institution i
                    ON i.institution_id = p.institution_id

                WHERE p.parent_id = %s
            """, (user_id,))

            user = cursor_local.fetchone()


        if not user:

            flash(
                "Unable to load profile.",
                "error"
            )

            return redirect(
                url_for("auth.login_page")
            )

        return render_template(
            "profile.html",
            user=user,
            role=role
        )

    except Exception as e:

        print("\n========== PROFILE ERROR ==========")
        print(e)
        print("===================================\n")

        flash(
            "Unable to load profile.",
            "error"
        )

        # Redirect back to the appropriate dashboard
        if role == "Admin":
            return redirect(url_for("admin.admin_home"))

        elif role == "Teacher":
            return redirect(url_for("teacher.teacher_home"))

        elif role == "Student":
            return redirect(url_for("student.student_home"))

        elif role == "Parent":
            return redirect(url_for("parent.parent_home"))

        return redirect(url_for("auth.login_page"))

    finally:

        if cursor_local:
            cursor_local.close()

        if conn_local:
            conn_local.close()

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