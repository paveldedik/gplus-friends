# -*- coding: utf-8 -*-


__version__ = '0.0.1'


from flask import Flask
from flask_oauth import OAuth
from werkzeug.contrib.cache import SimpleCache


app = Flask(__name__)
app.config.from_object('gplusfriends.config')
app.secret_key = app.config['SECRET_KEY']


oauth = OAuth()
google = oauth.remote_app('google',
    base_url='https://www.googleapis.com/plus/v1/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/plus.login',
        'response_type': 'code'},
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key=app.config['GOOGLE_CLIENT_ID'],
    consumer_secret=app.config['GOOGLE_CLIENT_SECRET']
)

cache = SimpleCache()


from gplusfriends import views
