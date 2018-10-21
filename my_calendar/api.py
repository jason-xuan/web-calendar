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
@check_fields(('email', str), ('password', str))
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
@check_fields(('email', str), ('password', str))
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


@bp_api.route('/events/user', methods=['POST'])
@need_login
@check_fields(('year', int), ('month', int))
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
@check_fields(('event_name', str), ('event_time', str))
def get_create():
    content = request.json
    event_name, event_time = content['event_name'], content['event_time']
    event = Event.create(event_name, event_time)
    g.user.events.append(event)
    db.session.commit()
    return json_response({
        'code': 201,
        'msg': f'{event_name} create successfully'
    })


@bp_api.route('/events/update', methods=['POST'])
@need_login
@check_fields(('event_id', str), ('update_fields', dict))
def update_events():
    content = request.json
    event_id, update_fields = content['event_id'], content['update_fields']
    event = Event.query.filter_by(event_id=event_id).first()
    if 'event_name' in update_fields:
        event.event_name = update_fields['event_name']
    elif 'event_time' in update_fields:
        event.event_name = update_fields['event_name']
    else:
        return error_msg(403, 'fields not complete')
    db.session.commit()
    return json_response({
        'code': 200,
    })


@bp_api.route('/events/delete', methods=['POST'])
@need_login
@check_fields(('event_id', str))
def delete_event():
    content = request.json
    event_id = content['event_id']
    event = Event.query.filter_by(event_id=event_id).first()
    db.session.delete(event)
    db.session.commit()
    return json_response({
        'code': 200
    })
