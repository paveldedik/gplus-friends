Documentation
=============

This page describes the basic architecture of the application.

Domain Model
------------
The application registers two entities which are subclasses of the abstract class Document (see `gplusfriends/models.py`).

###_class_ Document()

Abstract class that represents a document (e.g. XML, JSON).

_method_ **to_dict**()
Creates a dictionary which represents an instance of the subclassed class.

_method_ **to_json**()
Creates a JSON document which represents an instance of the subclassed class.

_method_ **to_xml**()
Creates an XML document which represents an instance of the subclassed class.

_method_ **to_etree**()
Creates an element tree which represents an instance of the subclassed class.

###_class_ Person(**kwargs)

Representation of a person. [See Google+ API reference](https://developers.google.com/+/api/latest/people).

* _id_: Google+ unique ID of the person.
* _name_: Name of the person.
* _url_: The link to the profile of the person.
* _gender_: The person's gender. Possible values are `male`, `female` or `other`.
* _type_: Whether the person is a page or a person.
* _people_: All the friends the person has in their circles.
* _activities_: All the activities the person posted.

###_class_ Activity(**kwargs)

Representation of an activity. [See Google+ API reference](https://developers.google.com/+/api/latest/activities).

* _id_: Google+ unique ID of the activity.
* _title_: Title of the activity.
* _url_: The link to the activity.
* _date_: The time at which this activity was initially published.
* _content_: The content of the activity (HTML formated).
* _publisher_: The person who performed the activity.

Views
-----
Endpoints of the application (see `gplusfriends/views.py`).

###Endpoints

GET `/`
Homepage of the application.

GET `/people/<pid:string>`
Endpoint that displays persons's friends, acquantances, followed pages and activities (which are notes the users have posted to their stream).

GET `/activities/<string:aid>`
Endpoint that displays the specified activity.

POST `/people`
Redirects the user to a person corresponding the input value.

POST `/activities`
Redirects the user to an activity corresponding the input value.

GET `/login`
Login endpoint which authorizes the user through the Google+ API.

GET `/logout`
Logout endpoint which removes the logged user's `access_token` from the session.

GET `/auth`
URI where the Google API redirects the user after successful login.

API Resources
-------------
The application uses four Google+ API resources (see `gplusfriends/resources.py`).

_Resource_ `people/{id}`
Requests user's data by their Google+ unique ID and creates an instance of the _class_ **Person**.

_Resource_ `activities/{id}`
Requests activity's data by its Google+ unique ID and creates an instance of the _class_ **Activity**.

_Resource_ `people/{id}/people/visible`
Requests information about given persons's friends and creates a list of instances of the _class_ **Person**.

_Resource_ `people/{id}/activities/public`
Requests information about given persons's public activities and creates a list of instances of the _class_ **Activity**.

Templates
---------
The templates of the application are created with the Jinja2 template engine (see `gplusfriends/templates/*`).

_Template_ `index.html`
Represents the basic layout of the page. Other templates extends this template.

_Template_ `loggedout.html`
If the user is not logged in with their Google+ account, this template representing the homepage of the application is displayed.

_Template_ `loggedin.html`
The template provides basic tools of the application and is presented to the user when they are successfully logged in.

_Template_ `person.html`
Displayes the downloaded data of a person from the google+ API and provides tools for converting and downloading the data as an XML document.

_Template_ `activity.html`
Displayes the downloaded data of an activity from the google+ API and provides tools for converting and downloading the data as an XML document.

_Template_ `404.html`
This template is displayed when the user enters in the browser a URL which doesn't exist.

_Template_ `401.html`
This template is displayed when the user doesn't have sufficient right to view the requested data.
