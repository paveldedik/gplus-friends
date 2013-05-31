# -*- coding: utf-8 -*-

"""
Application Views
=================
"""

from flask import (render_template, flash, url_for, request,
                   redirect, session, abort)

from gplusfriends import app, google
from gplusfriends.resources import get_access_token
from gplusfriends.tasks import (get_person_data, get_activity_data,
                                get_person_xml, get_activity_xml)


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


@app.route('/people/<string:pid>')
def show_person(pid):
    """Endpoint that displays persons's friends, acquantances, followed pages
    and activities (which are notes the users have posted to their stream).
    :param pid: The Google+ ID of the person.
    :return: Rendered HTML template which displays person's information.
    """
    person = get_person_data(pid)
    if person is None:
        abort(401)
    elif request.args.get('format') == 'xml':
        return get_person_xml(person)
    else:
        return render_template('person.html', person=person)


@app.route('/activities/<string:aid>')
def show_activity(aid):
    """Endpoint that displays the specified activity.
    :param pid: The Google+ ID of the activity.
    :return: Rendered HTML template which displays activity's data.
    """
    activity = get_activity_data(aid)
    if activity is None:
        abort(401)
    elif request.args.get('format') == 'xml':
        return get_activity_xml(activity)
    else:
        return render_template('activity.html', activity=activity)


@app.route('/people', methods=['POST'])
def search_people():
    """Redirects the user to a person corresponding the inserted value."""
    person_id = request.form['person']
    return redirect(url_for('show_person', pid=person_id))


@app.route('/activities', methods=['POST'])
def search_activities():
    """Redirects the user to an activity corresponding the inserted value."""
    activity_id = request.form['activity']
    return redirect(url_for('show_activity', aid=activity_id))


@app.route('/login')
def login():
    """Login view which authorizes the user through the Google+ API
    :return: Google authorization routine.
    """
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route('/logout')
def logout():
    """View that logouts the logged user."""
    session.pop('access_token', None)
    flash('You were successfully logged out.', 'info')
    return redirect(url_for('index'))


@app.route(app.config['GOOGLE_REDIRECT'])
@google.authorized_handler
def authorized(resp):
    """URI where the Google API redirects the user after successful login."""
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    flash('You were successfully logged in.', 'info')
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(e):
    """The function handles the HTTP 404 error status code."""
    return render_template('404.html')


@app.errorhandler(401)
def unauthorized(e):
    """The function handles the HTTP 401 error status code."""
    return render_template('401.html')
