import sys
sys.path.append("../")
import weather

result = weather.get_daylight_temperature("2/22/17", "../data/1089419.csv")

print result