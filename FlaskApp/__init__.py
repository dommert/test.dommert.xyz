# API.Dommert.xyz
from app import app
from views import Routes
from models import *
from auth import *



if __name__ == "__main__":
    User.create_table(fail_silently=True)
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'], port=app.config['PORT'])



