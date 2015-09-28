import csv, pickle
from datetime import datetime
import numpy as np


def read_data(file):
    count = 0
    list_crimes = []
    words_crimes = {}
    days = {}
    solutions_crimes = 0
    dict_dp = {}

    with open(file, 'rb') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        header = reader.next()
        for row in reader:
            if row[1] not in list_crimes:
                list_crimes.append(row[1])

            for w in row[2].split(' '):
                if w not in words_crimes.keys():
                    words_crimes[w] = [1, {row[1] : 1}]
                else:
                    if row[1] not in words_crimes[w][1].keys():
                        words_crimes[w][1][row[1]] = 1
                    words_crimes[w][1][row[1]] += 1
                    words_crimes[w][0] += 1
            count += 1

            if row[3] not in days.keys():
                days[row[3]] = 1
            else:
                days[row[3]] += 1

            if row[4] not in dict_dp.keys():
                dict_dp[row[4]] = [1, {row[1] : 1}]
            else:
                if row[1] not in dict_dp[row[4]][1].keys():
                    dict_dp[row[4]][1][row[1]] = 0
                dict_dp[row[4]][1][row[1]] += 1
                dict_dp[row[4]][0] += 1

            if row[5] != 'NONE':
                solutions_crimes += 1

    return list_crimes, words_crimes, days, dict_dp, solutions_crimes


def load_dumpy(name):
    f = open(name+'.p', 'rb')
    obj = pickle.load(f)
    f.close()
    return obj


def write_dumpy(item, name):
    f = open(name+'.p', 'wb')
    pickle.dump(item, f)
    f.close()


def get_prob(dict):
    new_dict = {}

    for k in dict.keys():
        new_dict[k] = {}
        for it in dict[k][1].keys():
            new_dict[k][it] = float(dict[k][1][it])/float(dict[k][0])

    return new_dict


def construct_data():
    days = ['Monday', 'Tuesday', 'Friday', 'Wednesday', 'Thursday', 'Sunday', 'Saturday']
    crimes = load_dumpy('crimes')
    words = load_dumpy('words')

    x = []
    y = []

    f = open("../2015s2-mo444-assignment-02.csv")
    reader = csv.reader(f, delimiter=',', quotechar='"')
    reader.next()

    for row in reader:
        y.append(crimes.index(row[1]))
        x_line = []
        d = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        x_line.append(days.index(row[3]) + (d.hour + float(d.minute)/60 + float(d.second)/3600)/24)

        ws = row[2].split(' ')
        a = [0.0 for i in range(len(crimes))]
        for it in crimes:
            for w in ws:
                if w != '' and it in words[w].keys():
                    if a[crimes.index(it)] !=0:
                        inters = a[crimes.index(it)] * words[w][it]
                        a[crimes.index(it)] += words[w][it] - inters
                    else:
                        a[crimes.index(it)] = words[w][it]

        x_line.append(float(row[7]))
        x_line.append(float(row[8]))
        x_line += a
        x.append(x_line)

    f.close()

    return np.array(x), np.array(y)


if __name__ == "__main__":
    x, y = construct_data()

    write_dumpy(y, 'input_y')
    write_dumpy(x, 'input_x')

