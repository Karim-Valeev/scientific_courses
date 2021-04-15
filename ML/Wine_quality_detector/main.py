from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

from sklearn.preprocessing import LabelEncoder
from pprint import pprint

import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print(os.path.abspath(os.curdir))
    os.chdir("..")
    df = pd.read_csv("Datasets/winequality-red.csv")
    # pprint(data.head())
    # print(data["alcohol"])
    # print(type(data["alcohol"]), '\n')
    # print(data.dtypes)
    print(df.info(), '\n')

    # Лучше всегда проверять на наличие Null и Дубликатов
    # data.columns.isna()
    # data.isin([' ?']).sum()
    print("Is there null values: ", df.isnull().values.any())

    duplicate_rows = df[df.duplicated()]
    print("Is there duplicate rows: ", duplicate_rows.shape)

    if duplicate_rows.shape[0] > 10:
        df = df.drop_duplicates()

    # sns.set()
    # fig = plt.figure(figsize=[15, 20])
    # cols = ['quality']
    # cnt = 1
    # for col in cols:
    #     plt.subplot(4, 3, cnt)
    #     sns.boxplot(data=data, y=col)
    #     cnt += 1
    # plt.show()

    df['quality'] = ['good' if i >= 7 else 'bad' for i in df['quality']]

    categorical_df = df.select_dtypes(include=['object'])
    categorical_df.columns

    enc = LabelEncoder()

    categorical_df = categorical_df.apply(enc.fit_transform)
    categorical_df.head()

    df = df.drop(categorical_df.columns, axis=1)

    df = pd.concat([df, categorical_df], axis=1)

    print("BEFORE:", df.head(), '\n')

    #     Standartisation
    X = df.drop('quality', axis=1)
    y = df['quality']

    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)

    print("AFTER: ", df.head(), '\n')

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

    from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold, learning_curve

    # Cross validate model with Kfold stratified cross val
    kfold = StratifiedKFold(n_splits=5)

    #     Logistic Regression

    def_lr = LogisticRegression()
    def_lr.fit(X_train, y_train)

    lr_pred = def_lr.predict(X_test)

    print("Logistic Regression accuracy: ", accuracy_score(y_test, lr_pred))

# cols = data.columns.tolist()
# #Checking for Detecting Outliers
# plt.subplots(figsize=(20,15))
# boxplot = data.boxplot(column=cols)
# Q1 = data.quantile(0.25)
# Q3 = data.quantile(0.75)
# IQR = Q3 - Q1
# print(IQR)
# #removing Out liers
# data = data[~((data < (Q1 - 1.5 * IQR)) |(data > (Q3 + 1.5 * IQR))).any(axis=1)]
