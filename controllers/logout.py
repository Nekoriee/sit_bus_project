from app import app 
from flask import request, session, redirect, url_for, make_response

from utils import get_db_connection

@app.route('/logout', methods=['GET', 'POST']) 
def logout(): 
 
    conn = get_db_connection()
     
    # если пользователь авторизован 
    if request.cookies.get('user_id'):
        resp = make_response('')
        resp.set_cookie('user_id', '', expires=0)
        return resp
    
    redirect(url_for('index'))
