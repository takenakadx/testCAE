import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import lib.common as c

class System:
    def __init__(self,THICKNESS,POISSON,YOUNG,WIDTH,HEIGHT,GRID_SIZE,meshes=None,force=None,fixed=None,dots=None):
        self.young = YOUNG
        self.thickness = THICKNESS
        self.poisson = POISSON
        self.width = WIDTH
        self.height = HEIGHT
        if dots is None:
            self.meshes = {}
            self.force = []
            self.fixed = []
            self.dots = []
        else:
            self.meshes = meshes
            self.force = force
            self.fixed = fixed
            self.dots = dots
        w,h = self.grid_size = GRID_SIZE
        dw = self.width/w
        dh = self.height/h
        meshsize = 0
        for i in range(w+1):
            for j in range(h+1):
                self.dots.append([i*dw,j*dh])
                if i < w and j < h:
                    now_pos = len(self.dots) - 1
                    r_pos = len(self.dots)
                    u_pos = len(self.dots) + h
                    ur_pos = len(self.dots) + h + 1 
                    self.meshes[meshsize] = [now_pos,r_pos,ur_pos]
                    self.meshes[meshsize + 1] = [now_pos,ur_pos,u_pos]
                    meshsize += 2
        self.fixed = [[False,False] for i in range(len(self.dots))]
        self.force = [[0.,0.] for i in range(len(self.dots))]
    
    def add_force(self,pos,f):
        self.force[pos] = f

    def add_fixed_position(self,pos,fixed):
        self.fixed[pos] = fixed

    def show_mesh(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()
        dots = np.array(self.dots)
        x,y = dots[:,0], dots[:,1]
        lines = []
        for k in self.meshes:
            points = [dots[e] for e in self.meshes[k]]
            lines.append(points[0:2])
            lines.append(points[1:3])
            lines.append(points[::2])
        #triangles = np.array([self.meshes[k] for k in self.meshes])
        #C = np.array([i for i in range(len(x))])
        #ax.tripcolor(x,y,triangles,C)
        self.ax.scatter(x,y)
        lc = LineCollection(lines,colors=["b" for _ in range(len(lines))])
        self.ax.add_collection(lc)
        plt.show()

    def output(self,filename):
        d = {
            "dots":self.dots,
            "fixed":self.fixed,
            "force":self.force,
            "meshes":self.meshes,
            "POISSON":self.poisson,
            "YOUNG":self.young,
            "THICKNESS":self.thickness,
            "WIDTH":self.width,
            "HEIGHT":self.height,
            "GRID_SIZE":self.grid_size
        }
        c.write_input(filename,d)

if __name__=="__main__":
    system = System(1,0.3,210000,2,1,(2,1))
    system.show_mesh()
    system.output("../data/input/sample2.json")
    #print(system.dots)