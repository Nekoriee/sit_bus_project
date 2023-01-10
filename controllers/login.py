from app import app 
from flask import render_template, request, session, redirect, url_for, make_response

from utils import get_db_connection
from models.login_model import *

@app.route('/login', methods=['GET', 'POST']) 
def login(): 
 
    conn = get_db_connection()
    error = False
     
    # если пользователь авторизован 
    if request.cookies.get('user_id'):
        return redirect(url_for('index'))

    if request.form.get('user_id') and request.form.get('user_password'):
        user_id = request.form.get('user_id')
        user_password = request.form.get('user_password')
        print(user_id)
        print(user_password)
        resp = make_response(redirect(url_for('index')))
        if not check_user(conn, user_id, user_password).empty:
            resp.set_cookie('user_id', user_id)
            return resp
        else:
            error = True

    html_login = render_template(
        'login.html',
        error = error
    )
        
    return html_login

@app.route('/logout', methods=['GET', 'POST']) 
def logout(): 
 
    conn = get_db_connection()
     
    # если пользователь авторизован 
    if request.cookies.get('user_id'):
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('user_id', '', expires=0)
        return resp
    
    return(redirect(url_for('index')))

