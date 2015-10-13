__author__ = 'abonfante'
import pickle,itertools
from sklearn import linear_model
from sklearn import preprocessing
from sklearn import neighbors
import numpy as np

def merge_class(l, a, b, porc):
    y = [a for i in range(int(len(l[a])*porc))] + [b for j in range(int(len(l[b])*porc))]
    ty = [a for i in range(len(l[a]) - int(len(l[a])*porc))]+ [b for j in range(len(l[b]) - int(len(l[b])*porc))]
    vet = [l[a][i] for i in range(int(len(l[a])*porc))] + [l[b][j] for j in range(int(len(l[b])*porc))]
    val = [l[a][i] for i in range(len(l[a]) - int(len(l[a])*porc))] + [l[b][j] for j in range(len(l[b]) - int(len(l[b])*porc))]

    return np.array(vet), np.array(y), np.array(val), np.array(ty)


def calc_ovo_log(allx, porc):
    classfs = []
    count = 0

    for it in itertools.combinations([i for i in range(39)], 2):
        print count, it
        input_x, input_y, vald_x, vald_y = merge_class(allx, it[0], it[1], porc)

        norm_x = preprocessing.normalize(input_x)
        norm_t = preprocessing.normalize(vald_x)

        tx, pred = grid_search_log(norm_x, input_y, norm_t, vald_y, 0.001, 1e4, 10)

        classfs.append([it, tx, pred])
        print tx

        count += 1

    return classfs

def grid_search_log(X, Y, TX, TY, i, f, s):
    res = []

    csf = None
    i = i
    while i < f:
        val, csf = clasf_valid_log(X, Y, TX, TY, i)
        if val != 1.0:
            res.append(val)
        i = i * s

    return max(res), csf


def clasf_valid_log(X, Y, TX, TY, alpha):
    csf = linear_model.LogisticRegression(C=alpha)
    csf.fit(X,Y)

    count_ok = 0
    for i in range(len(TX)):
        if csf.predict(TX[i])[0] == TY[i]:
            count_ok += 1

    return float(count_ok)/len(TX), csf

def calc_ovo_knn(allx, porc):
    classfs = []
    count = 0

    for it in itertools.combinations([i for i in range(39)], 2):
        print count, it
        input_x, input_y, vald_x, vald_y = merge_class(allx, it[0], it[1], porc)

        norm_x = preprocessing.normalize(input_x)
        norm_t = preprocessing.normalize(vald_x)

        tx, pred = grid_search_log(norm_x, input_y, norm_t, vald_y, 0.001, 1e4, 10)

        classfs.append([it, tx, pred])
        print tx

        count += 1

    return classfs

def grid_search_knn(X, Y, TX, TY, i, f, s):
    res = []

    csf = None
    i = i
    while i < f:
        val, csf = clasf_valid_log(X, Y, TX, TY, i)
        if val != 1.0:
            res.append(val)
        i = i + s

    max_res = max(res)
    while max_res in res:
        res.remove(max_res)
    max_f = max_res if len(res) == 0 else max(res)
    return max_f, csf


def clasf_valid_knn(X, Y, TX, TY, alpha):
    csf = neighbors.KNeighborsClassifier()
    csf.fit(X,Y)

    count_ok = 0
    for i in range(len(TX)):
        if csf.predict(TX[i])[0] == TY[i]:
            count_ok += 1

    return float(count_ok)/len(TX), csf


def eletion_ovo(list_clsf, X, size):
    mat = [[0 for i in range(size)] for i in range(size)]
    res = []

    for a,b,c in list_clsf:
        p = c.predict_proba(X)
        mat[a[0]][a[1]] = p[0][0]
        mat[a[1]][a[0]] = p[0][1]

    for it in mat:
        res.append(sum(it)/(len(it)-1))

    return res.index(max(res))


def get_accur(list_clsf, X, Y, crimes):

    ok = 0
    for i in range(len(X)):
        print i
        res = eletion_ovo(list_clsf, X[i], len(crimes))
        if res == crimes.index(Y[i]):
            ok += 1
            print 'ok'

    return ok