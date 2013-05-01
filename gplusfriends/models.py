# -*- coding: utf-8 -*-


import json


class Document(object):

    def __repr__(cls):
        return '<{0} id:{1}>'.format(cls.__class__.__name__, cls.id)

    def to_dict(cls):
        return dict(
            (attr for attr in cls.__dict__.items()
             if not attr[0].startswith('_')))

    def to_json(cls):
        return json.dumps(cls.to_dict(), indent=2)


class Person(Document):

    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name
        self.url = kwargs.get('url')
        self.gender = kwargs.get('gender')
        self.friends = kwargs.get('friends', [])
        self.activities = kwargs.get('activities', [])


class Activity(Document):

    def __init__(self, id, title, **kwargs):
        self.id = id
        self.title = title
        self.url = kwargs.get('url')
        self.date = kwargs.get('date')
        self.content = kwargs.get('content')
        self.publisher = kwargs.get('publisher')
