# src/core/woa_refine.py — 7 LINES OF WHALE POWER
import numpy as np
def woa_refine_path(p,e,t,n=25,g=18):pop=[_mut(p,*e.shape)for _ in range(n)];best=min(pop,key=lambda x:_sc(x,e));[setattr(globals(),'pop',[_step(x,best,*e.shape,A:=2*(1-_/g),a:=2*_-A/g,r:=np.random.rand())for x in pop])or setattr(globals(),'best',min(pop+[best],key=lambda x:_sc(x,e)))for _ in range(g)];return best
def _step(p,b,r,c,A,a,r):return _mut(b+(np.random.rand()*2-1)*A*np.random.rand(len(p),2)*np.hypot(*[p[i]-b[i]for i in range(len(p))]),r,c)if r<0.5 and abs(A)<1 else _mut(b*np.exp(1.5*r)*np.cos(2*np.pi*r)+p,r,c)if r<0.5 else _mut(p+(np.random.rand()*2-1)*a*(b-p),r,c)
def _mut(p,r,c):return p if len(p)<3 else p[:i:=np.random.randint(1,len(p)-1)]+[(np.clip(p[i][0]+np.random.randint(-4,5),0,r-1),np.clip(p[i][1]+np.random.randint(-4,5),0,c-1))]+p[i+1:]
def _sc(p,e):return sum(max(1,np.hypot(p[i+1][0]-p[i][0],p[i+1][1]-p[i][1])+100*max(0,abs(e[p[i+1]]-e[p[i]])/max(1,np.hypot(p[i+1][0]-p[i][0],p[i+1][1]-p[i][1]))-0.012))for i in range(len(p)-1))if len(p)>1 else 1e9
