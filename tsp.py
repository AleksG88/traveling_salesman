"""Решение задачи комивояджера"""

import math

def distance(p1, p2):
    """Квклидово расстояние мужду точками"""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def nearest_neighbor(points, start):
    """жадный алгоритм каждый раз ищем ближайшую точку."""
    n = len(points)
    visited = [False] * n
    visited[start] = True
    route = [start]
    current = start
    for _ in range(n - 1):
        best = -1
        best_dist = math.inf
        for i in range(n):
            if not visited[i]:
                d = distance(points[current], points[i])
                if d < best_dist:
                    best_dist = d
                    best = i
        route.append(best)
        visited[best] = True
        current = best
    return route


def route_length(points, route):
    """общая длина маршрута"""
    total = 0
    for i in range(len(route) - 1):
        total += distance(points[route[i]], points[route[i + 1]])
    return total
