"""ПР 5.2: решение задачи коммивояжёра для населённых пунктов СФО."""

from pathlib import Path

import pandas as pd

from tsp import nearest_neighbor, route_length, neighbor_lists, two_opt, or_opt, distance



HERE = Path(__file__).parent


def main():
    """Строит маршрут и сохраняет его в solution.csv."""
    data = pd.read_csv(HERE / "data.csv")
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

    with open(HERE / "solution.csv", "w", encoding="utf-8") as f:
        for i in range(len(route) - 1):
            d = distance(points[route[i]], points[route[i + 1]])
            f.write(f"{i};{d}\n")
    print("сохранено строк:", len(route) - 1)


if __name__ == "__main__":
    main()
