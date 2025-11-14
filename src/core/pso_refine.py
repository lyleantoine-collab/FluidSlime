# src/core/pso_refine.py — 4 LINES OF SWARM FURY
import numpy as np

def pso_refine_path(p,e,t,n=30,i=15): pop=[_mut(p,*e.shape)for _ in range(n)]; g=min(pop,key=lambda x:_sc(x,e)); [setattr(globals(),'pop',[_step(x,g,*e.shape)for x in pop])or setitem(globals(),'g',min(pop+[g],key=lambda x:_sc(x,e)))for _ in range(i)]; return g
def _mut(p,r,c): return p if len(p)<3 else p[:i:=np.random.randint(1,len(p)-1)]+[(np.clip(p[i][0]+np.random.randint(-2,3),0,r-1),np.clip(p[i][1]+np.random.randint(-2,3),0,c-1))]+p[i+1:]
def _step(p,g,r,c): return g if np.random.rand()<0.3 else _mut(p,r,c) if np.random.rand()<0.5 else p
def _sc(p,e): return sum(max(1,np.hypot(p[i+1][0]-p[i][0],p[i+1][1]-p[i][1])+100*max(0,abs(e[p[i+1]]-e[p[i]])/max(1,np.hypot(p[i+1][0]-p[i][0],p[i+1][1]-p[i][1]))-0.012)) for i in range(len(p)-1)) if len(p)>1 else 1e9
