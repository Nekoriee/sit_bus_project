import pandas
from datetime import date

def get_bus(conn):
    return pandas.read_sql( 
    ''' 
        SELECT * FROM bus 
    ''', conn)

def get_driver(conn):
    return pandas.read_sql( 
    ''' 
        SELECT * FROM driver 
    ''', conn)

def get_trip(conn, dat):
    df = pandas.read_sql(''' 
    SELECT
            trip.trip_id,
            route.route_id,
            route.route_name,
            bus.bus_id,
            bus.bus_number,
            driver.driver_id,
            driver.driver_name,
            trip.trip_timestart,
            trip.trip_started
        FROM trip, route, bus, driver
        WHERE
            trip.bus_id = bus.bus_id
            AND trip.route_id = route.route_id
            AND trip.driver_id = driver.driver_id
            AND date(trip_timestart) = date(:date)
        ORDER BY route_name
''', conn, params={"date" : str(dat) + ' 12:00:00'})
    return df

def carry_trip(conn, date_target, date_source):
    cursor = conn.cursor()
    if get_trip(conn, date_target).empty:
        cursor.execute(''' 
        INSERT INTO trip (route_id, bus_id, driver_id, trip_timestart)
        SELECT
            trip.route_id as route_id,
            trip.bus_id as bus_id,
            trip.driver_id as driver_id,
            :date_target || ' 00:00:00' as trip_timestart
        FROM trip
        WHERE
            date(trip_timestart) = date(:date_source)
        ''', {"date_source" : date_source, "date_target" : date_target})
        conn.commit()

def update_trip(conn, trip_id, bus_id, driver_id, datetime):
    cursor = conn.cursor()
    cursor.execute(''' 
        UPDATE trip
        SET
            bus_id = :bus_id,
            driver_id = :driver_id,
            trip_timestart = :datetime,
            trip_started = 1
        WHERE
            trip_id = :trip_id
    ''', {"datetime" : datetime, "driver_id" : driver_id,
          "bus_id" : bus_id, "trip_id" : trip_id})
    conn.commit()
    
