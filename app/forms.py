from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, DataRequired, Length
from app.models import *


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    verification_code = StringField('Verification_code', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_verification_code(self, verification_code):
        user = User.query.filter_by(verification_code=verification_code.data).first()
        if user is None:
            raise ValidationError('Verification code not found')
        else:
            if user.email is not None:
                raise ValidationError('This verification code has been used for registration with another email')

    # def validate_email_and_verification_code(self, verification_code, email):
    #     user = User.query.filter(User.verification_code == verification_code.data, User.email != email.data).first()
    #     if user is not None:
    #         raise ValidationError('This verification code has been used for registration with another email')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AddUserForm(FlaskForm):
    last_name = StringField('Last Name', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name', validators=[DataRequired()])
    type = SelectField('User type', choices=[('teacher', 'Teacher'), ('student', 'Student')])
    group = StringField('Group number(for students)')
    year_admission = StringField('Year Admission(for students)')
    degree = SelectField('Degree(for students)',
                         choices=[('', ''), ('bachelor', 'Bachelor'), ('specialist', 'Specialist'), ('master', 'Master')], default='')
    form = SelectField('Form(for students)',
                       choices=[('', ''), ('fulltime', 'Fulltime'), ('distance', 'Distance'), ('evening', 'Evening')], default='')
    basis = SelectField('Basis(for students)', choices=[('', ''), ('budget', 'Budget'), ('contract', 'Contract')], default='')
    submit = SubmitField('Register')

    def validate_group(self, group):
        group = Group.query.filter_by(id=group.data).first()
        if group is None:
            raise ValidationError('There is no such group. Please use a different group number. ')


class AddGroupForm(FlaskForm):
    id = StringField('Group number', validators=[DataRequired()])
    name = StringField('Group number', validators=[DataRequired()])
    faculty = StringField('Faculty', validators=[DataRequired()])
    course_number = StringField('Course number', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_id(self, id):
        group = Group.query.filter_by(id=id.data).first()
        if group is not None:
            raise ValidationError('Please use a different group number.')

class AddCourseForm(FlaskForm):
    name = StringField('Course name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Register')
