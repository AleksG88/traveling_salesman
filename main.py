import pandas as pd
from tsp import nearest_neighbor, route_length, neighbor_lists


data = pd.read_csv("data.csv")
points = list(zip(data["latitude_dd"], data["longitude_dd"]))
start = 3753

route = nearest_neighbor(points, start)
print("Жадный маршрут, скор" , route_length(points, route) / 100)

neighbors = neighbor_lists(points, 10)
print(data["settlement"][neighbors[start]].tolist())
