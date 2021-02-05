from app import db
from app.helpers.decorators import login_required
from app.models import User
from app.models.user_dict import UserDict
from app.modules.user.forms import ChangePasswordForm, LoginForm, RegisterForm
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)

module = Blueprint('user', __name__, url_prefix='/user')


@module.route('/', methods=['GET'])
def index():
    return redirect(url_for('user.dashboard'))


@module.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.username == form.username.data).first()

        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash("You have logged successfully", 'success')
            return redirect(url_for('user.dashboard'))

        flash("Username or password is incorrect", 'error')
    return render_template('user/login.html', form=form)


@module.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.username == form.username.data).first()

        if user:
            flash("Username is already taken", 'error')
            return render_template('user/register.html', form=form)

        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You have been successfully registered", 'success')
        return redirect(url_for('user.login'))

    return render_template('user/register.html', form=form)


@module.route('/logout', methods=['GET'])
@login_required
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('user.login'))


@module.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.username == g.user.username).first()

        if not user.check_password(form.password.data):
            flash("Please type last password correctly.")
            return render_template('user/change_password.html', form=form)

        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password changed successfully')
        return redirect(url_for('user.dashboard'))

    return render_template('user/change_password.html', form=form)


@module.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    context = dict()
    context['words'] = UserDict.query.filter_by(user_id=g.user.id)
    return render_template('user/dashboard.html', content=context)
