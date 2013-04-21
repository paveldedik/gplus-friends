Google+ Friends Visualization
=============================

The projects aimes to practise knowledge of the modern markup languages (XML, XSLT, XPath, XQuery etc.). It is written in Python and uses the front-end web framework Twitter Bootstrap.

Description
-----------
The task is to create a web application which visualizes information about google+ friends of the signed up user. This can be separated into following parts:

* download the needed data through Google+ API
* store the data as a XML document
* visualize the data on the created webpage

Run the application
-------------------
To run the application you will need python 2.7 and `pip` (python package manager). However, I recommend using `virtualenv` as well.

The requirements can be satisfied running this command:

```bash
$ pip install -r requirements.txt
```

If you don't use `virtualenv` you will need root priveleges.

After the installation run:

```bash
$ python runserver.py
```

Which will start up the server on the localhost (`127.0.0.1:5000`).

Team
----
Developers:

* Pavel Dedík

Owners of the project:

* Adam Rambousek
* Marek Grác

Lecturers:

* Tomáš Pitner
* Luděk Bártek
