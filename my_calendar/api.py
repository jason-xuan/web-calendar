from flask.blueprints import Blueprint
from flask import session, g, request, Response
from .modules import User, Event, Tag
from .utils import need_login, error_msg, json_response
from .db import db_session


bp_api = Blueprint('api', __name__, url_prefix='/api')


@bp_api.before_app_request
def load_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db_session.query(User).filter(User.user_id == user_id).one()


@bp_api.route('/users/login/', methods=['POST'])
def login():
    content = request.json
    if 'email' not in content or 'password' not in content:
        return error_msg(403, 'fields not complete')
    email, password = content['email'], content['password']
    # input validation
    if db_session.query(User).filter(User.email == email).count() == 0:
        return error_msg(404, 'user not exist')
    user = db_session.query(User).filter(User.email == email).one()
    if not user.verify(password):
        return error_msg(403, 'wrong password')
    session['user_id'] = user.user_id
    return json_response({
        'code': 200,
        'msg': 'successfully login'
    })


@bp_api.route('/users/register/', methods=['POST'])
def register():
    content = request.json
    if content is None:
        return error_msg(403, 'post type must be json')
    if 'email' not in content or 'password' not in content:
        return error_msg(403, 'fields not complete')
    email, password = content['email'], content['password']
    # check if exist same user
    if db_session.query(User).filter(User.email == email).count() != 0:
        return error_msg(403, 'user already exist')
    user = User(email, password)
    db_session.add(user)
    db_session.commit()
    return json_response({
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


@bp_api.route('/events/user/<string:user_id>', methods=['GET'])
@need_login
def get_user_events(user_id):
    pass


@bp_api.route('/events/<string:event_id>', methods=['GET'])
@need_login
def get_event(event_id):
    pass
