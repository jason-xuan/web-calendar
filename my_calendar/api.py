from flask.blueprints import Blueprint
from flask import session, g, request, Response
from sqlalchemy import and_, extract
from .database import db
from .modules import User, Event, Tag
from .utils import need_login, error_msg, json_response, check_fields


bp_api = Blueprint('api', __name__, url_prefix='/api')


@bp_api.before_app_request
def load_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(user_id=user_id).first()


@bp_api.route('/users/login/', methods=['POST'])
@check_fields('email', 'password')
def login():
    content = request.json
    email, password = content['email'], content['password']
    # input validation
    user = User.query.filter_by(email=email).first()
    if user is None:
        return error_msg(404, 'user not exist')
    if not user.verify(password):
        return error_msg(403, 'wrong password')
    session['user_id'] = user.user_id
    return json_response({
        'code': 200,
        'msg': 'successfully login'
    })


@bp_api.route('/users/register/', methods=['POST'])
@check_fields('email', 'password')
def register():
    content = request.json
    email, password = content['email'], content['password']
    # check if exist same user
    if User.query.filter_by(email=email).first() is not None:
        return error_msg(403, 'user already exist')
    user = User.create(email, password)
    db.session.add(user)
    db.session.commit()
    return json_response({
        'code': 201,
        'email': user.email
    })


@bp_api.route('/users/logout', methods=['GET'])
@need_login
def logout():
    session.clear()
    return json_response({
        'code': 200,
        'msg': 'successfully logout'
    })


@bp_api.route('/events/user/', methods=['POST'])
@need_login
@check_fields('year', 'month')
def get_user_events():
    content = request.json
    year, month = int(content['year']), int(content['month'])
    events = Event.query.with_parent(g.user).filter(and_(
        extract('year', Event.event_time) == year,
        extract('month', Event.event_time) == month,
    )).all()
    return json_response({
        'code': 200,
        'events': [event.to_dict() for event in events]
    })


@bp_api.route('/events/create', methods=['POST'])
@need_login
@check_fields('event_name', 'event_time')
def get_event():
    content = request.json
    event_name, event_time = content['event_name'], content['event_time']
    event = Event.create(event_name, event_time)
    g.user.events.append(event)
    db.session.commit()
    return json_response({
        'code': 201,
        'msg': f'{event_name} create successfully'
    })
