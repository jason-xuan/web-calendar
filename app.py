from my_calendar import create_app


if __name__ == '__main__':
    app = create_app()
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