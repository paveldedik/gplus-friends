# -*- coding: utf-8 -*-

"""
Application Views
=================
"""

from flask import render_template, flash, url_for, redirect, session

from gplusfriends import app, google
from gplusfriends.tasks import get_person_data
from gplusfriends.resources import get_access_token


@app.route('/')
def index():
    """Homepage of the application.
    :return: HTML document.
    """
    token = get_access_token()
    if token is None:
        return render_template('loggedout.html')
    else:
        return render_template('loggedin.html')


@app.route('/person/<string:pid>')
def person(pid):
    person = get_person_data(pid)
    if person is None:
        return redirect(url_for('index'))
    else:
        return render_template('loggedin.html', person=person)


@app.route('/login')
def login():
    """Login view which authorizes the user through the Google+ API
    :return: Google authorization routine.
    """
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route('/logout')
def logout():
    """View that logouts the logged user.
    :return: Redirection to the index.
    """
    session.pop('access_token', None)
    flash('You were successfully logged out.', 'info')
    return redirect(url_for('index'))


@app.route(app.config['REDIRECT_URI'])
@google.authorized_handler
def authorized(resp):
    """URI where the Google API redirects the user after successful login.
    :return: Redirection to the index.
    """
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    flash('You were successfully logged in.', 'info')
    return redirect(url_for('index'))
