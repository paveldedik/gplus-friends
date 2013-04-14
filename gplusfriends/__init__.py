# -*- coding: utf-8 -*-


__version__ = '0.0.1'


from flask import Flask


app = Flask(__name__)
app.config.from_object('gplusfriends.config')


from gplusfriends import views


if __name__ == '__main__':
    app.run()
