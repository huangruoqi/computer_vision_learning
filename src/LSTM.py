import pandas as pd
import numpy as np
import tensorflow as tf
import os

df = pd.read_csv(os.path.join("data", "1676004101.mp4.csv"))

groups = []

current_group_label = None
current_group = []
for row in df.itertuples():
    if current_group_label is None:
        current_group_label = row.label
    if current_group_label == row.label:
        current_group.append(row)
    else:
        current_group_label = row.label
        groups.append(current_group)
        current_group = []

if len(current_group):
    groups.append(current_group)

print(len(groups))