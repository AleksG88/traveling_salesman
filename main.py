import pandas as pd
from tsp import nearest_neighbor, route_length, neighbor_lists, two_opt, or_opt


data = pd.read_csv("data.csv")
points = list(zip(data["latitude_dd"], data["longitude_dd"]))
start = 3753

route = nearest_neighbor(points, start)
print("Жадный маршрут, скор" , route_length(points, route) / 100)

neighbors = neighbor_lists(points, 10)
route = two_opt(points, route, neighbors)
print("После 2-opt, длина маршрута:", route_length(points, route) / 100)

best_len = route_length(points, route)
while True:
    route = or_opt(points, route, neighbors)
    route = two_opt(points, route, neighbors)
    new_len = route_length(points, route)
    print("Or-opt + 2-opt, скор:", new_len / 100)
    if new_len >= best_len - 1e-9:
        break
    best_len = new_len
