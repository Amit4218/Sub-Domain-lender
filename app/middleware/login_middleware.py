from functools import wraps

from flask import redirect, session, url_for


def isLoggedIn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        email = session.get("email")

        if not user_id or not email:
            return redirect(url_for("login"))

        return func(*args, **kwargs)

    return wrapper
