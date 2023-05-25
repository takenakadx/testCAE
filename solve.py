import numpy as np
# this program made for 2D
# and triangle mesh
DIM = 2 # DO NOT CHANGE THIS VARIABLE
dots = [
    (0.,0.),
    (1.,0.),
    (2.,0.),
    (2.,1.),
    (1.,1.),
    (0.,1.0)
]

meshes = {
    1:[0,1,4],
    2:[1,2,3],
    3:[1,3,4],
    4:[0,4,5]
}
mesh_areas = {}

THICKNESS = 1.
YOUNG = 210000
POISSON = 0.3

def get_D():
    c = YOUNG / (1 - 2*POISSON) / (1 + POISSON) 
    return c*np.array([
        [1-POISSON,POISSON,0],
        [POISSON,1-POISSON,0],
        [0,0,(1-2*POISSON)/2]
    ])

def get_B():
    r_mat = {}
    for k in meshes:
        pi = meshes[k]
        x1,y1 = dots[pi[0]]
        x2,y2 = dots[pi[1]]
        x3,y3 = dots[pi[2]]

        mesh_areas[k] = (x1*y2-x1*y3+x2*y3-x2*y1+x3*y1-x3*y2)/2

        c = 1/ mesh_areas[k] /2

        B = c*np.array([
            [y2-y3,0,y3-y1,0,y1-y2,0],
            [0,x3-x2,0,x1-x3,0,x2-x1],
            [x3-x2,y2-y3,x1-x3,y3-y1,x2-x1,y1-y2]
        ])
        r_mat[k] = B
    return r_mat

def get_Ke(D,Bs):
    r_mat = {}
    for k in meshes:
        B = Bs[k]
        area = mesh_areas[k]
        r_mat[k] = THICKNESS*area*B.T@D@B
    return r_mat

def get_K(Ke):
    dots_size = len(dots)
    r_mat = np.zeros((dots_size*DIM,dots_size*DIM))
    for k in meshes:
        #sample = np.zeros_like(r_mat)
        for i in range(3):
            for j in range(3):
                i_d = meshes[k][i]
                j_d = meshes[k][j]
                r_mat[i_d*2:i_d*2+2,j_d*2:j_d*2+2] += Ke[k][i*2:i*2+2,j*2:j*2+2]
                #sample[i_d*2:i_d*2+2,j_d*2:j_d*2+2] = 1
        #print(sample)
    return r_mat

        

def main():
    D_MATRIX = get_D()
    B_MATRIXES = get_B()
    Ke_MATRIXES = get_Ke(D_MATRIX,B_MATRIXES)
    K_MATRIX = get_K(Ke_MATRIXES)

main()
