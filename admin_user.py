from app import app, db
from app.models import User, role_enum

u = User(email='dasha@mail.com', role=role_enum.admin)
u.set_password('cat')
db.session.add(u)
db.session.commit()
