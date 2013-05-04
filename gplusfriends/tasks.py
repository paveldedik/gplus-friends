# -*- coding: utf-8 -*-

"""
Tasks
=====
"""

from gplusfriends.resources import get_person, get_people, get_activities


def process_data(token):
    """Requests all needed data.
    :param token: Unique user's access token.
    """
    person = get_person(token, id='me')
    friends = get_people(token, id='me')
    activities = get_activities(token, id='me')

    person.friends.extend(friends)
    person.activities.extend(activities)
    return person
