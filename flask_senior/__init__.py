from flask import Flask, g, request , Response, make_response 
from flask import session, render_template , url_for
from datetime import date, datetime, timedelta
from markupsafe import Markup
from dateutil.relativedelta import relativedelta
import os    
import calendar


app = Flask(__name__)
app.debug = True
# app.jinja_env.trim_blocks = True

app.config.update(
    SECRET_KEY='X1243yRH!mMwf',
    SESSION_COOKIE_NAME='pyweb_flask_session',
    PERMANENT_SESSION_LIFETIME=timedelta(31)    # 31days
)


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint , filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.template_filter('ymd')
def datetime_ymd(dt, fmt='%m-%d'):
    if isinstance(dt, date):
        return "<strong>%s</strong>" % dt.strftime(fmt)
    else:
        return dt
    
    
@app.template_filter('simpledate')
def simpledate(dt):
    if not isinstance(dt, date):
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M')
    if (datetime.now() - dt).days < 1:
        fmt = "%H시 %M분이다"
    else:
        fmt = "%m월 %d일이다"
        
    return "<strong>%s</strong>" % dt.strftime(fmt)


def make_date(dt, fmt):
    if not isinstance(dt, date):
        return datetime.strptime(dt, fmt)
    else:
        return dt


@app.template_filter('mdt')
def mdt(dt, fmt='%Y-%m-%d'):
    d = make_date(dt, fmt)
    wd = d.weekday()
    # if wd == 6:
    #     return -1
    # else:
    #     return wd * -1
    return (1 if wd == 6 else wd) * -1


@app.template_filter('month')
def month(dt, fmt='%Y-%m-%d'):
    d = make_date(dt, fmt)
    return d.month
        
        
@app.template_filter('edt')
def edt(dt, fmt='%Y-%m-%d'):
    d = make_date(dt, fmt)
    nextMonth = d + relativedelta(month=1)
    return (nextMonth - timedelta(1)).day

    

class FormInput:
    def __init__(self, id, name, value, checked, text):
        self.id = id
        self.name = name
        self.value = value
        self.checked = checked
        self.text = text



@app.route('/')
def idx():
    rds = []
    for i in [1,2,3]:
        id = 'r' + str(i)
        name = 'radiotest'
        value = i
        checked = ''
        if i == 2:
            checked = 'checked'
        text = 'RadioTest' + str(i)
        rds.append(FormInput(id,name,value,checked,text))
        
    # today1 = date.today()
    today2 = datetime.now()
    # d = datetime.strptime("2024-07-20", "%Y-%m-%d")
    # year = 2024
    years = request.args.get('year', date.today().year, int)
    
    return render_template('app.html', year= years, sbsb='SBSB', ttt='triplesss', radioList=rds, today=today2 )


@app.route('/top100')
def top100():
    return render_template('application.html', title='main!!')


@app.route("/main")
def main():
    return render_template('main.html')


class Nav:
    def __init__(self, title, url='#', children=[]):
        self.title = title
        self.url = url
        self.children = children
        
        
@app.route("/tmpl3")
def tmpl3():
    py = Nav("파이썬", "https://search.naver.com",[])
    java = Nav("자바", "https://search.naver.com",[])
    prg = Nav("프로그래밍 언어", "https://search.naver.com",[py,java])
    jinja = Nav("JINJA", "https://search.naver.com",[])
    flask = Nav("플라스크", "https://search.naver.com",[jinja])
    my = Nav("나의 일상", "https://search.naver.com",[])
    others = Nav("기타", "https://search.naver.com",[my])
    
    return render_template("indexsss.html", navs=[java, others])


@app.route("/tmpl2")
def tmpl2():
    a = (1, '만남1', '김건모', False, [])
    b = (2, '만남2', '노사연', True, [a])
    c = (3, '만남3', '익명', False, [a,b])
    d = (4, '만남4', '익명2', False, [a,b,c])

    return render_template("indexsss.html", lst2=[a,b,c,d])


@app.route("/tmpl")
def tmpl():
    tit2 = Markup("<strong>Title222</strong>")
    mu = Markup("<h3>iii = <i>%s</i></h3>")
    h = mu % "Italic"
    lsst = [('sadf','1111'), ('qwer','2222'), ('dfdf','3333')]
    noodles = [('samyang'),('nongsim'),('paldo'),('oddugi')]
    return render_template('indexss.html', title="SSBR" , title2=tit2 , mu=h , lst=lsst , pds = noodles)
    

@app.route('/wc')
def wc():
    key = request.args.get('key')
    val = request.args.get('val')
    res = Response("SET COOKIE")
    res.set_cookie(key, val)
    session['Token'] = '123X'
    return make_response(res)


@app.route('/rc')
def rc():
    key = request.args.get('key')
    val = request.cookies.get(key)
    return "cookie["+key+"] = " + val + " , " + session.get('Token')


@app.route('/delsess')
def delsess():
    if session.get('Token'):
        del session['Token']
    return "Session이 삭제되었습니다."


@app.route('/reqenv')
def reqenv():
    return ("REQUEST_METHOD: %(REQUEST_METHOD)s<br>"
            "SCRIPT_NAME: %(SCRIPT_NAME)s<br>"
            "PATH_INFO: %(PATH_INFO)s<br>"
            "QUERY_STRING: %(QUERY_STRING)s<br>"
            "SERVER_NAME: %(SERVER_NAME) s<br>"
            "SERVER_PORT: %(SERVER_PORT) s<br>"
            "SERVER_PROTOCOL: %(SERVER_PROTOCOL) s<br>"
            'wsgi.version: %(wsgi.url_scheme) s<br>'
            ) % request.environ


def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str, fmt)
    return trans

@app.route("/dt")
def dt():
    datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식 : %s" % str(datestr) 



# app.config['SERVER_NAME']='local.com:5000'


# @app.route("/sd")
# def helloworld_local():
#     return "Hello Local.com"


# @app.route("/sd", subdomain="g")
# def helloworld1():
#     return "Hello G.Local.com!!!"


@app.route('/rp')
def rp():
    # q = request.args.get('q')
    q = request.args.getlist('q')
    return "q= %s" % str(q)


@app.route('/test_wsgi')
def wsgi_test():
    def application(environ, start_response):
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        headers = [('Content-Type', 'text/plain'),
                   ('Content-Length', str(len(body)))]
        start_response('200 OK', headers)
        return [body]
    return make_response(application)
        
        
@app.route("/res1")
def res1():
    custom_res = Response("Custom Response!!!!", 200, {'test':'ttt'})   #Response(바디본문? , status코드 , 헤더)
    return make_response(custom_res)


# @app.before_request
# def before_request():
#     print("before request")
#     g.str = "한글"



# @app.route("/gg")
# def helloworld2():
#     return "Hello Flask World" + getattr(g, 'str', '111')



# @app.route("/")
# def helloworld():
#     return "Hello Falsk World !!!"    








