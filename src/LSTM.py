import pandas as pd
import numpy as np
import tensorflow as tf
import os

df = pd.read_csv(os.path.join("data", "1676004101.mp4.csv"))

for row in df.itertuples():
    print(row.v20)
    break