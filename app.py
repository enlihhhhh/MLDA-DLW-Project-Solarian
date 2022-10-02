
# import libraries
import streamlit as st
import pandas as pd
from patchify import patchify
import pydeck as pdk
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
st.set_option('deprecation.showPyplotGlobalUse', False)
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

################################################################################################################################

# Introductory write-up for our app
title = st.container()
with title:
  st.title("Welcome to Solarian")
  st.write("----")
  st.header("How it works: ")
  st.markdown("- Input a location ( via address or longtitude/langtitude ).")
  st.markdown("- Take a screenshot ( using our button ) of the specific area which will be ran through our Machine Learning model. ")
  st.markdown("- Choose the patch of image that best represents the area you want the statistics of. ")
  st.markdown("- We will return you information such as: Surface area of rooftops/flat surfaces in image and money saved by installing commercial solar panels there.")
  st.write("----")

################################################################################################################################

# section for getting user input ( address OR lang/long )
userInput = st.container()
with userInput:

  # intialise 2 columns
  col1, col2 = st.columns(2)

  # initialise langitude and longitude variables
  lat= 0.0
  lon = 0.0
  lat_2 = 0.0
  lon_2 = 0.0
  
  # create pandas dataframe and array for lan and lon
  df = pd.DataFrame()
  coord = [0,0]
  lowest = 100

  # user input via lang/long
  col1.subheader("Find Current Location")
  col1.write("Please Enter the Longitude and Latitude of your current location")
  lat = col1.number_input("Enter Latitude: ", 
    min_value = -90.0, 
    max_value = 90.0, 
    value = 1.3521,
    step = 1e-4,
    format = "%.4f")

  lon= col1.number_input("Enter Longitude: ",
      min_value = -180.0, 
      max_value = 180.0,
      value = 103.8198,
      step = 1e-4,
      format = "%.4f")
  
  if col1.button('Confirm Longitude and Latitude'):
      df = df.append({'Latitude' : lat, 'Longitude' : lon},ignore_index = True)
      coord[0] = lat
      coord[1] = lon

# user input via address
  col2.subheader("Find Latitude and Longitude using Street")
  col2.write("Enter the details of your desired location")
  street = col2.text_input("Street", placeholder="E.g. 50 Nanyang Ave")
  city = col2.text_input("City", "Singapore")
  province = col2.text_input("Province", "Singapore")
  country = col2.text_input("Country", "Singapore")

  geolocator = Nominatim(user_agent="GTA Lookup")
  geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
  location = geolocator.geocode(street+", "+city+", "+province+", "+country)

  try:
      lat_2 = location.latitude
      lon_2 = location.longitude
      formatted_lat = "{:.4f}".format(location.latitude)
      formatted_lon = "{:.4f}".format(location.longitude)

  except AttributeError:
      col2.warning("Error in Input, Please Try Again")
      col2.stop()

  if col2.button('Confirm Street Name'):
      df = df.append({'Latitude' : lat_2, 'Longitude' : lon_2},ignore_index = True)
      col2.markdown("The Latitude and Longitude of your selected location are " 
      + formatted_lat + "," + formatted_lon)
      coord[0] = lat_2
      coord[1] = lon_2

  try:
      st.header("Please crop out the map using a snipping tool and upload the file")
      st.pydeck_chart(pdk.Deck(
          map_style='mapbox://styles/mapbox/satellite-v9', 
          api_keys = {'mapbox':'pk.eyJ1IjoidW5pY29ybnByZXNpZGVudCIsImEiOiJjbDhyN3F2MTcwNm16M3JwY29zb3VweDV6In0.3E3EjkupKg50fx5qLwxWEw' },
          initial_view_state=pdk.ViewState(
              latitude=df.iloc[0]['Latitude'],
              longitude=df.iloc[0]['Longitude'],
              zoom=18,
              pitch = 0)
      ))
      
  except IndexError:
      st.stop()

################################################################################################################################

st.subheader("Please move to next page 'map' after snipping the image of the map")