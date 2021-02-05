from flask import (Blueprint, redirect, url_for)

module = Blueprint('default', __name__)


@module.route('/', methods=['GET'])
def index():
    return redirect(url_for('user.dashboard'))

