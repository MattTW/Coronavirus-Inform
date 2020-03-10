import urllib.request as request
import pandas as pd
from geopy.geocoders import Nominatim
from geopy import distance


# get users location and convert into lat/long
my_location = input("Where you at? ")
geolocator = Nominatim(user_agent="corona-inform")
my_geocoded_location = geolocator.geocode(my_location)
my_lat_and_long = (my_geocoded_location.latitude, my_geocoded_location.longitude)
print(f"Your latitude and longitude: {my_lat_and_long}")

# here is where the data is at
COVID_19_github_prefix = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-"
confirmed_url = COVID_19_github_prefix + "Confirmed.csv"
deaths_url = COVID_19_github_prefix + "Deaths.csv"
recovered_url = COVID_19_github_prefix + "Recovered.csv"

# read them each into a matrix
confirmed_matrix = pd.read_csv(confirmed_url)
deaths_matrix = pd.read_csv(deaths_url)
recovered_matrix = pd.read_csv(recovered_url)

def calculate_distance(row):
    return distance.distance((row['latitude'], row['longitude']), my_lat_and_long).miles

# last column is the lastest in the time series
latest_data_date = confirmed_matrix.iloc[:,-1].name

# build a new matrix that combines the data we want
# location, lat/long columns plus last date in the timer series for each and give it an appropriate name.   
# Instead of confirmed column create active column
combined_matrix = pd.DataFrame({'location': confirmed_matrix['Province/State'], 'latitude': confirmed_matrix['Lat'],
                                 'longitude': confirmed_matrix['Long'], f'deaths': deaths_matrix[latest_data_date],
                                 f'recovered': recovered_matrix[latest_data_date]})
# Active = confirmed - deaths - recovered
combined_matrix['active'] = confirmed_matrix[latest_data_date] - combined_matrix.deaths - combined_matrix.recovered
combined_matrix['distance'] = combined_matrix.apply(calculate_distance, axis=1)
print(combined_matrix)

print(f"This data is current as of {latest_data_date}")

# Now do the analysis
print(combined_matrix['distance'].min())
# Deaths
has_death = combined_matrix['deaths'] > 0
closest_death_row = combined_matrix.loc[combined_matrix[has_death]['distance'].idxmin()]
print(f"The closest death to you is {closest_death_row['distance']:.0f} miles away in {closest_death_row['location']}!")
# shortest_confirmed_distance = 9999999999
# shortest_confirmed_location = "Mars"
# shortest_death_distance = 9999999999
# shortest_death_location = "Mars"
# one_hundred_mile_confirmed_total = 0
# five_hundred_mile_confirmed_total = 0
# one_hundred_mile_death_total = 0
# five_hundred_mile_death_total = 0

# # process confirmed
# for index, row in confirmed_matrix.iterrows():
#     current_corona_location = (row['Lat'], row['Long'])
#     current_corona_distance = distance.distance(my_lat_and_long, current_corona_location).mi
#     if row[latest_data_date] > 0 and current_corona_distance < shortest_confirmed_distance:
#         shortest_confirmed_distance = current_corona_distance
#         shortest_confirmed_location = row['Province/State']
#     if current_corona_distance < 100 and row[latest_data_date] > 0:
#         one_hundred_mile_confirmed_total += row[latest_data_date]
#     if current_corona_distance < 500 and row[latest_data_date] > 0:
#         five_hundred_mile_confirmed_total += row[latest_data_date]


# # process deaths
# for index, row in deaths_matrix.iterrows():
#     current_corona_location = (row['Lat'], row['Long'])
#     current_corona_distance = distance.distance(my_lat_and_long, current_corona_location).mi
#     if row[latest_data_date] > 0 and current_corona_distance < shortest_death_distance:
#         shortest_death_distance = current_corona_distance
#         shortest_death_location = row['Province/State']
#     if current_corona_distance < 100 and row[latest_data_date] > 0:
#         one_hundred_mile_death_total += row[latest_data_date]
#     if current_corona_distance < 500 and row[latest_data_date] > 0:
#         five_hundred_mile_death_total += row[latest_data_date]


# # print out some info
# print(f"Uh oh, the closest confirmed Coronavirus case was found in {shortest_confirmed_location} which is only {shortest_confirmed_distance:.0f} miles from you!")
# print(f"Yikes! The closest death was in {shortest_death_location} which is {shortest_death_distance:.0f} miles from you!")
# print(f"There are {one_hundred_mile_confirmed_total} confirmed cases within 100 miles of you")
# print(f"There are {five_hundred_mile_confirmed_total} confirmed cases within 500 miles of you")
# print(f"There have been {one_hundred_mile_death_total} deaths within 100 miles of you")
# print(f"There have been {five_hundred_mile_death_total} deaths within 500 miles of you")
