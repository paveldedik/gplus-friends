# -*- coding: utf-8 -*-


from flask import render_template, url_for, redirect, session

from gplusfriends import app, google
from gplusfriends.tasks import process_data


@app.route('/')
def index():
    access_token = get_access_token()

    if access_token is None:
        return render_template('index.html')

    return process_data(access_token[0])


# ----------------------- AUTHENTICATION ENDPOINTS -------------------------


@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return 'You were signed out'


@app.route(app.config['REDIRECT_URI'])
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')
