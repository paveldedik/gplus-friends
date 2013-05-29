# -*- coding: utf-8 -*-

"""
Tasks
=====
"""

from hashlib import md5

from gplusfriends import cache
from gplusfriends.resources import (get_person, get_people, get_activities,
                                    get_activity, get_access_token)


def cashed_data(func):
    """Decorator which tries to load the needed data from the cache.
    If the data aren't present in the cache, call the decorated function.
    :param func: the decorated function.
    """
    def wrapper(entity_id):
        token = get_access_token()

        if token is None:
            return None

        token_hash = md5(token[0]).hexdigest()
        cache_key = '{0}-{1}'.format(entity_id, token_hash)
        data = cache.get(cache_key)

        if data is None:
            data = func(entity_id)
            cache.set(cache_key, data, timeout=30 * 60)  # 30 minutes

        return data
    return wrapper


@cashed_data
def get_person_data(person_id):
    """Requests all google+ data about the specified person.
    :param person_id: Google+ ID of the person.
    :return: An instance of the :class:`models.Person`.
    """
    person = get_person(id=person_id)
    activities = get_activities(id=person_id)
    person.activities.extend(activities)

    if person_id == 'me':
        people = get_people(id=person_id)
        person.people.extend(people)

    return person


@cashed_data
def get_activity_data(activity_id):
    """Requests all google+ data about the specified activity.
    :param activity_id: Google+ ID of the activity.
    :return: An instance of the :class:`models.Activity`.
    """
    return get_activity(id=activity_id)
