import os
import flask_login
from flask import Blueprint, abort, request, session, Flask
from sqlalchemy import create_engine
from api_views import *
from models import User
import json
from json import JSONDecodeError
from status import *
from werkzeug.security import check_password_hash
from sqlalchemy.orm import sessionmaker
from back_end import get_result
import re
import codecs
from utils import save_thumbnail
from models import Prediction
import cv2

api = Blueprint("api", __name__)
engine = create_engine('sqlite:///asar.db', echo=True)
Session = sessionmaker(bind=engine)
s = Session()
login_manager = flask_login.LoginManager()
app = Flask(__name__)
app.secret_key = 'SUPER SCRET KEY FOR ASSAR PROJECT'
app.config['SESSION_TYPE'] = 'filesystem'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    '''Load a user from the database using a user_id.

    Args:
        username: The username of the user to be found.

    Returns:
        res: The user where user.user_id == user_id.
    '''
    res = s.query(User).filter(User.username == username).first()
    s.close()
    return res


@api.route('/auth/register', methods=['POST'])
def api_user_register():
    '''
    Register new user from API
    ---
    post:
      parameters:
      - in: body
        name: register
        schema: RegisterSchema
        description: Register DTO model
      responses:
        200:
          content:
            application/json:
              schema: BasicSchema
        400:
          content:
            application/json:
              schema: BasicSchema
    '''
    try:
        data_dict = json.loads(request.data.decode('utf-8'))
    except JSONDecodeError:
        return 'Malformed request', HTTP_400_BAD_REQUEST
    try:
        username = data_dict['username']
        password = data_dict['password']
        confirm_password = data_dict['confirm_password']
        res = s.query(User).filter(User.username.in_([username])).first()
        if res == None:
            if password == confirm_password:
                user = User(username, password)
                s.add(user)
                s.commit()
                session['logged_in'] = True
                session['user'] = username
                user = load_user(username)
                if not os.path.exists('static/users/{}'.format(user.username)):
                    os.makedirs('static/users/{}'.format(user.username))
                flask_login.login_user(user)
                s.close()
                return 'Success', HTTP_200_OK
            else:
                return 'Password not match the confirm password', HTTP_400_BAD_REQUEST
        else:
            return 'Username already in use', HTTP_400_BAD_REQUEST
    except KeyError:
        return 'Malformed request', HTTP_400_BAD_REQUEST


@api.route('/auth/login', methods=['POST'])
def api_user_login():
    '''
    Register new user from API
    ---
    post:
      parameters:
      - in: body
        name: login
        schema: LoginSchema
        description: Login DTO model
      responses:
        200:
          content:
            application/json:
              schema: BasicSchema
        400:
          content:
            application/json:
              schema: BasicSchema
        403:
          content:
            application/json:
              schema: BasicSchema
    '''
    try:
        data_dict = json.loads(request.data.decode('utf-8'))
    except JSONDecodeError:
        return 'Malformed request', 400
    try:
        username = data_dict['username']
        password = data_dict['password']
        result = s.query(User).filter(User.username.in_([password])).first()
        if result:
            if check_password_hash(result.password, password):
                session['logged_in'] = True
                session['user'] = username
                user = load_user(password)
                flask_login.login_user(user)
                s.close()
                return 'Success', 200
            else:
                abort(HTTP_403_FORBIDDEN, 'Incorrect username or password!')
    except KeyError:
        return 'Malformed request', HTTP_400_BAD_REQUEST


@api.route('/auth/logout', methods=['POST'])
@flask_login.login_required
def api_user_logout():
    '''
    Register new user from API
    ---
    post:
      responses:
        200:
          content:
            application/json:
              schema: BasicSchema
    '''
    flask_login.logout_user()
    session['logged_in'] = False
    session['user'] = ''
    return 'Success', 200

@api.route('/predict', methods=['POST'])
@flask_login.login_required
def api_predict():
    ''' Makes a prediciton from an image send from the application.

    The method retrieves the image, converts it to a usable format, makes a
    prediciton, then saves it if the user is not a guest.

    ---
    post:
      parameters:
      - in: body
        name: image
        schema: PredictSchema
        description: image format should be base64 image, for example in body {'image' 'data:image/png;base64,.....'}
      responses:
        200:
          content:
            application/json:
              schema: BasicSchema
        400:
          content:
            application/json:
              schema: BasicSchema
    '''
    try:
        data_dict = json.loads(request.data.decode('utf-8'))
    except JSONDecodeError:
        return 'Malformed request', HTTP_400_BAD_REQUEST
    path = 'static/users/{}'.format(session['user'])
    if not os.path.exists(path):
        os.makedirs(path)
    img_data = data_dict['image']
    img_data = bytearray(img_data.encode('utf-8'))
    convertImage(img_data, path)
    result = str(get_result(path + '/temp.png'))
    if session['user'] != 'guest':
        save_pred(result)

    return result, HTTP_200_OK

@api.route('/')
@flask_login.login_required
def api_home():
    ''' The home naviagion option.

    If a user is not logged in, show Login screen.
    else show the Home.
    ---
    get:
      parameters:
      - in: path
        name: test
        required: true
        type: string
        description: test description in Markdown.
      - in: query
        name: test
        type: string
        description: test description in Markdown.
      responses:
        200:
          content:
            application/json:
              schema: BasicSchema
        201:
          content:
            application/json:
              schema: BasicSchema
    '''
    return 'hello world'

# Decoding an image from base64 into raw representation
def convertImage(imgData1, path):
    '''Decodes an image from base64.

    Args:
        imgData1: The image to be decoded
        path: The location the decoded image is saved
    '''
    img_str = re.search(b'base64,(.*)', imgData1).group(1)
    with open(path + '/temp.png', 'wb') as output:
        output.write(codecs.decode(img_str, 'base64'))


def save_pred(result):
    '''Saves the prediction to the users file.

    Args:
        result: the result of the prediction
    '''
    save_loc = save_thumbnail(session['user'], cv2.imread('static/users/{}/temp.png'.format(session['user'])))
    os.remove('static/users/{}/temp.png'.format(session['user']))
    create_prediction(save_loc, result)

def create_prediction(loc, result):
    '''creates the prediction entry in the database.

    Args:
        loc: the location of the image
        result: the prediciton result
    '''
    user = load_user(session['user'])
    res = s.query(User.id).filter(User.username == user.username)
    for r in res:
        identity = r.id
    pred = Prediction(identity, loc, result)
    s.add(pred)
    s.commit()
    s.close()