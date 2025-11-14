# src/core/nsga2.py — 8 LINES OF MULTI-OBJECTIVE DOMINANCE
import numpy as np
def nsga2_refine(p,e,t,n=30,g=20):pop=[_mut(p,*e.shape)for _ in range(n)];fronts=[[]for _ in range(n)];[setattr(globals(),'pop',[_tourn(pop)for _ in range(n)])for _ in range(g)];rank={i:0 for i in range(n)};dom={i:[]for i in range(n)};[dom[j].append(i)for i in range(n)for j in range(n)if i!=j and all(_sc1(pop[i],e,k)<=_sc1(pop[j],e,k)for k in[0,1])and any(_sc1(pop[i],e,k)<_sc1(pop[j],e,k)for k in[0,1])];[rank.update({j:rank[j]+1})for j in dom for _ in dom[j]];return pop[min(range(n),key=lambda i:(rank[i],_crowd(i,pop,rank,e)))]
def _sc1(p,e,k):return len(p)if k==0 else _sc(p,e)
def _crowd(i,pop,rank,e):d=0;for k in[0,1]:f=[j for j in range(len(pop))if rank[j]==rank[i]];d+=abs(_sc1(pop[f[1]],e,k)-_sc1(pop[f[-2]],e,k))if len(f)>2 else 0;return d
def _tourn(pop):return min([pop[np.random.randint(len(pop))]for _ in range(3)],key=lambda x:(_rank(x,pop),_crowd(x,pop)))
def _rank(x,pop):return min((i for i in range(len(pop))if all(_sc1(pop[i],e,k)<=_sc1(x,e,k)for k in[0,1])and any(_sc1(pop[i],e,k)<_sc1(x,e,k)for k in[0,1])),default=0)
def _mut(p,r,c):return p if len(p)<3 else p[:i:=np.random.randint(1,len(p)-1)]+[(np.clip(p[i][0]+np.random.randint(-3,4),0,r-1),np.clip(p[i][1]+np.random.randint(-3,4),0,c-1))]+p[i+1:]
def _sc(p,e):return sum(max(1,np.hypot(p[i+1][0]-p[i][0],p[i+1][1]-p[i][1])+100*max(0,abs(e[p[i+1]]-e[p[i]])/max(1,np.hypot(p[i+1][0]-p[i][0],p[i+1][1]-p[i][1]))-0.012))for i in range(len(p)-1))if len(p)>1 else 1e9
