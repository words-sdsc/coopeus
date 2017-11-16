#!/usr/bin/env python3
# coding: utf-8

# In[1]:

import json
from postgis import Point
from postgis.psycopg import register
import psycopg2
import requests


# In[2]:

r = requests.get('http://data.neonscience.org/api/v0/sites')
d = r.json()
#print(len(['data']))


# In[3]:

if 'data' in d and len(d['data']) > 0:
    connection = psycopg2.connect("dbname=geoserver user=etlfires")  
    register(connection)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM {}".format('neon_sites'))
    
    for site in d['data']:    
        #print(site['siteLongitude'])
        cursor.execute("""
INSERT INTO neon_sites (dataProducts, stateCode, siteType, siteDescription,
domainCode, siteCode, siteName, stateName, domainName, geom)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
            [json.dumps(site['dataProducts']), site['stateCode'], site['siteType'], 
            site['siteDescription'], site['domainCode'], site['siteCode'], 
            site['siteName'], site['stateName'], site['domainName'], 
            Point(x=site['siteLongitude'], y=site['siteLatitude'], srid=4326)])
        
    connection.commit()
    connection.close()


# In[4]:

#list(d['data'][0].keys())


# In[5]:

#for i in range(0, len(d['data'])):
#    print('{} {} {}'.format(d['data'][i]['d['data'][i]['siteLatitude'], d['data'][i]['siteLongitude']))


# In[6]:

#d['data'][0]


# In[ ]:



