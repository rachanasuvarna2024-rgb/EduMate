from flask import Blueprint, render_template
from session_utils import role_required

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
@admin_bp.route("/add_teacher")
def add_teacher():

    check = role_required("Admin")
    if check:
        return check

    return "Add Teacher Page"


@admin_bp.route("/view_teachers")
def view_teachers():

    check = role_required("Admin")
    if check:
        return check

    return "View Teachers Page"


@admin_bp.route("/add_parent")
def add_parent():

    check = role_required("Admin")
    if check:
        return check

    return "Add Parent Page"


@admin_bp.route("/view_parents")
def view_parents():

    check = role_required("Admin")
    if check:
        return check

    return "View Parents Page"


@admin_bp.route("/add_standard")
def add_standard():

    check = role_required("Admin")
    if check:
        return check

    return render_template("add_standard.html")


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