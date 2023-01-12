from app import app 
from flask import render_template, request, session, redirect, url_for

from utils import get_db_connection
from models.routes_model import *
from datetime import datetime, timedelta

@app.route('/routes', methods=['get', 'post']) 
def routes():
 
    conn = get_db_connection()

    req = {}
    session['cur_date'] = str(date.today())
    session['cur_time'] = str(datetime.now().strftime("%H:%M"))
    min_time = '07:00'
    max_time = '20:00'
     
    # если пользователь авторизован 
    if request.cookies.get('user_id'):
        user_id = request.cookies.get('user_id') 
        session['user_id'] = str(user_id)
    else:
        return redirect(url_for('index'))

    # выбрана дата (get)
    if request.values.get('date'):
        date_val = request.values.get('date')
        session['date'] = str(date_val)
    else:
        session['date'] = session['cur_date']

    # выбрана дата (post)
    if request.form.get('date'):
        date_val = request.form.get('date')
        session['date'] = str(date_val)

    # нажата кнопка "Добавить рейс"
    if request.form.get('add'):
        route_id = request.form.get('route_id')
        add_trip(conn, session['date'] + ' 00:00:00', route_id)
        return redirect(url_for('routes'))

    # перенос рейсов с предыдущего дня
    if request.form.get('carry'):
        carry_trip(conn, session['date'], str(datetime.strptime(session['date'], '%Y-%m-%d') - timedelta(days = 1)))
        return redirect(url_for('routes') + '?date=' + session['date'])

    # выбран рейс
    if request.form.get('trip_id'):
        trip_id = request.form.get('trip_id')
        req['trip_id'] = trip_id
    else:
        req['trip_id'] = 0
 
    # выбран номер автобуса
    if request.form.get('bus_id'):
        bus_id = request.form.get('bus_id')
        req['bus_id'] = bus_id
    else:
        req['bus_id'] = 0
 
    # выбран водитель
    if request.form.get('driver_id'):
        driver_id = request.form.get('driver_id')
        req['driver_id'] = driver_id
    else:
        req['driver_id'] = 0

    # выбрано время
    if request.form.get('time'):
        time_val = request.form.get('time')
        req['datetime'] = session['date'] + ' ' + str(time_val) + ':00'
    else:
        req['datetime'] = None

    # вычисление минимально возможного времени
    if session['date'] != session['cur_date']:
        session['cur_time'] = min_time

    if int(req['trip_id']) > 0 and int(req['bus_id']) > 0  and int(req['driver_id']) > 0 \
    and req['datetime'] is not None:
        update_trip(conn, req['trip_id'], req['bus_id'], req['driver_id'], req['datetime'])
        return redirect(url_for('routes') + '?date=' + session['date'])
 
    df_trip_today = get_trip(conn, session['date'])
    print("CONTROLLER")
    print(df_trip_today)
    df_trip_today = df_trip_today.fillna(0)
    df_trip_yesterday = get_trip(conn, str(datetime.strptime(session['date'], '%Y-%m-%d') - timedelta(days = 1)))
    df_bus = get_bus(conn)
    df_driver = get_driver(conn)
    df_route = get_route(conn)

    
     
    # выводим страницу 
    html = render_template( 
        'routes.html',
        user = session['user_id'],
        cur_date = session['cur_date'],
        date = session['date'],
        cur_time = session['cur_time'],
        max_time = max_time,
        trip_today = df_trip_today,
        trip_yesterday = df_trip_yesterday,
        table_bus = df_bus,
        table_driver = df_driver,
        table_route = df_route,
        len = len
    ) 
    return html 
