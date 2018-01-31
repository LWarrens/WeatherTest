import sys
sys.path.append("../")
import weather

most_similar_date = weather.get_most_similar_date("../data/1089419.csv", "../data/1089441.csv")

print most_similar_date