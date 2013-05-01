# -*- coding: utf-8 -*-


from gplusfriends import google
from gplusfriends.models import Person


def resource(endpoint):
    """A decorator for mining specified data thourgh Google+ API.
    :param endpoint: The type of data that will be requested.
    """
    def wrapper(get_entity):
        def func(entity_id, headers=None):
            relative_url = endpoint + '/' + entity_id
            data = google.get(relative_url, headers=headers).data
            return get_entity(data, entity_id)
        return func
    return wrapper


def process_data(token):
    """Requests all needed data.
    :param token: Unique user's access token.
    """
    headers = {'Authorization': 'Bearer ' + token}
    person = get_person('me', headers=headers)
    return person.to_json()


@resource('people')
def get_person(data, entity_id, headers=None):
    """Requests user's data and creates an instance of the
    :class:`models.Person`.
    :param entity_id: ID of the requested user. Posible value is ``'me'``,
                      which requests the user that is currently logged in.
    :param headers: Optional headers of the request (e.g. access token).
    """
    return Person(data['id'], data['displayName'],
                  url=data['url'], gender=data['gender'])


@resource('activities')
def get_activity(data, entity_id, headers=None):
    """Requests activity's data and creates an instance of the
    :class:`models.Activity`.
    :param entity_id: ID of the requested user.
    :param headers: Optional headers of the request (e.g. access token).
    """
    raise NotImplementedError
