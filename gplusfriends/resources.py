# -*- coding: utf-8 -*-

"""
Google+ API resources
=====================
"""

from flask import abort, session

from gplusfriends import google, app
from gplusfriends.models import Person, Activity


@google.tokengetter
def get_access_token():
    """Returns user's access token.
    :return: Access token.
    """
    return session.get('access_token')


def get_header():
    """Returns header required for Google+ API authorization.
    :return: Google+ header needed for authorization.
    """
    token = get_access_token()[0]
    return {'Authorization': app.config['GOOGLE_AUTH'].format(token=token)}


def resource(endpoint):
    """A decorator for mining specified data thourgh Google+ API.
    :param endpoint: The type of data that will be requested.
    """
    def wrapper(func):
        def decorator(**kwargs):
            formated = endpoint.format(**kwargs)
            resp = google.get(formated, headers=get_header())
            if resp.status != 200:
                abort(resp.status)
            return func(resp.data)
        return decorator
    return wrapper


@resource('people/{id}')
def get_person(data):
    """Requests user's data and creates an instance of the
    :class:`models.Person`.
    :param token: Access token required for authorization.
    :param id: ID of the requested user. Posible value is ``'me'``,
               which requests the user that is currently logged in.
    """
    # create the person
    kwargs = Person.from_google(data)
    return Person(**kwargs)


@resource('activities/{id}')
def get_activity(data):
    """Requests activity's data and creates an instance of the
    :class:`models.Activity`.
    :param token: Access token required for authorization.
    :param id: ID of the requested activity.
    """
    # create the person
    person_kwargs = Person.from_google(data['actor'])
    publisher = Person(**person_kwargs)
    # create the activity
    activity_kwargs = Activity.from_google(data)
    return Activity(publisher=publisher, **activity_kwargs)


@resource('people/{id}/people/visible')
def get_people(data):
    """Requests information about given persons's friends and creates
    a list :obj:`models.Person`.
    :param token: Access token required for authorization.
    :param id: ID of the person who's friends will be requested.
    """
    people = []
    for item in data['items']:
        # create the person
        kwargs = Person.from_google(item)
        person = Person(**kwargs)
        people.append(person)

    return people


@resource('people/{id}/activities/public')
def get_activities(data):
    """Requests information about given persons's public activities
    and creates a list of :obj:`models.Activity`.
    :param token: Access token required for authorization.
    :param id: ID of the person who's activities will be requested.
    """
    activities = []
    for item in data['items']:
        # create the person
        person_kwargs = Person.from_google(item['actor'])
        publisher = Person(**person_kwargs)
        # create the activity
        activity_kwargs = Activity.from_google(item)
        activity = Activity(publisher=publisher, **activity_kwargs)
        activities.append(activity)

    return activities
