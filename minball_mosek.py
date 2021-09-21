
#use mosek to solve a Minimum circular cover problem
from mpl_toolkits.mplot3d import Axes3D
from mosek.fusion import *
import mosek as msk
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import numpy as np

def plot_points(p, p0=[], r0=0.):
    n,k= len(p0), len(p)
    plt.rc('savefig',dpi=360)

    if len(p0)==2:
        ax = plt.subplot(111)
        ax.set_aspect('equal')
        ax.plot([ p[i][0] for i in range(k)], [ p[i][1] for i in range(k)], 'b*')
        ax.plot(  p0[0],p0[1], 'r.')
        ax.add_patch( mpatches.Circle( p0,  r0 ,  fc="w", ec="r", lw=1.5) )
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter([ p[i][0] for i in range(k)], [ p[i][1] for i in range(k)], [ p[i][2] for i in range(k)])
        ax.scatter(p0[0],p0[1],p0[2])
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = r0 * np.outer(np.cos(u), np.sin(v)) + p0[0]
        y = r0 * np.outer(np.sin(u), np.sin(v)) + p0[1]
        z = r0 * np.outer(np.ones(np.size(u)), np.cos(v)) + p0[2]
        ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b' ,alpha=0.25)

    plt.grid()
    plt.show()

def primal_problem(P):
    k= len(P)
    if k==0: return -1,[]
    n= len(P[0])
    with Model("minimal sphere enclosing a set of points - primal") as M:
        r0 = M.variable(1    , Domain.greaterThan(0.))
        p0 = M.variable([1,n], Domain.unbounded())

        R0 = Var.repeat(r0,k)
        P0 = Var.repeat(p0,k)

        M.constraint( Expr.hstack( R0, Expr.sub(P0 , P) ), Domain.inQCone())

        M.objective(ObjectiveSense.Minimize, r0)
        M.setLogHandler(open('logp','wt'))

        M.solve()
        return r0.level()[0], p0.level()

n = 3
k = 400
p=  [ [random.gauss(0.,10.) for nn in range(n)] for kk in range(k)]
r0,p0 = primal_problem(p)

print ("r0^* = ", r0)
print ("p0^* = ", p0)

plot_points(p,p0,r0)
