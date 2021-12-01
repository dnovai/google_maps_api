# Import packages
import pandas as pd
import googlemaps
import json


# Utilities

def get_address(gmaps, latitude, longitude):
    commune = ''
    province = ''
    region = ''
    country = ''

    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))

    if len(reverse_geocode_result[0]['address_components']) >= 4:
        commune = reverse_geocode_result[0]['address_components'][
            len(reverse_geocode_result[0]['address_components']) - 4]['long_name']
        province = reverse_geocode_result[0]['address_components'][
            len(reverse_geocode_result[0]['address_components']) - 3]['long_name']
        region = reverse_geocode_result[0]['address_components'][
            len(reverse_geocode_result[0]['address_components']) - 2]['long_name']
        country = reverse_geocode_result[0]['address_components'][
            len(reverse_geocode_result[0]['address_components']) - 1]['long_name']

    return commune, province, region, country


# Loading api key / credentials
with open('api_key.json') as json_file:
    data = json.load(json_file)
    api_key = data['api_key'][0]

# Load data
stations_df = pd.read_csv('stations.csv')

# Connect to google maps api by using api key
g = googlemaps.Client(key=api_key)

# Look up an addresses with reverse geocoding
unpacked_tuple_df = pd.DataFrame(
    stations_df.apply(
        lambda x: get_address(g, x['latitud'], x['longitud']),
        axis=1).tolist(), columns=['comuna', 'provincia', 'region', 'pais'], index=stations_df.index)
stations_df = pd.concat([stations_df, unpacked_tuple_df], axis=1)

# Save to *.csv file
stations_df.to_csv('stations_locations.csv', sep=';', index=False)
