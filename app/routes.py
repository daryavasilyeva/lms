from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app
from app.forms import *
from app.models import *
from app import db
import random


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title='Home Page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(verification_code=form.verification_code.data).first()
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<email>')
@login_required
def user(email):
    user = User.query.filter_by(email=email).first_or_404()
    return render_template('user.html', user=user)


# @app.route('/edit_profile', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
#     form = EditProfileForm()
#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         db.session.commit()
#         flash('Your changes have been saved.')
#         return redirect(url_for('edit_profile'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#     return render_template('edit_profile.html', title='Edit Profile', form=form)

def get_code():
    Big_S = list('QWERTYUIOPASDFGHJKLZXCVBNM')
    Low_S = list('qwertyuiopasdfghjklzxcvbnm')
    Num_S = list('1234567890')
    Pass = ""
    for i in range(4):
        n = random.randrange(len(Big_S))
        Pass = Pass + Big_S[n]
        n = random.randrange(len(Low_S))
        Pass = Pass + Low_S[n]
        n = random.randrange(len(Num_S))
        Pass = Pass + Num_S[n]
    random.shuffle(list(Pass))
    return str(Pass)


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddUserForm()
    verification_code = get_code()
    code = User.query.filter_by(verification_code=verification_code).first()
    while code is not None:
        verification_code = get_code()
        code = User.query.filter_by(verification_code=verification_code).first()

    if form.validate_on_submit():
        if current_user.role != role_enum.admin:
            flash('No permission')
            return redirect(url_for('index'))
        if form.type.data == 'teacher':
            teacher = Teacher(verification_code=verification_code,
                        last_name=form.last_name.data,
                        first_name=form.first_name.data,
                        middle_name=form.middle_name.data,
                        role='teacher')
            db.session.add(teacher)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
        else:
            student = Student(verification_code=verification_code,
                        last_name=form.last_name.data,
                        first_name=form.first_name.data,
                        middle_name=form.middle_name.data,
                        role='student',
                        group_id=form.group.data,
                        year_admission=form.year_admission.data,
                        degree=form.degree.data,
                        form=form.form.data,
                        basis=form.basis.data)
            db.session.add(student)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('add_user.html', title='Add new user', form=form, verification_code=verification_code)
