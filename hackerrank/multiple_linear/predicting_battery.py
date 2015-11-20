from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

def main(fst):
    input_number = float(fst.readline())
    x = []
    y = []
    for line in open('trainingdata.txt').readlines():
        xi, yi = line.split(',')
        x.append([float(xi)])
        y.append(float(yi))

    model = Pipeline([('poly', PolynomialFeatures(degree=7)), ('linear', LinearRegression())])
    model.fit (x, y)

    print model.predict(input_number)


if __name__ == '__main__':
    import sys
    main(sys.stdin)
