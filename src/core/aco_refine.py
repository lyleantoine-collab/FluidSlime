# src/core/aco_refine.py — 6 LINES OF ANT DOMINANCE
import numpy as np
def aco_refine_path(p,e,t,a=40,s=80,ev=0.95):ph=np.full(e.shape,0.1);best=p;bs=_sc(p,e);[ph*=(ev),ph:=ph+np.array([1/bs if np.all(np.array(ant)==best)else 0 for ant in ants]).reshape(ph.shape)for ants in[[[p[0]]+[next((n for n in _nei(pos,*e.shape)if n in p and ph[n[0],n[1]]>0),max(_nei(pos,*e.shape),key=lambda n:ph[n[0],n[1]]if n in p else (0,0)))for pos in ant[:-1]]+[p[-1]]for _ in range(a)]if(bs:=min(bs,_sc(ant:=ants[np.random.randint(a)],e)))and(setattr(globals(),'best',ant))][:s];return best
def _nei(pos,r,c):y,x=pos;return[(y+dy,x+dx)for dy in[-1,0,1]for dx in[-1,0,1]if 0<=y+dy<r and 0<=x+dx<c and(dy,dx)!=(0,0)]
def _sc(p,e):return sum(max(1,np.hypot(p[i+1][0]-p[i][0],p[i+1][1]-p[i][1])+100*max(0,abs(e[p[i+1]]-e[p[i]])/max(1,np.hypot(p[i+1][0]-p[i][1],p[i+1][1]-p[i][1]))-0.012))for i in range(len(p)-1))if len(p)>1 else 1e9
