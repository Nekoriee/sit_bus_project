import pandas
from datetime import date

def get_bustop(conn):
    return pandas.read_sql( 
    ''' 
        SELECT * FROM bustop 
    ''', conn)

def get_route(conn):
    return pandas.read_sql( 
    ''' 
        SELECT * FROM route 
    ''', conn)

def get_time(conn, datetime, bustop, route):
    cursor = conn.cursor()
    cursor.execute(''' 
    DELETE FROM time;
    ''')
    if bustop == '0':
        bustop = '%'
    if route == '0':
        route = '%'
    cursor.execute(''' 
    INSERT INTO time
    SELECT
        bustop_route_id,
        trip_id,
        datetime(trip_timestart, '+' || bustop_route_movetime || ' minutes') as time_arrivetime
    FROM
        bustop_route
        JOIN trip on bustop_route.route_id = trip.route_id
    WHERE
        strftime('%s', time_arrivetime) > strftime('%s', :datetime)
        AND date(time_arrivetime) = date(:datetime)
        AND bustop_route.route_id LIKE :route
        AND bustop_route.bustop_id LIKE :bustop
        AND trip.trip_started = 1
    ''', {"bustop" : bustop, "route" : route, "datetime" : datetime})
    conn.commit()
    df_time = pandas.read_sql(
    ''' 
        SELECT
            route_name,
            bustop_name,
            bus_number,
            strftime('%H:%M', time_arrivetime) as time_arrivetime
        FROM
            time
            JOIN trip on time.trip_id = trip.trip_id
            JOIN bustop_route on time.bustop_route_id = bustop_route.bustop_route_id
            JOIN route on bustop_route.route_id = route.route_id
            JOIN bustop on bustop_route.bustop_id = bustop.bustop_id
            JOIN bus on trip.bus_id = bus.bus_id
        ORDER BY route_name, bus_number, time_arrivetime
    ''', conn)
    return df_time
