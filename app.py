<<<<<<< HEAD
from my_calendar import app
from flask import Flask, render_template
from datetime import timedelta
app1 =Flask(__name__)


if __name__ == '__main__':

=======
from my_calendar import create_app


if __name__ == '__main__':
    app = create_app()
>>>>>>> 90c303a9546b9d11a1bd47711576280ce4fe219c
    app.run(debug=True)


# test code
# from my_calendar import create_app
# from my_calendar.database import db
# from my_calendar.modules import User, Event, Tag
# from datetime import datetime
# app = create_app()
# app.app_context().push()
#
# user = User.create('jason@xua', '12345')
# db.session.add(user)
# db.session.commit()
# event = Event.create('dinner', datetime(2018, 9, 10))
# event = Event.create('dinner', datetime(2018, 9, 11))