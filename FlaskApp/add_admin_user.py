# Flask-Netpad Version 0.0.3
# admin_user.py

# Creates User table and Admin User

from app import app, db
from models import *
from auth import *


#auth.User.create_table(fail_silently=True) # make sure table created.
admin = User(username='admin', email='admin@email.com', admin=True, active=True)
admin.set_password('admin')
admin.save()
print('Admin Created! ... Have a nice day')