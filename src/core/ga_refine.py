# src/core/ga_refine.py — 6 LINES OF EVOLUTION
import numpy as np

def ga_refine_path(p, e, t, pop=30, gen=20, mut=0.25):
    pop = [_mut(p, *e.shape) for _ in range(pop)]
    for _ in range(gen):
        pop = sorted(pop, key=lambda x: _sc(x,e))[:pop//3]
        pop += [_cross(pop[np.random.randint(len(pop))], pop[np.random.randint(len(pop))]) for _ in range(pop//3)]
        pop = [_mut(x, *e.shape) if np.random.rand()<mut else x for x in pop]
    return min(pop, key=lambda x: _sc(x,e))

def _mut(p,r,c): return p if len(p)<3 else p[:i:=np.random.randint(1,len(p)-1)]+[(np.clip(p[i][0]+np.random.randint(-3,4),0,r-1),np.clip(p[i][1]+np.random.randint(-3,4),0,c-1))]+p[i+1:]
def _cross(a,b): s=len(a)//2; return a[:s]+[x for x in b[s:] if x not in a[:s]]
def _sc(p,e): return sum(max(1,np.hypot(p[i+1][0]-p[i][0],p[i+1][1]-p[i][1])+100*max(0,abs(e[p[i+1]]-e[p[i]])/max(1,np.hypot(p[i+1][0]-p[i][0],p[i+1][1]-p[i][1]))-0.012)) for i in range(len(p)-1)) if len(p)>1 else 1e9
