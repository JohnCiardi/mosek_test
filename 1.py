from mosek.fusion import *
import mosek as msk
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random

def plot_points(p, p0=[], r0=0.):
    n,k= len(p0), len(p)

    plt.rc('savefig',dpi=120)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.plot([ p[i][0] for i in range(k)], [ p[i][1] for i in range(k)], 'b*')

    if len(p0)>0:
        ax.plot(  p0[0],p0[1], 'r.')
        ax.add_patch( mpatches.Circle( p0,  r0 ,  fc="w", ec="r", lw=1.5) )
    plt.grid()
    plt.show()

n = 2
k = 100

p=  [ [random.gauss(0.,10.) for nn in range(n)] for kk in range(k)]

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

r0,p0 = primal_problem(p)

print ("r0^* = ", r0)
print ("p0^* = ", p0)

plot_points(p,p0,r0)
