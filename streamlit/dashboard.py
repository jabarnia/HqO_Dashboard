# importing the packages we are going to use:

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt
import holoviews as hv
import hvplot.pandas

import geopandas as gpd 
from shapely.geometry import Point 

from plots import plot
from Location_API import location


df_buildings = pd.read_csv('DIM_BUILDING.csv')
df_buildings.dropna(subset = ['LATITUDE','LONGITUDE'], inplace = True)
city_bound = gpd.read_file('tl_2020_us_uac10.shp')
df_data = pd.read_csv('df_users.csv')
chicago_bound = gpd.read_file('Chicago/geo_export_ea2f6836-36fc-4f46-aa50-277ef4914884.shp')

df_buildings['geometry'] = df_buildings.apply(lambda x: Point( x['LONGITUDE'] , x['LATITUDE']), axis = 1)
gdf_buildings = gpd.GeoDataFrame(df_buildings, geometry = 'geometry')
gdf_buildings.crs = {'init' :'epsg:4326'}
nl = '\n'

'''
sample list of amenities, building names, cities, and possible comparison choices. 
In the final product, the building list should reflect budilings that the user has in their portfolio
'''

amen_list = ['Amenities', 'Retail/Restaurants', 'Location','Sustainabiliy', 'Maintenance', 'Security', 'Other']
building_list = ['All HqO Buildings', 'My Portfolio', 'HqO Park', 'Willis Tower', 'Yellow Business Center']
city_list = ['Worldwide', 'Austin, TX', 'Chicago, IL', 'New York, NY']
comparelist = ['Buidings of similar size', 'Buildings in the same city', 'Buildings in my portfolio']



business_list = ['restaurant', 'cafe', 'bar', 'gym']
city_tags = ['Chicago, IL':3, 'Austin, TX': 7]




'''
The two colors that have been used in the plots - one for the actual selection 
and the other to represent what it is being compared againts
'''

color_select = '#f67171'
color_compare = '#bfbfbf'



#Let's start the streamlit page.


st.set_page_config(layout="wide")

st.sidebar.write('# **HqO Benchmark**' )
st.sidebar.write('### TDI Capstone - Shiva Jabarnia')
    

#drop down menus on the side to pick what is to be shown


def selection(df, sel, compare_to):
    if compare_to == comparelist[0]:
        return None
    if not sel:
        sel = df[df['NAME'] == 'Willis Tower']
    if compare_to == comparelist[1]:
        area = sel['AREA'].iloc[0]
        df_non_na = df.dropna(subset = ['AREA'])
        ind = df_non_na[ df_non_na['AREA'] > (area*0.7) ]
        return (ind)
    if compare_to == comparelist[2]:
        city = sel['CITY'].iloc[0]
        df_non_na = df.dropna(subset = ['CITY'])
        ind = df_non_na[ df_non_na['CITY'] == city ]
        return (ind)
    if compare_to == comparelist[3]:
        port = sel['PORTFOLIO'].iloc[0]
        df_non_na = df.dropna(subset = ['PORTFOLIO'])
        ind = df_non_na[ df_non_na['PORTFOLIO'] == port ]
        return (ind)
    return None


#making the picks for what data to show and what to compare to.


building = building_list[0]
city = city_list[0]
city = st.sidebar.selectbox('Location', city_list)
building = st.sidebar.selectbox('Selection', building_list)


'''
df_draw is going to be our main source here for the plots. We are looking at what 
the user has picked, to make the approporiate selection from df_data. If no selection
has been made, the default values should not trigger any of these if clauses.
'''

if building != building_list[0]:
    df_draw = gdf_buildings[gdf_buildings['NAME'] == building]
elif city != city_list[0]:
    df_draw = df_data[ df_data['city'] == city_tags[city]]
else:
    df_draw = df_data

st.sidebar.markdown('---')

'''
Compare button will set a bolean to set whether the user wants to see only the data 
from the set they have selected or if they want to compare that to other items.
''' 
compare_against = st.sidebar.selectbox('Compare Against:', comparelist)
Compare = st.sidebar.button('Compare', key='Compare')

'''
right now I only have the base to compare against buildings in chicago
in future iterations, there will be a function to create df_compare based 
on the user input
'''

df_compare = df_data[ df_data['city'] == city_tags['Chicago, IL']]


#breaking up the board into vertical coulumns to have things organized!
row1_1, w1, row1_2 = st.beta_columns((4,1,17))

with row1_1:
    polar_labels = ['Marketing and Branding', 
                                'Maintanance                 ', 
                                'Security         ', 
                                'Building Amenities', 
                                '                    Deals and Perks', 
                                '                        Digital Experience']
    vals = df_draw[['Marketing_Branding_imp','Maintanance_imp',	'Security_imp',	
        'Amenities_imp','Deals_Perks_imp','Digital_Experience_imp']].mean(axis = 0).tolist()

    polar_df = pd.DataFrame({'Col A': polar_labels,
                            'Col B': vals})

    st.pyplot(plot.polar_plot(polar_df))

with row1_2:
    st.write('')

    if not Compare:
        p = plot.draw_user_for_selection(df_draw, color_select)
        g = plot.draw_amen_selection(df_draw, color_select)
        st.bokeh_chart(hv.render(p+g))

    if Compare:

        p2 = plot.draw_user_compare(df_compare, color_compare)
        g2 = plot.draw_amen_selection(df_compare, color_compare)

        p1 = plot.draw_user_for_selection(df_draw, color_select) 
        g1 = plot.draw_amen_compare(df_draw, color_select)

        p = p1 * p2
        g = g1 * g2
    
        try:
            st.bokeh_chart(hv.render(p+g))
        except:
            st.bokeh_chart(hv.render(p + g1))

        


