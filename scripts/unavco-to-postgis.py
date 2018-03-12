#!/usr/bin/python3

import io
import json
import pandas
from postgis import Point
from postgis.psycopg import register
import psycopg2
import requests

r2 = requests.get('http://www.unavco.org/gsacws/gsacapi/site/search?output=site.csv&site.group=PBO+Analysis+Complete&site.sortorder=ascending&limit=99999')
df2 = pandas.read_csv(io.StringIO(r2.text), skiprows=1, header=None,
  names=['id', 'stationName', 'lat', 'lon', 'elev', 'startTime', 'stopTime'],sep='\s*,\s*', engine='python')

merged_df = df2
#print(merged_df.columns)

if merged_df.size > 0:
    connection = psycopg2.connect("dbname=geoserver user=etlfires")  
    register(connection)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM {}".format('unavco_sites'))

    for idx, row in merged_df.iterrows():
        #print(site['siteLongitude'])
        #print(row)
        cursor.execute("""
INSERT INTO unavco_sites (id, stationName, startTime, stopTime, geom)
VALUES (%s, %s, %s, %s, %s)""",
            [row['id'], row['stationName'], 
            row['startTime'] + 'Z', row['stopTime'] + 'Z',
            Point(x=row['lon'], y=row['lat'], z=row['elev'], srid=4326)])
        
    connection.commit()
    connection.close()
