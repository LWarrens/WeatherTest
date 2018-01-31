# WeatherTest
# Read Me

# Requirements
Python >=2.7.9 and the Python Pandas module are required to use this library.
To install python >=2.7.9, visit
https://www.python.org/download/releases/2.7/

After having the Python 2.x distribution installed, you can install the Pandas module by running this command in the Python home directory
python -m pip install pandas

To run, clone the repository or unzip the .zip distribution of this repository.
The test can be run from their respective folders relatively, otherwise the project should be treated as a simple python module.
The provided test/examples present the usage of this library, with the user functionality being provided by get_daylight_temperature, get_sub40F_wind_chill, and get_most_similar_day in the weather.py file.

# Similarity metric
The reasoning behind the chosen similarity metric.
In developing a similarity metric, I chose to use columns that were not sparsely populated.
If those columns were used when variables were not present, there would be days that similarity could not be calculated.
The name of the station and location information(longitude / latitude / elevation) do not offer much in explaining the variance for environmental conditions, so they were not considered for this metric.
Wind speed is represented by the day's windchill, this prevents the Euclidean distance measure from placing too much importance on wind conditions while accounting for what a human would perceive as a similar day.
Humidity is represented by the dew point temperature instead of the relative humidity because the dew point temperature is absolute, captures humidity in its definition, and is on a similar scale to most of the other variables selected for the similarity metric.
Altimeter Setting was used over station pressure because it reads at a mean sea level, unlike station pressure.
The formulation for the similarity index is currently
(WindchillTemperatureF^2 + DryBulbTemperatureF^2 + WetBulbTemperatureF^2 + DewPointTemperatureF^2 + AltimeterSetting^2)^.5

# Results
With current files, results for most similar date should be "02/19/17"