row2_1, row2_2, row2_3 = st.beta_columns((4,1,15))

with row2_3:
    # drawing the world map
    if city == city_list[0]:
        st.pydeck_chart(pdk.Deck(
                map_style = 'mapbox://styles/shivajabarnia/ckoj9yu57030u19qic2w2dztl',
                initial_view_state=pdk.ViewState(
                    latitude=35,
                    longitude=-45,
                    zoom=2,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data= df_buildings[['LONGITUDE', 'LATITUDE']],
                        get_position='[LONGITUDE, LATITUDE]',
                        filled = True,
                        getRadius = 1,
                        radiusMinPixels = 2,
                        getFillColor = [255,0,0],
                        pickable=True,
                        extruded=False,
                    )
                ], 
            ))

    else:
        if building == building_list[0]:
            # drawing the world map
            if city == city_list[0] :
                st.pydeck_chart(pdk.Deck(
                    map_style = 'mapbox://styles/shivajabarnia/ckoj9yu57030u19qic2w2dztl',
                    initial_view_state=pdk.ViewState(
                        latitude=35,
                        longitude=-45,
                        zoom=2,
                    ),
                    layers=[
                        pdk.Layer(
                            'ScatterplotLayer',
                            data= df_buildings[['LONGITUDE', 'LATITUDE']],
                            get_position='[LONGITUDE, LATITUDE]',
                            filled = True,
                            getRadius = 1,
                            radiusMinPixels = 2,
                            getFillColor = [255,0,0],
                            pickable=True,
                            extruded=False,
                        )
                    ], 
                ))

            else:
                #drawing the city map

                city_bound_selected = city_bound[city_bound['NAME10'] == 'Chicago, IL--IN']
                multicoords = [list(line.coords) for line in chicago_bound['geometry'].boundary.iloc[0]]

                center = city_bound_selected['geometry'].centroid.iloc[0]

                #selecting only buildings that fall into the limits of this city

                selected_buildings = gdf_buildings[gdf_buildings['geometry']/
                            .within(city_bound_selected['geometry'].iloc[0])]
                center = city_bound_selected['geometry'].centroid.iloc[0]
                
                ciy_poly = pdk.Layer(
                    "PolygonLayer",
                    multicoords,
                    opacity=0.01,
                    get_polygon='-',
                    filled=True,
                    get_fill_color=[255, 0, 0],
                    )

                ciy_line = pdk.Layer(
                    "PolygonLayer",
                    multicoords,
                    opacity=1,
                    stroked=True,
                    filled=False,
                    get_polygon='-',
                    get_line_color=[0, 0, 0]
                    )

                building_points = pdk.Layer(
                    'ScatterplotLayer',
                    data= selected_buildings[['LONGITUDE', 'LATITUDE']],
                    get_position='[LONGITUDE, LATITUDE]',
                    filled = True,
                    getRadius = 1,
                    radiusMinPixels = 3,
                    getFillColor = [255,0,0],
                    pickable=True,
                    extruded=False
                    )

                st.pydeck_chart(pdk.Deck(
                    map_style="https://openmaptiles.org/styles/#toner",
                    initial_view_state=pdk.ViewState(
                        latitude=41.881476,
                        longitude=-87.626670,
                        zoom=9,
                        #height = 1200
                    ),
                    layers=[ciy_line, ciy_poly, building_points]
                ))
        #drawing building map
        if building != building_list[0]:
            nearby = location.vic(df_draw['lat'], df_draw['long'])
            d_s = gdf_buildings[gdf_buildings['NAME'] == building].copy()
            #building point
            b_p = pdk.Layer(
                    'ScatterplotLayer',
                    data= d_s[['LONGITUDE', 'LATITUDE']],
                    get_position='[LONGITUDE, LATITUDE]',
                    filled = True,
                    getRadius = 10,
                    radiusMinPixels = 5,
                    getFillColor = [0,0,0],
                    pickable=True,
                    extruded=False
                    )

            #5 minute walk 400 meters
            b_r = pdk.Layer(
                    'ScatterplotLayer',
                    data= d_s[['LONGITUDE', 'LATITUDE']],
                    get_position='[LONGITUDE, LATITUDE]',
                    filled = False,
                    stroked=True,
                    getRadius = 400,
                    line_width_min_pixels = 2,
                    get_line_color = [200,200,200],
                    pickable=True,
                    extruded=False
                    )
            
            #nearby amenities as a scatter plot
            nearby = []
            map_colors = [[225,0,0], [255, 128, 0], [255, 0, 255], [0,128, 255]]

            for i in range(len(business_list)):
                b = business_list[i]
                new_layer = pdk.Layer(
                        'ScatterplotLayer',
                        data= nearby[b][['LONGITUDE', 'LATITUDE']],
                        get_position='[LONGITUDE, LATITUDE]',
                        filled = True,
                        getRadius = 10,
                        radiusMinPixels = 5,
                        getFillColor = map_colors[i],
                        pickable=True,
                        extruded=False
                        )
                near_by.append(new_layer)
            
            
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=41.878881,
                    longitude=-87.636516,
                    zoom=15
                ),
                layers=[b_p, b_r] + near_by
            ))
