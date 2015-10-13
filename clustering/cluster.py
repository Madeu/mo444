import math, random
import numpy as np

class Cluster:

    def __init__(self, p, e):
        self.points = p
        self.ELPS = e

    def __dist_vect(self, a, b):
        return np.linalg.norm(a-b)

    def __dist_list_vect(self, a, b):
        res = 0.0
        for i in range(len(a)):
            res += self.__dist_vect(a[i], b[i])

        return res/len(a)

    def __calc_groups(self, centers, points):
        c = {}
        len(centers)
        for p in points:
            dists = []
            for center in centers:
                dists.append(self.__dist_vect(center, p))
            c_point = str(dists.index(min(dists)))
            if c_point not in c.keys():
                c[c_point] = []
            c[c_point].append(p)

        return c

    def __realoc_center(self, dict_class, centers):
        new_c = centers
        for k in sorted(dict_class.keys()):
            c = np.zeros(len(new_c[0]))
            for p in dict_class[k]:
                c = c+p
            new_c[int(k)] = c/len(dict_class[k])

        return new_c

    def __k_means_core(self, k):

        centers = self.__random_centers(self.points, k)
        classes, new_centers = [], []
        last_dist = 0

        while True:
            len(centers)
            classes = self.__calc_groups(centers, self.points)
            new_centers = self.__realoc_center(classes, centers)

            dist = self.__dist_list_vect(new_centers, centers)

            if math.fabs(dist - last_dist) < self.ELPS:
                break

            last_dist = dist
            centers = new_centers

        return new_centers, classes

    def distortion(self, centers, classes):
        j, m = 0.0, 0
        for k in classes.keys():
            for it in classes[k]:
                j += self.__dist_vect(it, centers[int(k)])
                m += 1

        return j/m

    def __random_centers(self, points, k):
        centers = []
        for i in range(k):
            centers.append(points[int(len(points)*random.random())])

        return centers

    def k_means(self, k, times = 100):
        centers, classes = self.__k_means_core(k)
        best_dist = self.distortion(centers, classes)

        for i in range(times):
            center_aux, classes_aux = self.__k_means_core(k)

            aux_dist = self.distortion(center_aux, classes_aux)

            if (aux_dist < best_dist):
                centers = center_aux
                classes = classes_aux

        return centers, classes