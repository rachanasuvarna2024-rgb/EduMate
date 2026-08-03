from flask import session, redirect, url_for

# ---------------------------------
# CHECK LOGIN
# ---------------------------------
def login_required():

    if "role" not in session:
        return redirect(url_for("auth.login_page"))

    return None


# ---------------------------------
# CHECK USER ROLE
# ---------------------------------
def role_required(required_role):

    if "role" not in session:
        return redirect(url_for("auth.login_page"))

    if session["role"] != required_role:
        return redirect(url_for("auth.login_page"))

    return None