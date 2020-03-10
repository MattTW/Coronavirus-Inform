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

# last column is the lastest in the time series
latest_data_date = deaths_matrix.iloc[:,-1].name
print(f"This data is current as of {latest_data_date}")

# Now do the analysis
# Active = confirmed - deaths - recovered
# Deaths
shortest_confirmed_distance = 9999999999
shortest_confirmed_location = "Mars"
shortest_death_distance = 9999999999
shortest_death_location = "Mars"
one_hundred_mile_confirmed_total = 0
five_hundred_mile_confirmed_total = 0
one_hundred_mile_death_total = 0
five_hundred_mile_death_total = 0
# process confirmed
for index, row in confirmed_matrix.iterrows():
    current_corona_location = (row['Lat'], row['Long'])
    current_corona_distance = distance.distance(my_lat_and_long, current_corona_location).mi
    if row[latest_data_date] > 0 and current_corona_distance < shortest_confirmed_distance:
        shortest_confirmed_distance = current_corona_distance
        shortest_confirmed_location = row['Province/State']
    if current_corona_distance < 100 and row[latest_data_date] > 0:
        one_hundred_mile_confirmed_total += row[latest_data_date]
    if current_corona_distance < 500 and row[latest_data_date] > 0:
        five_hundred_mile_confirmed_total += row[latest_data_date]


# process deaths
for index, row in deaths_matrix.iterrows():
    current_corona_location = (row['Lat'], row['Long'])
    current_corona_distance = distance.distance(my_lat_and_long, current_corona_location).mi
    if row[latest_data_date] > 0 and current_corona_distance < shortest_death_distance:
        shortest_death_distance = current_corona_distance
        shortest_death_location = row['Province/State']
    if current_corona_distance < 100 and row[latest_data_date] > 0:
        one_hundred_mile_death_total += row[latest_data_date]
    if current_corona_distance < 500 and row[latest_data_date] > 0:
        five_hundred_mile_death_total += row[latest_data_date]


# print out some info
print(f"Uh oh, the closest confirmed Coronavirus case was found in {shortest_confirmed_location} which is only {shortest_confirmed_distance:.0f} miles from you!")
print(f"Yikes! The closest death was in {shortest_death_location} which is {shortest_death_distance:.0f} miles from you!")
print(f"There are {one_hundred_mile_confirmed_total} confirmed cases within 100 miles of you")
print(f"There are {five_hundred_mile_confirmed_total} confirmed cases within 500 miles of you")
print(f"There have been {one_hundred_mile_death_total} deaths within 100 miles of you")
print(f"There have been {five_hundred_mile_death_total} deaths within 500 miles of you")
