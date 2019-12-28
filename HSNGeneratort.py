# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 18:24:32 2019

@author: hu
"""
import numpy as np
import random as r
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform


class HSNGenerator:
    def __init__(self):
        self.dir = 'your-directory\\'
    
    def gen(self, Spokes, Cities, f):
        WH = 50000
        R = int(np.sqrt(WH**2/Cities/np.pi))
        cx = []
        cy = []
        for i in range(Cities):
            cx.append(int(r.randint(1, WH)))
            cy.append(int(r.randint(1, WH)))
            
        sx = []
        sy = []
        while len(sx)<Spokes:
            ci = r.randint(0,Cities-1)
            xt = np.random.normal(0, R/2)
            yt = np.random.normal(0, R/2)
            x = int(cx[ci]+xt)
            y = int(cy[ci]+yt)
            if x>0 and x<=WH and y>0 and y<=WH:
                sx.append(x)
                sy.append(y)
        plt.figure()
        plt.plot(sx, sy, 'o', c = 'black')
        
        L = zip(sx,sy)
        L = [[a,b] for (a,b) in L]
        L = pdist(L,metric='euclidean')
        L = squareform(L).astype(np.int)
        W = []
        for i in range(Spokes):
            d = r.randint(0,np.max([1000,Spokes]))
            row = L[i,:]
            row = row/np.max(row)
            if np.sum(row<0)>0:
                print(np.sum(row<0))
            a1 = np.sum(row)
            d = (row/a1 *d*10).astype(np.long)
            W.append(d)
        
        if f is None:
            PC = 3
            PT = 0.75
            PD = 2
            W = np.array(W)
            Oi = np.sum(W,1)
            Di = np.sum(W,0)            
            return (sx,sy,W,PC,PT,PD,Oi,Di,L)
        
        s = '{}Net_{}_{}_{}.svg'.format(self.dir,Spokes,Cities,f)
        plt.savefig(s, dpi=600, bbox_inches='tight')
        s = '{}Net_{}_{}_{}.txt'.format(self.dir,Spokes,Cities,f)
        file = open(s,'w')
        file.write('{}\n'.format(Spokes))
        for i in range(Spokes):
            file.write('{},{}\n'.format(sx[i],sy[i]))
        for i in range(Spokes):
            s = ''
            for j in range(Spokes):
                s += str(W[i][j])+','
            file.write('{}\n'.format(s[:-1]))
        file.close()
    
    def gen_dataset(self):
        for c in range(10,50,10):
            for s in range(1,6):
                if c>s:
                    pass
                for i in range(1):
                    self.gen(s*1000,c*10,i)                
        for c in range(10,11):
            for s in range(20,220,20):
                if c>s:
                    pass
                for i in range(1):
                    self.gen(s,c,i)
        
    def read(self, Spokes, Cities, f):
        s = '{}Net_{}_{}_{}.txt'.format(self.dir,Spokes,Cities,f)
        f = open(s,'r')
        lines = f.readlines()
        f.close()
        i = 0
        N = 0
        X = []
        Y = []
        W = []
        for s in lines:
            if i==0:
                N = int(s)
                i += 1
                continue
            if i<= N:
                xy = s.split(',')
                X.append(int(xy[0]))
                Y.append(int(xy[1]))
                i += 1
                continue
            wi = s.split(',')
            wi = [int(a) for a in wi]
            W.append(wi)
        PC = 3
        PT = 0.75
        PD = 2
        W = np.array(W)
        Oi = np.sum(W,1)
        Di = np.sum(W,0)
        L = zip(X,Y)
        L = [[a,b] for (a,b) in L]
        L = pdist(L,metric='euclidean')
        L = (squareform(L)/10).astype(np.int)
        return (X,Y,W,PC,PT,PD,Oi,Di,L)
        
    def cost(self, W,PC,PT,PD,L,A):
        N = list(range(len(A)))
        c = 0
        for i in N:
            for j in N:
                c += W[i,j]*(L[i,A[i]]*PC + L[A[i],A[j]]*PT + L[A[j],j]*PD)
        return c

    def draw(self, X, Y, A):
        N = list(range(len(X)))
        H = list(set(A))
        for k1 in range(len(H)):
            for k2 in range(k1, len(H)):
                i = H[k1]
                j = H[k2]
                plt.plot([X[i], X[j]], [Y[i], Y[j]], color='g')
        for i in set(N)-set(H):
            plt.plot([X[i], X[A[i]]], [Y[i], Y[A[i]]], color = 'k', linewidth=0.5)
            plt.plot(X[i], Y[i], 'ko')
        for i in H:
            plt.plot(X[i], Y[i], 'ro', markersize=10)
        plt.show()
        
    def test_1(self):
        (X,Y,W,PC,PT,PD,Oi,Di,L) = self.gen(30, 3, None)
        L = (L/10).astype(np.int)
        A = [1,2,3]*10
        print(X,len(Y))
        c = self.cost(W,PC,PT,PD,L,A)
        print('cost=',c)
        self.draw(X, Y, A)
        
if __name__ == '__main__':
    hsn = HSNGenerator()
    hsn.test_1()

                