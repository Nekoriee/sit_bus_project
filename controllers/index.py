from app import app 
from flask import render_template, request, session

from utils import get_db_connection
from models.index_model import *
from datetime import datetime

@app.route('/', methods=['get']) 
def index(): 
 
    conn = get_db_connection()

    session['cur_date'] = str(date.today())
     
    # если пользователь авторизован 
    if request.cookies.get('user_id'):
        user_id = request.cookies.get('user_id') 
        session['user_id'] = str(user_id)
    else:
        session['user_id'] = None

    # выбрана дата
    if request.values.get('date'):
        date_val = request.values.get('date')
        session['date'] = str(date_val)
    else:
        session['date'] = session['cur_date']
 
    # выбрана остановка
    if request.values.get('bustop'):
        bustop_id = request.values.get('bustop')
        session['bustop'] = str(bustop_id)
    else:
        session['bustop'] = str(0)
 
    # выбран маршрут
    if request.values.get('route'):
        route_id = request.values.get('route')
        session['route'] = str(route_id)
    else:
        session['route'] = str(0)

    if session['date'] == session['cur_date']:
        session['cur_time'] = str(datetime.now().strftime("%H:%M:%S"))
    else:
        session['cur_time'] = '00:00:00'
 
    df_bustop = get_bustop(conn)
    df_route = get_route(conn)
    df_time = get_time(conn, session['date'] + ' ' + session['cur_time'], session['bustop'], session['route'])
     
    # выводим страницу 
    html = render_template( 
        'index.html',
        user = session['user_id'],
        cur_date = session['cur_date'],
        date = session['date'],
        bustop = int(session['bustop']),
        route = int(session['route']),
        table_bustop = df_bustop,
        table_route = df_route,
        table_time = df_time,
        len = len 
    ) 
    return html 
