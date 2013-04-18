# -*- coding: utf-8 -*-

import requests
from flask import render_template, redirect, url_for, session

from gplusfriends import app, google


@app.route('/')
def index():
    access_token = get_access_token()

    if access_token is None:
        return render_template('index.jinja')

    headers = {'Authorization': 'Bearer ' + access_token[0]}

    return google.get('people/me', headers=headers).raw_data


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
