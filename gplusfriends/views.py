# -*- coding: utf-8 -*-

"""
Application views
=================
"""


from hashlib import md5
from flask import render_template, flash, url_for, redirect, session

from gplusfriends import app, google, cache
from gplusfriends.tasks import process_data


@app.route('/')
def index():
    """Homepage of the application."""
    token = get_access_token()
    if token is None:
        return render_template('loggedout.html')
    else:
        person = get_person_data(token[0])
        return render_template('loggedin.html', person=person)


# ----------------------- AUTHENTICATION ENDPOINTS -------------------------


@app.route('/login')
def login():
    """Login view which authorizes the user through the Google+ API"""
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route('/logout')
def logout():
    """View that logouts the logged user."""
    session.pop('access_token', None)
    flash('You were successfully logged out.', 'info')
    return redirect(url_for('index'))


@app.route(app.config['REDIRECT_URI'])
@google.authorized_handler
def authorized(resp):
    """URI where the Google API redirects the user after successful login."""
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    flash('You were successfully logged in.', 'info')
    return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
    """Returns user's access token."""
    return session.get('access_token')


def get_person_data(token):
    """Function that returnes cashed user's data."""
    token_hash = md5(token).hexdigest()
    data = cache.get(token_hash)
    if data is None:
        data = process_data(token)
        cache.set(token_hash, data, timeout=30 * 60) # 30 minutes
    return data
