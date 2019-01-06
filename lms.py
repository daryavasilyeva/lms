from app import app, db
from app.models import User, Student, Teacher, Group, Course, Materials, Homework, Homework_parcel

app.run(debug = True)