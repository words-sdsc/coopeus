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
df = pandas.read_csv(io.StringIO(r.text), skiprows=6, header=None, names=['id', 'stationName', 'lat', 'lon',
       'elev', 'epoch', 'referenceFrame'], sep='\s*,\s*', engine='python')
#print(len(['data']))


r2 = requests.get('http://www.unavco.org/gsacws/gsacapi/site/search?output=site.csv&site.group=PBO+Analysis+Complete&site.sortorder=ascending&limit=99999')
df2 = pandas.read_csv(io.StringIO(r2.text), skiprows=1, header=None,
  names=['id', 'stationName', 'lat', 'lon', 'elev', 'startTime', 'stopTime'],sep='\s*,\s*', engine='python')
df2 = df2.drop(['lat', 'lon', 'elev'], axis=1)


# In[60]:

merged_df = pandas.merge(df, df2, on=['id', 'stationName'])


# In[66]:

if merged_df.size > 0:
    connection = psycopg2.connect("dbname=geoserver user=etlfires")  
    register(connection)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM {}".format('unavco_sites'))

    for idx, row in merged_df.iterrows():
        #print(site['siteLongitude'])
        cursor.execute("""
INSERT INTO unavco_sites (id, stationName, epoch, referenceFrame, startTime, stopTime, geom)
VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            [row['id'], row['stationName'], row['epoch'] + 'Z', row['referenceFrame'],
            row['startTime'] + 'Z', row['stopTime'] + 'Z',
            Point(x=row['lon'], y=row['lat'], z=row['elev'], srid=4326)])
        
    connection.commit()
    connection.close()
