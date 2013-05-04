# -*- coding: utf-8 -*-

"""
Google+ API resources
=====================
"""


from gplusfriends import google, app
from gplusfriends.models import Person, Activity


def get_header(token):
    """Returns header required for Google+ API authorization.
    :param token: User's access token.
    """
    return {'Authorization': app.config['GOOGLE_AUTH'].format(token=token)}


def resource(endpoint):
    """A decorator for mining specified data thourgh Google+ API.
    :param endpoint: The type of data that will be requested.
    """
    def wrapper(func):
        def decorator(token, **kwargs):
            formated = endpoint.format(**kwargs)
            data = google.get(formated, headers=get_header(token)).data
            return func(data)
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
    return Person(data['id'], data['displayName'],
                  url=data['url'], gender=data['gender'])


@resource('activities/{id}')
def get_activity(data):
    """Requests activity's data and creates an instance of the
    :class:`models.Activity`.
    :param token: Access token required for authorization.
    :param id: ID of the requested activity.
    """
    publisher = Person(data['actor']['id'], data['actor']['displayName'],
                       url=data['actor']['url'])
    return Activity(data['id'], data['title'], url=data['url'],
                   date=data['published'], publisher=publisher,
                   content=data['object']['content'])


@resource('people/{id}/people/visible')
def get_people(data):
    """Requests information about given persons's friends and creates
    a list :obj:`models.Person`.
    :param token: Access token required for authorization.
    :param id: ID of the person who's friends will be requested.
    """
    people = []

    for item in data['items']:
        person = Person(item['id'], item['displayName'], url=item['url'])
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
        publisher = Person(item['actor']['id'], item['actor']['displayName'],
                           url=item['actor']['url'])
        activity = Activity(item['id'], item['title'], url=item['url'],
                            date=item['published'], publisher=publisher,
                            content=item['object']['content'])
        activities.append(activity)

    return activities
