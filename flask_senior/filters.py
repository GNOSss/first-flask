from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from flask_senior import app
from flask_senior.utils import make_date



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
