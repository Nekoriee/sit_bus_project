import pandas

def check_user(conn, login, password):
    return pandas.read_sql( 
    ''' 
        SELECT
            *
        FROM
            user
        WHERE
            user_login = :login
            AND user_password = :password
    ''', conn, params={"login" : login, "password" : password})
