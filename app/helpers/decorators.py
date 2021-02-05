from functools import wraps

from flask import g, redirect, request, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('user.login', next=request.url))

        return f(*args, **kwargs)

    return decorated_function
