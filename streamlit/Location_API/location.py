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
        df = df[['name', 'rating', 'geometry.location.lng', 
            'geometry.viewport.northeast.lat', 'price_level']]
        vicinity[b] = df
    return vicinity

