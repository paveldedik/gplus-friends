# -*- coding: utf-8 -*-


from gplusfriends import google
from gplusfriends.models import Person


def resource(endpoint):
    def wrapper(get_entity):
        def func(entity_id, headers=None):
            relative_url = endpoint + '/' + entity_id
            data = google.get(relative_url, headers=headers).data
            return get_entity(data, entity_id)
        return func
    return wrapper


def process_data(token):
    headers = {'Authorization': 'Bearer ' + token}
    person = get_person('me', headers=headers)
    return person.to_json()


@resource('people')
def get_person(data, entity_id, headers=None):
    return Person(data['id'], data['displayName'],
                  url=data['url'], gender=data['gender'])


@resource('activities')
def get_activity(data, entity_id, headers=None):
    raise NotImplementedError
