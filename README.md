# Coronavirus-Inform
Give a user some info on Coronavirus COVID-19 cases near their location

## Installation
* Install Python 3.6 or newer
* Clone this repository
* ```pip3 install -r requirements.txt```
* ```python3 go.py```

If you get SSL errors, run the Install Certificates command that comes with your python install.   On a Mac with Python 3, run ```/Applications/Python\ 3.7/Install\ Certificates.command ```

If python 3 is your default python, ```pip``` and ```python``` will work just fine too.

You can be pretty generic answering the location prompt.  A city and state is usually enough.  Well known landmarks will work too.

```
Where you at? Des Moines, IA
Your latitude and longitude: (41.5910641, -93.6037149)
This data is current as of 3/10/20
The closest active Coronavirus case to you is 35 miles away in Iowa!
The closest death to you is 832 miles away in Santa Rosa County, FL!
There are 9 active cases within 100 miles of you
There are 73 active cases within 500 miles of you
There are 0 deaths within 100 miles of you
There are 0 deaths within 500 miles of you


Where you at? statue of liberty
Your latitude and longitude: (40.689253199999996, -74.04454817144321)
This data is current as of 3/10/20
The closest active Coronavirus case to you is 3 miles away in New York County, NY!
The closest death to you is 16 miles away in Bergen County, NJ!
There are 191 active cases within 100 miles of you
There are 588 active cases within 500 miles of you
There are 2 deaths within 100 miles of you
There are 2 deaths within 500 miles of you