from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

def main(fst):
    lines = fst.readlines()
    features_m = lines.pop(0)
    feature, m = features_m.strip().split(' ')
    X = []
    y = []

    for _ in range(int(m)):
        features_price = lines.pop(0)
        features_price_l = map(float, features_price.strip().split(' '))
        y.append(features_price_l[-1])
        features = list(features_price_l[:-1])
        X.append(features)

    num_val = lines.pop(0)
    Xval = []
    for _ in range(int(num_val)):
        features_val = lines.pop(0)
        features_val = map(float, features_val.strip().split(' '))
        Xval.append(features_val)

    model = Pipeline([('poly', PolynomialFeatures(degree=3)), ('linear', LinearRegression(fit_intercept=False))])
    model.fit (X, y)
    y_val = model.predict(Xval)
    for i in y_val:
        print i


if __name__ == '__main__':
    import sys
    main(sys.stdin)
