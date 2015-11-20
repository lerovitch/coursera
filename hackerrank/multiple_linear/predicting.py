from sklearn import linear_model

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt


def main(fst):
    lines = fst.readlines()
    features_m = lines.pop(0)
    feature, m = features_m.strip().split(' ')
    X = []
    y = []
    for _ in range(int(m)):
        features_price = lines.pop(0)
        features_price_l = features_price.strip().split(' ')
        y.append(float(features_price_l[-1]))
        X.append(map(float, features_price_l[:-1]))

    num_val = lines.pop(0)
    Xval = []
    for _ in range(int(num_val)):
        features_val = lines.pop(0)
        features_val = features_val.strip().split(' ')
        Xval.append(map(float, features_val))

    clf = linear_model.LinearRegression()
    clf.fit (X, y)
    y_val = clf.predict(Xval)
    for i in y_val:
        print i

    graph([x[0] + x[1] for x in Xval], y_val)
    print X, y
    graph([x[0] + x[1] for x in X], y)

    plt.show()


def graph(x, y):
    items = zip(x, y)
    items.sort(key=lambda x: x[1])
    x = []
    y = []
    for i in items:
        x.append(i[0])
        y.append(i[1])

    plt.scatter(x, y, label='feature1')

    plt.xlabel('x label')
    plt.ylabel('y label')

    plt.title("Simple Plot")

    plt.legend()






if __name__ == '__main__':
    import sys
    #main(sys.stdin)
    main(open('/Users/sergisorribas/git/coursera/hackerrank/multiple_linear/sample_input.txt'))
