import os
from app import app
from app.models import User, Todo, Sensors, db




# эти переменные доступны внутри оболочки без явного импорта


if __name__ == "__main__":
    app.run(debug=True)

# From Shell
# from app import db,app
# app.app_context().push()
# db.create_all()

# from cmd in the app's  folder:
# flask db init - This will add a migrations folder to your application. The contents of this folder need to be
# #added to version control along with your other source files.
# flask db migrate -m "Initial migration." - The migration script needs to be reviewed and edited, as Alembic is not
# #always able to detect every change you make to your models.
# flask db upgrade - Then you can apply the changes described by the migration script to your database