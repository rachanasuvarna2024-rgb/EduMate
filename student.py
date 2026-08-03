from flask import Blueprint, render_template
from session_utils import role_required

# ---------------------------------
# STUDENT BLUEPRINT
# ---------------------------------
student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/student"
)

# ---------------------------------
# STUDENT DASHBOARD
# ---------------------------------
@student_bp.route("/")
def student_home():

    check = role_required("Student")
    if check:
        return check

    return render_template("student_home.html")


# ---------------------------------
# AVAILABLE TESTS
# ---------------------------------
@student_bp.route("/available_tests")
def available_tests():

    check = role_required("Student")
    if check:
        return check

    return "Available Tests Page"


# ---------------------------------
# TEST HISTORY
# ---------------------------------
@student_bp.route("/test_history")
def test_history():

    check = role_required("Student")
    if check:
        return check

    return "Test History Page"


# ---------------------------------
# MY RESULTS
# ---------------------------------
@student_bp.route("/my_results")
def my_results():

    check = role_required("Student")
    if check:
        return check

    return "My Results Page"


# ---------------------------------
# MY PROGRESS
# ---------------------------------
@student_bp.route("/my_progress")
def my_progress():

    check = role_required("Student")
    if check:
        return check

    return "My Progress Page"


# ---------------------------------
# STUDENT PROFILE
# ---------------------------------
@student_bp.route("/student_profile")
def student_profile():

    check = role_required("Student")
    if check:
        return check

    return "Student Profile Page"