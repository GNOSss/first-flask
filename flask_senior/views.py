from flask import render_template, request, Response, jsonify
from datetime import datetime, date
from flask_senior import app
from flask_senior.classes import FormInput
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from flask_senior.init_db import db_session, world_session
from flask_senior.models import User, Country, City, User_country
from collections import namedtuple
from sqlalchemy import func
from sqlalchemy.orm import subqueryload, joinedload


@app.route('/sqljoin')
def sqljoin():
    session = db_session()
    
    try:
        
        
        # 예제: User 데이터 삽입
        new_user = User(email='kbr111111@example.com', passwd='password123', nickname='Boster')
        session.add(new_user)  # 세션에 새로운 User 객체를 추가합니다.
        session.flush()
        
        # 예제: UserCountry 데이터 삽입
        new_country = User_country(countrycode='Purgio111111', country='Korea')
        new_user.user_countries.append(new_country)
        # session.add(new_country)  # 세션에 새로운 UserCountry 객체를 추가합니다.

        session.commit()
        
        # 성공 메시지 반환
        return "Data inserted successfully"
    
    except Exception as e:
        session.rollback()
        return f"An error occurred : {e}"

    finally:
        session.close()


# pre-load (sametime)
@app.route('/sql2')
def sql2():
    # test = world_session.query(City).options(subqueryload(City.countries)).filter(City.population > 1000000).all()
    test = world_session.query(City).options(joinedload(City.countries)).filter(City.population > 5000000).all()
    return render_template('sqltest.html', test=test)



# select by each record
@app.route('/sql')




@app.route('/')
def idx():
    try:
        
        # Create(insert)
        # u = User('abc@gmail.com','SONG')
        # db_session.add(u)
        # db_session.commit()
        
        # Read(select)
        # 두 코드 같은 결과값 반환함
        # ret = User.query.filter(User.id > 54)
        ret = db_session.query(User).filter(User.id < 40).all()
        world_data = world_session.query(Country).filter(Country.population > 100000000).all()
        city_data = City.query.join(Country, Country.code == City.countrycode).filter(City.population > 7000000).all()
        have10cities = world_session.query(Country.code, Country.name).join(City, Country.code == City.countrycode).group_by(Country.code, Country.name).having(func.count(City.id) >=30).all()

        
        # Update(update)
        # u.email = 'TripleSSS@gmail.com'
        # db_session.add(u) 
        
        # delete(delete)
        # u = User.query.filter(User.id == 48).first()
        # db_session.delete(u)
        
        
        # # 서브 세션 생성
        # s = db_session()
        
        # # 서브 세션을 .execute()로 쿼리문 작성
        # result = s.execute(text("SELECT id, email, nickname FROM USER WHERE id > :id"), {'id': 50})
        # Record = namedtuple('User',result.keys())
        # records = [Record(*row) for row in result.fetchall()]
        
        # for r in records:
        #     print(r, r.nickname, type(r))
        # s.close()
        

        # 쿼리 함수 작성 후 Commit
        db_session.commit()
        world_session.commit()

        # 서브세션 쿼리문 응답을 return값에 전달
        # ret = records
    
        # ret = 'aaa'
        # ret = User.query.filter(User.id > 49).all()
        
        
        # for user in  ret:
        #user.followers = Foller.query.filter(Foller.user_id == user.id).all()
        
        
    except SQLAlchemyError as sqlerr:
        db_session.rollback()
        world_session.rollback()
        print("SqlError >>", sqlerr)
        ret = []
        world_data = []
        city_data = []
        have10cities = []
        
    except Exception as e:
        print("Error!!")
        ret = []
        world_data = []
        city_data = []
        have10cities = []
        
    
        
    
    # return "RET=" + str(ret)
    return render_template('main.html', users=ret, worlds=world_data, city_data=city_data, have10cities=have10cities)
    
    
    # # 쿼리 실행
    # users = db_session.query(User).filter(User.id > 0).all()

    # # 결과를 JSON 형식으로 변환
    # result = [{
    #     'id': user.id,
    #     'email': user.email,
    #     'nickname': user.nickname
    # } for user in users]

    # return jsonify(result)

    
    
    