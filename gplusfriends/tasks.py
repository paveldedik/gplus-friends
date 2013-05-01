# -*- coding: utf-8 -*-


from gplusfriends import google
from gplusfriends.models import Person


def get_resource(endpoint):
    def wrapper(get_entity):
        def func(entity_id, headers=None):
            data = google.get(endpoint + entity_id, headers=headers).data
            return get_entity(data, entity_id)
        return func
    return wrapper


def process_data(token):
    headers = {'Authorization': 'Bearer ' + token}
    person = get_person('me', headers=headers)
    return person.to_json()


@get_resource('people/')
def get_person(data, entity_id, headers=None):
    return Person(data['id'], data['displayName'],
                  url=data['url'], gender=data['gender'])


@get_resource('activities/')
def get_activity(data, entity_id, headers=None):
    raise NotImplementedError
