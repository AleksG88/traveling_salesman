"""Решение задачи комивояджера"""

import math

def distance(p1, p2):
    """Квклидово расстояние мужду точками"""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
