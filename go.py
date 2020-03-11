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

# data locations on Githb
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
combined_matrix = pd.DataFrame({'location': confirmed_matrix['Province/State'], 'latitude': confirmed_matrix['Lat'],
                                 'longitude': confirmed_matrix['Long'], 'deaths': deaths_matrix[latest_data_date],
                                 'recovered': recovered_matrix[latest_data_date]})
# Active = confirmed - deaths - recovered
combined_matrix['active'] = confirmed_matrix[latest_data_date] - combined_matrix.deaths - combined_matrix.recovered
combined_matrix['distance'] = combined_matrix.apply(calculate_distance, axis=1)

print(f"This data is current as of {latest_data_date}")

# Now do the analysis
closest_active_row = combined_matrix.loc[combined_matrix[(combined_matrix.active > 0)]['distance'].idxmin()]
print(f"The closest active Coronavirus case to you is {closest_active_row.distance:.0f} miles away in {closest_active_row.location}!")

closest_death_row = combined_matrix.loc[combined_matrix[combined_matrix.deaths > 0]['distance'].idxmin()]
print(f"The closest death to you is {closest_death_row.distance:.0f} miles away in {closest_death_row.location}!")

has_active_within_100_miles = combined_matrix[(combined_matrix.active > 0) & (combined_matrix.distance < 100)]
print(f"There are {has_active_within_100_miles.active.sum():.0f} active cases within 100 miles of you")

has_active_within_500_miles = combined_matrix[(combined_matrix.active > 0) & (combined_matrix.distance < 500)]
print(f"There are {has_active_within_500_miles.active.sum():.0f} active cases within 500 miles of you")

has_deaths_within_100_miles = combined_matrix[(combined_matrix.deaths > 0) & (combined_matrix.distance < 100)]
print(f"There are {has_deaths_within_100_miles.deaths.sum():.0f} deaths within 100 miles of you")

has_deaths_within_500_miles = combined_matrix[(combined_matrix.deaths > 0) & (combined_matrix.distance < 500)]
print(f"There are {has_deaths_within_500_miles.deaths.sum():.0f} deaths within 500 miles of you")
