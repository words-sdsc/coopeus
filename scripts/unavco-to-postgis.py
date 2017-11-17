#!/usr/bin/env python3

import io
import json
import pandas
from postgis import Point
from postgis.psycopg import register
import psycopg2
import requests

r = requests.get('http://web-services.unavco.org/internalWS/gps/metadata/stationcoordinate/sites/beta?project=PBO&refframe=igs08&verboseheader=true&stddev=false')

# set engine to python for regex separator
df = pandas.read_csv(io.StringIO(r.text), skiprows=5, sep='\s*,\s*', engine='python')
#print(len(['data']))

if df.size > 0:
    connection = psycopg2.connect("dbname=geoserver user=etlfires")  
    register(connection)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM {}".format('unavco_sites'))

    for idx, row in df.iterrows():
        #print(site['siteLongitude'])
        cursor.execute("""
INSERT INTO unavco_sites (id, stationName, epoch, referenceFrame, geom)
VALUES (%s, %s, %s, %s, %s)""", 
            [row['# ID'], row['Station Name'], row['Epoch'], row['Reference Frame'],
            Point(x=row['Longitude (deg)'], y=row['Latitude (deg)'], z=row['Ellipsoidal Elevation (m)'], srid=4326)])
        
    connection.commit()
    connection.close()
