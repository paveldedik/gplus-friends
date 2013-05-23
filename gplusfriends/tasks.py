# -*- coding: utf-8 -*-

"""
Tasks
=====
"""

from hashlib import md5

from gplusfriends import cache
from gplusfriends.resources import (get_person, get_people, get_activities,
                                    get_access_token)


def get_person_data(person_id):
    """Function that returnes cashed user's data.
    :param person_id: ID of the requested person.
    :return: The :class:`models.Person` instance if the user is logged in,
             ``NoneType`` object otherwise.
    """
    token = get_access_token()
    if token is None:
        return None
    else:
        token_hash = md5(token[0]).hexdigest()
        cache_id = '{0}-{1}'.format(person_id, token_hash)
        return from_cache(cache_id, call=process_data, args=(person_id,))


def from_cache(key, call=None, args=()):
    """Gets data from the cache.
    :param key: The identifier of the data to be retrieved from the cache.
    :param call: If the key isn't present in the cache, call the function.
    :return: The retrieved data.
    """
    data = cache.get(key)
    if data is None and call:
        data = call(*args)
        cache.set(key, data, timeout=30 * 60)  # 30 minutes
    return data


def process_data(person_id):
    """Requests all google+ data about the specified person.
    :param person_id: Google+ ID of the persen.
    :return: An instance of the :class:`models.Person`.
    """
    person = get_person(id=person_id)
    activities = get_activities(id=person_id)
    person.activities.extend(activities)

    if person_id == 'me':
        people = get_people(id=person_id)
        person.people.extend(people)

    return person
