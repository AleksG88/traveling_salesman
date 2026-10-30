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


def positions(route):
    """Справочник: на каком месте маршрута стоит каждая точка."""
    pos = [0] * len(route)
    for place, city in enumerate(route):
        pos[city] = place
    return pos


def segment_remove_gain(points, route, i, seg_len):
    """Сколько сэкономим, если вырезать кусок route[i..i+seg_len-1]."""
    p, first = route[i - 1], route[i]
    last = route[i + seg_len - 1]
    gain = distance(points[p], points[first])
    if i + seg_len < len(route):
        q = route[i + seg_len]
        gain += distance(points[last], points[q]) - distance(points[p], points[q])
    return gain


def insertion_slots(route, pos, neighbors, i, seg_len):
    """Щели рядом с соседями куска, куда его можно вставить."""
    first, last = route[i], route[i + seg_len - 1]
    slots = []
    for c in neighbors[first] + neighbors[last]:
        for k in (pos[c] - 1, pos[c]):
            if k >= 0 and not i - 1 <= k <= i + seg_len - 1:
                slots.append(k)
    return slots


def insertion_cost(points, u, v, a, b):
    """Сколько добавится, если вставить кусок a..b между u и v."""
    cost = distance(points[u], points[a])
    if v is not None:
        cost += distance(points[b], points[v]) - distance(points[u], points[v])
    return cost


def best_insertion(points, route, slots, segment, gain_remove):
    """Лучшая щель для куска: (номер щели, переворачивать ли) или (-1, False)."""
    best_k, best_rev, best_gain = -1, False, 1e-9
    for k in slots:
        u = route[k]
        v = route[k + 1] if k + 1 < len(route) else None
        for a, b in (segment, segment[::-1]):
            gain = gain_remove - insertion_cost(points, u, v, a, b)
            if gain > best_gain:
                best_k, best_rev, best_gain = k, a == segment[1], gain
    return best_k, best_rev


def move_segment(route, i, seg_len, k, rev):
    """Вырезать кусок route[i..i+seg_len-1] и вставить в щель k."""
    seg = route[i:i + seg_len]
    if rev:
        seg.reverse()
    del route[i:i + seg_len]
    ins = k + 1 if k < i else k + 1 - seg_len
    route[ins:ins] = seg


def or_opt(points, route, neighbors, max_len=3):
    """Улучшение маршрута переносом кусков из 1..max_len точек."""
    n = len(route)
    improved = True
    while improved:
        improved = False
        for seg_len in range(1, max_len + 1):
            pos = positions(route)
            i = 1
            while i + seg_len <= n:
                gain_remove = segment_remove_gain(points, route, i, seg_len)
                slots = insertion_slots(route, pos, neighbors, i, seg_len)
                segment = (route[i], route[i + seg_len - 1])
                k, rev = best_insertion(points, route, slots, segment, gain_remove)
                if k >= 0:
                    move_segment(route, i, seg_len, k, rev)
                    pos = positions(route)
                    improved = True
                i += 1
    return route
