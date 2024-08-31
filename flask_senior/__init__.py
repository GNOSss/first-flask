from flask import Flask, g, request , Response, make_response 
from flask import session, render_template , url_for
from datetime import date, datetime, timedelta
import os
from flask_senior.init_db import init_database, db_session, world_session



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


@app.before_first_request
def beforeFirstRequest():
    print(">> before first request")
    init_database()
    

@app.after_request
def afterReq(response):
    print(">> after request")
    return response


@app.teardown_request
def teardown_request(exception):
    print(">> teardown request", exception)
    
    
@app.teardown_appcontext
def teardown_context(exception):
    print(">> teardown context", exception)
    db_session.remove()
    world_session.remove()
    
    
# 3자리 숫자마다 (,) 넣어주는 필터
@app.template_filter('format_number')
def format_number(num):
    if isinstance(num, (int,float)):
        return "{:,}".format(num)
    return num