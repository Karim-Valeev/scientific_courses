import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pprint import pprint

if __name__ == '__main__':
    print(os.path.abspath(os.curdir))
    os.chdir("..")
    data = pd.read_csv("Datasets/winequality-red.csv")

    cols = data.columns.tolist()
    #Checking for Detecting Outliers
    plt.subplots(figsize=(20,15))
    boxplot = data.boxplot(column=cols)
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    print(IQR)
    #removing Out liers
    data = data[~((data < (Q1 - 1.5 * IQR)) |(data > (Q3 + 1.5 * IQR))).any(axis=1)]