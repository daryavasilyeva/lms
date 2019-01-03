import enum
from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


group_x_course = db.Table('group_x_course',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

teacher_x_course = db.Table('teacher_x_course',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

monitor_x_course = db.Table('monitor_x_course',
    db.Column('monitor_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)


class role_enum(enum.Enum):
    admin = 'админимратор'
    teacher = 'преподаватель'
    student = 'студент'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum(role_enum))
    verification_code = db.Column(db.String(120), index=True, unique=True)
    last_name = db.Column(db.String(64), index=True)
    first_name = db.Column(db.String(64), index=True)
    middle_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone_number = db.Column(db.String(12))
    city = db.Column(db.String(64))
    about_me = db.Column(db.String(140))
    vk_link = db.Column(db.String(64))
    facebook_link = db.Column(db.String(64))
    linkedin_link = db.Column(db.String(64))
    instagram_link = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.last_name + self.first_name + self.middle_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }


class degree_enum(enum.Enum):
    bachelor = 'бакалавр'
    specialist = 'специалист'
    master = 'магистр'


class form_enum(enum.Enum):
    fulltime = 'очная'
    distance = 'заочная'
    evening = 'вечерняя'


class basis_enum(enum.Enum):
    budget = 'бюджетная'
    contract = 'контрактная'


class Student(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    year_admission = db.Column(db.Integer)
    degree = db.Column(db.Enum(degree_enum))
    form = db.Column(db.Enum(form_enum))
    basis = db.Column(db.Enum(basis_enum))
    courses = db.relationship('Course', secondary=monitor_x_course, lazy='dynamic',
                              backref=db.backref('monitors', lazy=True))

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }


class Teacher(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    courses = db.relationship('Course', secondary=teacher_x_course, lazy='dynamic',
        backref=db.backref('teachers', lazy=True))

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    faculty = db.Column(db.String(64))
    course_number = db.Column(db.Integer)
    students = db.relationship('Student', backref='student', lazy=True)
    courses = db.relationship('Course', secondary=group_x_course, lazy='dynamic',
        backref=db.backref('groups', lazy=True))


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(200))
    groups = db.relationship('Group', secondary=group_x_course, lazy='dynamic',
        backref=db.backref('courses', lazy=True))
    teachers = db.relationship('Teacher', secondary=teacher_x_course, lazy='dynamic',
        backref=db.backref('courses', lazy=True))
    monitors = db.relationship('Student', secondary=group_x_course, lazy='dynamic',
        backref=db.backref('courses', lazy=True))

class Materials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    name = db.Column(db.String(64))
    description = db.Column(db.String(200))
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    name = db.Column(db.String(64))
    description = db.Column(db.String(200))
    start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class Homework_parcel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'), primary_key=True)
    send_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    text = db.Column(db.String(200))