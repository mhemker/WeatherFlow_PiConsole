""" Returns the WeatherFlow forecast variables required by the Raspberry Pi
Python console for WeatherFlow Tempest and Smart Home Weather stations.
Copyright (C) 2018-2020 Peter Davis

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

# Import required modules
from datetime   import datetime, date, timedelta, time
from lib        import observationFormat  as observation
from lib        import derivedVariables   as derive
from lib        import requestAPI
from kivy.clock import Clock
import requests
import bisect
import pytz
import time

def Download(metData,Config):

    """ Download the weather forecast data using the WeatherFlow BetterForecast
    API

    INPUTS:
        metData             Dictionary holding weather forecast data
        Config              Station configuration

    OUTPUT:
        metData             Dictionary holding weather forecast data
    """

    # Download latest forecast data
    Data = requestAPI.weatherflow.Forecast(Config)

    # Verify API response and extract forecast
    if requestAPI.weatherflow.verifyResponse(Data,'forecast'):
        metData['Dict'] = Data.json()['forecast']
    else:
        Clock.schedule_once(lambda dt: Download(metData,Config),600)
        if not 'Dict' in metData:
            metData['Dict'] = {}
    Extract(metData,Config)

    # Return metData dictionary
    return metData

def Extract(metData,Config):

    # Get current time in station time zone
    Tz = pytz.timezone(Config['Station']['Timezone'])
    Now = datetime.now(pytz.utc).astimezone(Tz)

    # Extract all forecast data from WeatherFlow JSON file. If  forecast is
    # unavailable, set forecast variables to blank and indicate to user that
    # forecast is unavailable
    try:
        metDict = (metData['Dict']['hourly'])
    except KeyError:
        metData['Time']    = Now
        metData['Temp']    = '--'
        metData['WindDir'] = '--'
        metData['WindSpd'] = '--'
        metData['Weather'] = 'ForecastUnavailable'
        metData['Precip']  = '--'
        metData['Valid']   = '--'

        # Attempt to download forecast again in 10 minutes and return
        # metData dictionary
        Clock.schedule_once(lambda dt: Download(metData,Config),600)
        return metData

    # Extract 'valid from' time of all available hourly forecasts, and
    # retrieve forecast for the current hourly period
    Times = list(hourlyForecast['time'] for hourlyForecast in metDict)
    metDict = metDict[bisect.bisect(Times,int(time.time()))]

    # Extract 'Valid' until time of forecast
    Valid = Times[bisect.bisect(Times,int(time.time()))]
    Valid = datetime.fromtimestamp(Valid,pytz.utc).astimezone(Tz)

    # Extract weather variables from DarkSky forecast
    Temp    = [metDict['air_temperature'],'c']
    WindSpd = [metDict['wind_avg'],'mps']
    WindDir = [metDict['wind_direction'],'degrees']
    Precip  = [metDict['precip_probability'],'%']
    Weather =  metDict['icon'].replace('cc-','')

    # Convert forecast units as required
    Temp = observation.Units(Temp,Config['Units']['Temp'])
    WindSpd = observation.Units(WindSpd,Config['Units']['Wind'])

    # Define and format labels
    metData['Time']    = Now
    metData['Valid']   = datetime.strftime(Valid,'%H:%M')
    metData['Temp']    = ['{:.1f}'.format(Temp[0]),Temp[1]]
    metData['WindDir'] = derive.CardinalWindDirection(WindDir)[2]
    metData['WindSpd'] = ['{:.0f}'.format(WindSpd[0]),WindSpd[1]]
    metData['Precip']  = '{:.0f}'.format(Precip[0])

    # Define weather icon
    if Weather == 'clear-day':
        metData['Weather'] = '1'
    elif Weather == 'clear-night':
        metData['Weather'] = '0'
    elif Weather == 'rainy':
        metData['Weather'] = '15'
    elif Weather == 'possibly-rainy-day':
        metData['Weather'] = '10'
    elif Weather == 'possibly-rainy-night':
        metData['Weather'] = '9'
    elif Weather == 'snow':
        metData['Weather'] = '27'
    elif Weather == 'possibly-snow-day':
        metData['Weather'] = '23'
    elif Weather == 'possibly-snow-night':
        metData['Weather'] = '22'
    elif Weather == 'sleet':
        metData['Weather'] = '18'
    elif Weather == 'possibly-sleet-day':
        metData['Weather'] = '17'
    elif Weather == 'possibly-sleet-night':
        metData['Weather'] = '16'
    elif Weather == 'thunderstorm':
        metData['Weather'] = '30'
    elif Weather == 'possibly-thunderstorm-day':
        metData['Weather'] = '29'
    elif Weather == 'possibly-thunderstorm-night':
        metData['Weather'] = '28'
    elif Weather == 'windy':
        metData['Weather'] = 'wind'
    elif Weather == 'foggy':
        metData['Weather'] = '6'
    elif Weather == 'cloudy':
        metData['Weather'] = '7'
    elif Weather == 'partly-cloudy-day':
        metData['Weather'] = '3'
    elif Weather == 'partly-cloudy-night':
        metData['Weather'] = '2'
    else:
        metData['Weather'] = 'ForecastUnavailable'

    # Return metData dictionary
    return metData