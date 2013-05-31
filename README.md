Demo
----
The application is available at [heroku](http://gplusfriends.herokuapp.com).

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

Which starts up the server on the localhost (`127.0.0.1:5000`).

**Note**: You should create your own client ID (see [Google API Console](https://code.google.com/apis/console/)) and edit the following variables in `gplusfriends/config.py`:

* `GOOGLE_CLIENT_ID`
* `GOOGLE_CLIENT_SECRET`
* `GOOGLE_REDIRECT`

Licence
-------
The application is released under the [MIT License](http://www.opensource.org/licenses/MIT).
