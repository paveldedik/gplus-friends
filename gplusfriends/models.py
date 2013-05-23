# -*- coding: utf-8 -*-

"""
Application models
==================
"""

import json


class DocumentEncoder(json.JSONEncoder):
    """JSON encoder."""

    def default(self, obj):
        if isinstance(obj, Document):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)


class Document(object):
    """Representation of a document mixin."""

    def __repr__(cls):
        return '<{0} id:{1}>'.format(cls.__class__.__name__, cls.id)

    def to_dict(cls):
        return dict(
            (attr for attr in cls.__dict__.items()
             if not attr[0].startswith('_')))

    def to_json(cls):
        return json.dumps(cls.to_dict(), indent=2,
                          ensure_ascii=False, cls=DocumentEncoder)


class Person(Document):
    """Representation of a person. `See Google+ API reference
    <https://developers.google.com/+/api/latest/people>`_.
    :param id: Google+ unique ID of the person.
    :param name: Name of the person.
    :param url: The link to the profile of the person.
    :param type: Whether the person is a page or a person.
    :param gender: The person's gender. Possible values are ``male``,
                   ``female`` or ``other``.
    :param people: All the friends and pages the person has in their circles.
    :param activities: All the activities the person posted.
    """
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.url = kwargs.get('url')
        self.type = kwargs.get('type')
        self.gender = kwargs.get('gender')
        self.people = kwargs.get('people', [])
        self.activities = kwargs.get('activities', [])

    @staticmethod
    def from_google(data):
        return {
            'id': data.get('id'),
            'name': data.get('displayName').strip(' .'),
            'url': data.get('url'),
            'type': data.get('objectType'),
            'gender': data.get('gender')
        }


class Activity(Document):
    """Representation of an activity. `See Google+ API reference
    <https://developers.google.com/+/api/latest/activities>`_.
    :param id: Google+ unique ID of the activity.
    :param title: Title of the activity.
    :param url: The link to the activity.
    :param date: The time at which this activity was initially published.
    :param content: The content of the activity (HTML formated).
    :param publisher: The person who performed the activity.
    """
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.title = kwargs.get('title')
        self.url = kwargs.get('url')
        self.date = kwargs.get('date')
        self.content = kwargs.get('content')
        self.publisher = kwargs.get('publisher')

    @staticmethod
    def from_google(data):
        return {
            'id': data.get('id'),
            'title': data.get('title'),
            'url': data.get('url'),
            'date': data.get('published'),
            'content': data['object'].get('content')
        }
