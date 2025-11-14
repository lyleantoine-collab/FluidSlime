# src/core/firefly_refine.py — 6 LINES OF LIGHT
import numpy as np
def firefly_refine_path(p,e,t,n=20,g=15):pop=[_mut(p,*e.shape)for _ in range(n)];best=min(pop,key=lambda x:_sc(x,e));[setattr(globals(),'pop',[_step(x,best,d:=_dist(x,best,e),*e.shape,r:=np.random.rand())for x in pop])or setattr(globals(),'best',min(pop+[best],key=lambda x:_sc(x,e)))for _ in range(g)];return best
def _step(p,b,d,r,c,rand):return _mut(p+(b-p)*np.exp(-0.5*d)*rand,r,c)if d>0 else _mut(p+np.random.randn(len(p),2),r,c)
def _dist(a,b,e):return sum(max(1,np.hypot(a[i+1][0]-b[i+1][0],a[i+1][1]-b[i+1][1])+abs(e[a[i+1]]-e[b[i+1]]))for i in range(min(len(a),len(b))-1))
def _mut(p,r,c):return p if len(p)<3 else p[:i:=np.random.randint(1,len(p)-1)]+[(np.clip(p[i][0]+np.random.randint(-3,4),0,r-1),np.clip(p[i][1]+np.random.randint(-3,4),0,c-1))]+p[i+1:]
def _sc(p,e):return sum(max(1,np.hypot(p[i+1][0]-p[i][0],p[i+1][1]-p[i][1])+100*max(0,abs(e[p[i+1]]-e[p[i]])/max(1,np.hypot(p[i+1][0]-p[i][0],p[i+1][1]-p[i][1]))-0.012))for i in range(len(p)-1))if len(p)>1 else 1e9
