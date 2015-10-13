import matplotlib.pyplot as plt
import matplotlib.colors as clr
import random, math


def create_marks(dict):

    colors = clr.cnames.keys()

    allx, ally = [], []

    for k in sorted(dict.keys()):
        x = []
        y = []
        color = colors[int(random.random()*len(colors))]
        colors.remove(color)
        for it in dict[k]:
            x.append(it[0])
            y.append(it[1])

        plt.plot(x, y, color=color, marker='o', linestyle='none')

        allx += x
        ally += y

    print ([min(allx)-1, max(allx)+1, min(ally)-1, max(ally)+1])

    plt.axis([min(allx)-1, max(allx)+1, min(ally)-1, max(ally)+1])
    plt.show()


def generate_points(num_centers, num_range, space):

    points = []
    for i in range(num_centers):
        center = [int(num_range*random.random())+space, int(num_range*random.random())+space]
        print center
        for i in range(space):
            r, teta = int(space*random.random()), 2*math.pi*random.random()
            points.append([center[0]+r*math.cos(teta), center[1]+r*math.sin(teta)])

    return points