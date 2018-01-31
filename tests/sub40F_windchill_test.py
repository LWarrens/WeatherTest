import sys
sys.path.append("../")
import weather
result = weather.get_sub40F_wind_chill("1/22/17", "../data/1089419.csv")

print result