import copy
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np

class Post:
    def __init__(self,i,o):
        self.output = {
            "U":o[0],
            "Fr":o[1],
            "strain":[2],
            "stress":o[3]
        }
        self.input = i

    def get_max_u(self):
        return max(self.output["U"])
        
    def calc_dots_position(self,scaling=1.):
        dots = copy.deepcopy(self.input["dots"])
        for i in range(len(dots)):
            dots[i][0] += self.output["U"][i*2]*scaling
            dots[i][1] += self.output["U"][i*2+1]*scaling
        return dots

    def make_label_for_dots(self,dots,threshold=0.5):
        o = np.array(self.output["Fr"],dtype=int)
        r_label = []
        for i in range(len(o)//2):
            if abs(o[i*2]) < threshold > abs(o[i*2+1]):continue
            r_label.append((dots[i][0],dots[i][1],f"({o[i*2]},{o[i*2+1]})"))
        return r_label
    def show_dots_position(self,scaling):
        dots = np.array(self.calc_dots_position(scaling))
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()
        x,y = dots[:,0], dots[:,1]
        lines = []
        for k in self.input["meshes"]:
            points = [dots[e] for e in self.input["meshes"][k]]
            lines.append(points[0:2])
            lines.append(points[1:3])
            lines.append(points[::2])
        self.ax.scatter(x,y)
        lc = LineCollection(lines,colors=["b" for _ in range(len(lines))])
        self.ax.add_collection(lc)
        labels = self.make_label_for_dots(dots)
        for label in labels:
            self.ax.text(label[0],label[1],label[2])
        plt.show()
