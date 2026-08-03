from flask import Blueprint, render_template
from session_utils import role_required

# ---------------------------------
# TEACHER BLUEPRINT
# ---------------------------------
teacher_bp = Blueprint(
    "teacher",
    __name__,
    url_prefix="/teacher"
)

# ---------------------------------
# TEACHER DASHBOARD
# ---------------------------------
@teacher_bp.route("/")
def teacher_home():

    check = role_required("Teacher")
    if check:
        return check

    return render_template("teacher_home.html")


# ---------------------------------
# QUESTION BANK
# ---------------------------------
@teacher_bp.route("/add_question")
def add_question():

    check = role_required("Teacher")
    if check:
        return check

    return "Add Question Page"


@teacher_bp.route("/view_questions")
def view_questions():

    check = role_required("Teacher")
    if check:
        return check

    return "View Questions Page"


# ---------------------------------
# TEST MANAGEMENT
# ---------------------------------
@teacher_bp.route("/create_test")
def create_test():

    check = role_required("Teacher")
    if check:
        return check

    return "Create Test Page"


@teacher_bp.route("/view_tests")
def view_tests():

    check = role_required("Teacher")
    if check:
        return check

    return "View Tests Page"


@teacher_bp.route("/view_results")
def view_results():

    check = role_required("Teacher")
    if check:
        return check

    return "View Results Page"


# ---------------------------------
# STUDENT ANALYTICS
# ---------------------------------
@teacher_bp.route("/student_progress")
def student_progress():

    check = role_required("Teacher")
    if check:
        return check

    return "Student Progress Page"


# ---------------------------------
# PROFILE
# ---------------------------------
@teacher_bp.route("/teacher_profile")
def teacher_profile():

    check = role_required("Teacher")
    if check:
        return check

    return "Teacher Profile Page"