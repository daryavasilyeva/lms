from app import app, db
from app.models import User, Student, Teacher, Group, Course

app.run(debug = True)