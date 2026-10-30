"""Решение задачи комивояджера"""

import math
import numpy as np

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


def neighbor_lists(points, k):
    """дляя каждой точки список k ближайших к ней точек"""
    xs = np.array([p[0] for p in points])
    ys = np.array([p[1] for p in points])
    result = []
    for x, y in points:
        dists = np.hypot(xs - x, ys - y)
        nearest = np.argsort(dists)[1:k + 1]
        result.append(nearest.tolist())
    return result


def reverse_delta(points, route, x, y):
    """на сколько изменится длина, если перевернуть кусок route[x+1..y]"""
    a, b = route[x], route[x + 1]
    c = route[y]
    delta = distance(points[a], points[c]) - distance(points[a], points[b])
    if y + 1 < len(route):
        e = route[y + 1]
        delta += distance(points[b], points[e]) - distance(points[c], points[e])
    return delta


def two_opt(points, route, neighbors):
    """улучшение маршрута методом 2-opt."""
    n = len(route)
    improved = True
    while improved:
        improved = False
        pos = [0] * n
        for k, city in enumerate(route):
            pos[city] = k
        for i in range(n - 1):
            a, b = route[i], route[i + 1]
            for c in neighbors[a]:
                if distance(points[a], points[c]) >= distance(points[a], points[b]):
                    break
                j = pos[c]
                x, y = min(i, j), max(i, j)
                if y - x < 2:
                    continue
                if reverse_delta(points, route, x, y) < -1e-9:
                    route[x + 1:y + 1] = route[x + 1:y + 1][::-1]
                    for k in range(x + 1, y + 1):
                        pos[route[k]] = k
                    improved = True
                    break
    return route


def or_opt(points, route, neighbors, max_len=3):
    """улучшение маршрута переносом кусков из 1..max_len точек."""
    n = len(route)
    improved = True
    while improved:
        improved = False
        for seg_len in range(1, max_len + 1):
            pos = [0] * n
            for k, city in enumerate(route):
                pos[city] = k
            i = 1
            while i + seg_len <= n:
                p = route[i - 1]
                first = route[i]
                last = route[i + seg_len - 1]
                if i + seg_len < n:
                    q = route[i + seg_len]
                    gain_remove = (distance(points[p], points[first])
                                   + distance(points[last], points[q])
                                   - distance(points[p], points[q]))
                else:
                    gain_remove = distance(points[p], points[first])
                best = None
                for c in neighbors[first] + neighbors[last]:
                    j = pos[c]
                    for k in (j - 1, j):
                        if k < 0 or i - 1 <= k <= i + seg_len - 1:
                            continue
                        u = route[k]
                        v = route[k + 1] if k + 1 < n else None
                        for a, b in ((first, last), (last, first)):
                            add = distance(points[u], points[a])
                            if v is not None:
                                add += (distance(points[b], points[v])
                                        - distance(points[u], points[v]))
                            gain = gain_remove - add
                            if gain > 1e-9 and (best is None or gain > best[0]):
                                best = (gain, k, a == last)
                if best is not None:
                    _, k, rev = best
                    seg = route[i:i + seg_len]
                    if rev:
                        seg.reverse()
                    del route[i:i + seg_len]
                    ins = k + 1 if k < i else k + 1 - seg_len
                    route[ins:ins] = seg
                    for t, city in enumerate(route):
                        pos[city] = t
                    improved = True
                i += 1
    return route
