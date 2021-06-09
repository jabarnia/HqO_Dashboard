'''
=========================
This notebook reads the csv files downloaded 
from company website to access the google 
Location API to provide and find the amenities 
within the 5 minute walk of that building.

The vic function reads the lat and long, and 
returns a dictionary of data frames for each 
business type.
=========================
'''

import pandas as pd
import numpy as np
Google_key = '[GOOGLE_API_KEY]'
base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'

business_list = ['restaurant', 'cafe', 'bar', 'gym']

def vic(lat, long, rad = 400):
    vicinity = {}
    for b in business_list:
        url = f'{base_url}location={lat},{long}&radius={rad}&type={b}&key={Google_key}'
        response = requests.get(url)
        df = pd.json_normalize(response.json()['results'])
        df = df[df['business_status'] == 'OPERATIONAL']
        try:
            df = df[['name', 'rating', 'geometry.location.lng', 
                'geometry.location.lat', 'price_level']]
        except:
            df = df[['name', 'rating', 'geometry.location.lng', 
                'geometry.location.lat']]
        df.rename(columns = {'geometry.location.lat': 'LATITUDE', 'geometry.location.lng': 'LONGITUDE' })
        vicinity[b] = df
    return vicinity

def building_info(df_bld):
    try: 
        near_by = pd.read_pickle(''.join(["./", df_bld['NAME'], ".pkl"]))
    except:
        near_by = vic(df_bld['lat'], df_bld['long'])
        near_by.to_pickle(''.join(["./", df_bld['NAME'], ".pkl"]))
    for b in near_by.keys():
        df_bld[''.join([b, '_num'])] = len(near_by[b])
        df_bld[''.join([b, '_rating'])] = near_by[b]['rating'].mean()
        if b!= 'gym':
            df_bld[''.join([b, '_price'])] = near_by[b]['price_level'].mean()
    return df_bld