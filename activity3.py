from readdata.readdata import load_dumpy, write_dumpy
from clustering import cluster


def main():
    hogs = load_dumpy('hogs')
    print 'Hogs loaded'

    c = cluster.Cluster(hogs, 0.0001)

    clusters = []

    for i in range(10, 100, 5):
        print str(i)+' clusters ...'
        center, classes = c.k_means(i)
        clusters.append((c.distortion(center, classes), i))

    write_dumpy(clusters, 'elbow')


if __name__ == '__main__':
    main()