import numpy as np
import json

# this program made for 2D
# and triangle mesh
DIM = 2 # DO NOT CHANGE THIS VARIABLE

mesh_areas = {}

def get_D(YOUNG,POISSON):
    c = YOUNG / (1 - 2*POISSON) / (1 + POISSON) 
    return c*np.array([
        [1-POISSON,POISSON,0],
        [POISSON,1-POISSON,0],
        [0,0,(1-2*POISSON)/2]
    ])

def init():
    with open("input/sample.json","r") as f:
        r = json.load(f)
    return r

def get_B(meshes,dots):
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

def get_Ke(meshes,D,Bs,THICKNESS):
    r_mat = {}
    for k in meshes:
        B = Bs[k]
        area = mesh_areas[k]
        r_mat[k] = THICKNESS*area*B.T@D@B
    return r_mat

def get_K(meshes,dots,Ke):
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

def set_boundary_condition(dots,fixed,force,K):
    u = np.zeros(len(dots)*2)
    um = np.array([False for _ in range(len(dots)*2)])
    f = np.zeros_like(u)
    for i,e in enumerate(force):f[i*2:i*2+2] = np.array(e)

    for k,e in enumerate(fixed):
        for ax_i,is_fixed in enumerate(e):
            if is_fixed:
                index = 2*k+ax_i
                um[index] = True
                u[index] = dots[k][ax_i]
                f-=u[index]*K[:,index]
                K[:,index] = 0
                K[index,:] = 0
                K[index,index] = 1
    for i,e in enumerate(um):
        if e:f[i] = u[i]
    return f,K

def gaussian_elimination(A, b):
    n = len(b)
 
    # 前進消去を行う
    for i in range(n):
        pivot = A[i, i]                 # 対角成分をpivotに代入
        A[i] = A[i] / pivot             # pivotで係数行列を割り、A[i,i]を1にする
        b[i] = b[i] / pivot             # 定数ベクトルもpivotで割り同値変形する
 
        # i行目の定数倍をi+1行目以降から引くループ
        for j in range(i+1, n):
            p = A[j, i]                 # i+1行目以降i列の数値を格納
            A[j] -= p * A[i]            # 係数行列のi+1行目からi行目の定数倍を引く
            b[j] -= p * b[i]            # 定数ベクトルのi+1行目からi行目の定数倍を引く
 
    # 後退代入を行う
    x = np.zeros(n)                     # 解の入れ物を用意
    for i in reversed(range(n)):        # 最終行から後退処理する
        x[i] = b[i] / A[i, i]           # 解を求める
        for j in range(i):
            b[j] -= A[j, i] * x[i]      # 解が求まった列分bの値を上から更新する
    return x

def make_reaction(K,U):
    return K@U

def make_strain_element(meshes,U,Bs):
    strain_element = {}
    for k in meshes:
        ue = np.zeros(len(meshes[k])*2)
        for i,e in enumerate(meshes[k]):
            ue[i*2:i*2+2] = U[e*2:e*2+2]
        strain_element[k] = Bs[k]@ue
    return strain_element

def make_stress_element(st,D):
    r_vec = {}
    for k in st:
        r_vec[k] = D@st[k]
    return r_vec


def solve(data):
    D_MATRIX = get_D(data["YOUNG"],data["POISSON"])
    B_MATRIXES = get_B(data["meshes"],data["dots"])
    Ke_MATRIXES = get_Ke(data["meshes"],D_MATRIX,B_MATRIXES,data["THICKNESS"])
    K_MATRIX = get_K(data["meshes"],data["dots"],Ke_MATRIXES)
    F,K_MATRIX_ranked = set_boundary_condition(data["dots"],data["fixed"],data["force"],np.copy(K_MATRIX))

    ans = np.linalg.solve(K_MATRIX_ranked,F)
    Fr = make_reaction(K_MATRIX,ans)
    strain = make_strain_element(data["meshes"],ans,B_MATRIXES)
    stress = make_stress_element(strain,D_MATRIX)
    return ans,Fr,strain,stress

if __name__=="__main__":
    solve(init())