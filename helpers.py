from flask import redirect, render_template, request, session
from functools import wraps
import hashlib

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def hashit(password, key):
    salt = key
    print("Hello this is helper")
    print(salt)
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
