import pandas as pd
from tsp import distance

data = pd.read_csv("data.csv")
print(data.head())
print("Всего пунктов:", len(data))
print(distance((5601, 9285), (5661, 9621)))
