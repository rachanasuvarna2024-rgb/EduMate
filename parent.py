from flask import Blueprint, render_template
from session_utils import role_required

# ---------------------------------
# PARENT BLUEPRINT
# ---------------------------------
parent_bp = Blueprint(
    "parent",
    __name__,
    url_prefix="/parent"
)

# ---------------------------------
# PARENT DASHBOARD
# ---------------------------------
@parent_bp.route("/")
def parent_home():

    check = role_required("Parent")
    if check:
        return check

    return render_template("parent_home.html")


# ---------------------------------
# CHILD PROFILE
# ---------------------------------
@parent_bp.route("/child_profile")
def child_profile():

    check = role_required("Parent")
    if check:
        return check

    return "Child Profile Page"


# ---------------------------------
# CHILD RESULTS
# ---------------------------------
@parent_bp.route("/child_results")
def child_results():

    check = role_required("Parent")
    if check:
        return check

    return "Child Results Page"


# ---------------------------------
# CHILD PROGRESS
# ---------------------------------
@parent_bp.route("/child_progress")
def child_progress():

    check = role_required("Parent")
    if check:
        return check

    return "Child Progress Page"


# ---------------------------------
# PARENT PROFILE
# ---------------------------------
@parent_bp.route("/parent_profile")
def parent_profile():

    check = role_required("Parent")
    if check:
        return check

    return "Parent Profile Page"