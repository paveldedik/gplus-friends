# -*- coding: utf-8 -*-


import json
import unittest
from lxml import etree
from datetime import datetime
from StringIO import StringIO

from gplusfriends.models import Activity, Person


person2 = Person(
    id='111',
    name='Osoba 1',
    url='http://plus.google.com/111',
    type='person'
)

activity = Activity(
    id='aaa',
    title='Aktivita 1',
    url='http://plus.google.com/aaa',
    date=datetime(2013, 05, 05),
    content='Aktivita 1 obsah',
    publisher=person2
)

person = Person(
    id='222',
    name='Osoba 2',
    url='http://plus.google.com/222',
    type='person',
    gender='male',
    people=[person2],
    activities=[activity]
)

a_dict = {
    'id': 'aaa',
    'title': 'Aktivita 1',
    'url': 'http://plus.google.com/aaa',
    'date': datetime(2013, 05, 05),
    'content': 'Aktivita 1 obsah',
    'publisher': person2,
}

a_json = """{
  "id": "aaa",
  "title": "Aktivita 1",
  "url": "http://plus.google.com/aaa",
  "date": "2013-05-05 00:00:00",
  "content": "Aktivita 1 obsah",
  "publisher": "111"
}"""

p_dict = {
    'id': '222',
    'name': 'Osoba 2',
    'url': 'http://plus.google.com/222',
    'gender': 'male',
    'type': 'person',
    'people': [person2],
    'activities': [activity],
}

p_json = """{
  "id": "222",
  "name": "Osoba 2",
  "url": "http://plus.google.com/222",
  "gender": "male",
  "type": "person",
  "people": ["111"],
  "activities": ["aaa"]
}"""


class TestPerson(unittest.TestCase):

    def setUp(self):
        self.person = person
        self.dict_test = p_dict
        self.json_test = json.loads(p_json)
        self.xml_schema = 'gplusfriends/static/xsd/person.xsd'

    def test_to_dict(self):
        person_dict = self.person.to_dict()
        self.assertEqual(person_dict, self.dict_test)

    def test_to_json(self):
        person_json = self.person.to_json()
        self.assertEqual(json.loads(person_json), self.json_test)

    def test_to_xml(self):
        person_xml = etree.parse(StringIO(self.person.to_xml()))
        with open(self.xml_schema) as f:
            doc = etree.parse(f)
        schema = etree.XMLSchema(doc)
        self.assertTrue(schema.validate(person_xml))


class TestActivity(unittest.TestCase):

    def setUp(self):
        self.activity = activity
        self.dict_test = a_dict
        self.json_test = json.loads(a_json)
        self.xml_schema = 'gplusfriends/static/xsd/activity.xsd'

    def test_to_dict(self):
        activity_dict = self.activity.to_dict()
        self.assertEqual(activity_dict, self.dict_test)

    def test_to_json(self):
        activity_json = self.activity.to_json()
        self.assertEqual(json.loads(activity_json), self.json_test)

    def test_to_xml(self):
        activity_xml = etree.parse(StringIO(self.activity.to_xml()))
        with open(self.xml_schema) as f:
            doc = etree.parse(f)
        schema = etree.XMLSchema(doc)
        self.assertTrue(schema.validate(activity_xml))


if __name__ == '__main__':
    unittest.main()
