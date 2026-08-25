from functools import wraps
from flask import session, redirect, url_for

def login_required():
    if "role" not in session:
        return redirect(url_for("auth.login_page"))
    return None

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "role" not in session:
                return redirect(url_for("auth.login_page"))
            if session.get("role") != required_role:
                return redirect(url_for("auth.login_page"))
            return func(*args, **kwargs)
        return wrapper
    return decorator