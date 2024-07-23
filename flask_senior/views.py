from flask import render_template, request, Response
from datetime import datetime, date
from flask_senior import app
from flask_senior.classes import FormInput


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
