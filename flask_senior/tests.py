from flask import render_template, Markup, request, Response, session, make_response, g
from datetime import datetime, date
from flask_senior import app
from flask_senior.classes import Nav



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








