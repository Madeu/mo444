import csv


def read_data(file):
    count = 0
    crime_number = 0
    list_crimes = {}

    with open(file, 'rb') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        header = reader.next()
        for row in reader:
            if row[1] not in list_crimes.keys():
                list_crimes[row[1]] = [crime_number, {}]
                crime_number += 1
            for w in row[2].split(' '):
                if w not in list_crimes[row[1]][1].keys():
                    list_crimes[row[1]][1][w] = 0
                list_crimes[row[1]][1][w] += 1
            count += 1

    count1 = 0

    for k in list_crimes.keys():
        for it in list_crimes:
            if 'COMPUTERS' in list_crimes[it][1].keys():
                count1 += list_crimes[it][1]['COMPUTERS']

    print count1
    print list_crimes['LARCENY/THEFT']

if __name__ == "__main__":
    read_data("../2015s2-mo444-assignment-02.csv")