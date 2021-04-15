import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pprint import pprint

if __name__ == '__main__':
    print(os.path.abspath(os.curdir))
    os.chdir("..")
    data = pd.read_csv("Datasets/winequality-red.csv")

    duplicate_rows = data[data.duplicated()]
    print("Is there duplicate rows: ", duplicate_rows.shape)

    if duplicate_rows.shape[0] > 10:
        data = data.drop_duplicates()