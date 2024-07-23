from flask import Flask, g, request , Response, make_response 
from flask import session, render_template , url_for
from datetime import date, datetime, timedelta
import os



app = Flask(__name__)
import flask_senior.views
import flask_senior.tests
import flask_senior.filters


app.debug = True
# app.jinja_env.trim_blocks = True


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint , filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


app.config.update(
    SECRET_KEY='X1243yRH!mMwf',
    SESSION_COOKIE_NAME='pyweb_flask_session',
    PERMANENT_SESSION_LIFETIME=timedelta(31)    # 31days
)







