# -*- coding: utf-8 -*-


from flask import render_template

from gplusfriends import app


@app.route('/')
def index():
    return render_template('index.jinja')
