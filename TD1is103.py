# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import matplotlib.pyplot as plt
import numpy as np
import math as m
import scipy.linalg as la
import scipy.io as sio

pluv = sio.loadmat('pluv') #chargement du fichier

def Gaussienne(mu, sigma):
    x=[]
    for i in range(0, 10000):
        x.append((m.sqrt(sigma) * np.random.randn()) + mu)
    return x

def dens(x):
    y = m.exp(-((x-2)**2)/(2*9))/(m.sqrt(9) * m.sqrt(2 * m.pi))
    return y

def plot(x):
   plt.hist(x, bins=50, density = True)
   X=[]
   Y=[]
   for i in range(0, 10000):
       X.append((i*20/10000 - 10))
       Y.append(dens(X[i]))
   plt.plot(X, Y)
   plt.show()
   
def calcEntrop(x):
    p = np.histogram(x, bins=50, density = None)[0]
    N = len(p)
    H = 0
    s=0
    for i in range(0, N):
        s+=p[i]
        x = (p[i]/1000)
        if (x != 0):
            H = H + (x * m.log10(x))
    return -H


#on procede de la meme maniere que pour la loi normale unidimensionelle
#cependant, il nous faut acceder a la "racine" de la matrice de covariance
#or cela est permis, on cherche la matrice telle que DD^T = R, qui existe car
#R est diagonalisable

#on a alors D, et X est alors la combinaison linaire de Y avec les Yi des 
#variables aleatoires scalaires independantes entre elles
#X = mu + BY
#et c'est ok

# l'operation permettant d'obtenir la "racine d'une matrice diagonalisable est
#fournie par scipy : scipy.linalg.sqrtm

def GaussienneP(mu, sigma, p):
    X=[]
    for i in range(0, 1000):
        X.append(np.dot(la.sqrtm(sigma),[[np.random.randn()], [np.random.randn()]]) + mu)
    return X

cases = 20

x = GaussienneP([[1], [2]], [[2,1],[1, 2]], 2)
y = GaussienneP([[0], [0]], [[1,0],[0, 1]], 2)
Xaxisx = []
Yaxisx = []
Xaxisy = []
Yaxisy = []
for i in range(0, 1000):
    ax = x[i][0]
    bx = x[i][1]
    ay = y[i][0]
    by = y[i][1]
    Xaxisx.append(ax[0])
    Yaxisx.append(bx[0])
    Xaxisy.append(ay[0])
    Yaxisy.append(by[0])
H1 = np.histogram2d(Xaxisx, Yaxisx, bins=20, normed=True)
H2 = np.histogram2d(Xaxisy, Yaxisy, bins=20)
#plt.matshow(H1[0])
#plt.matshow(H2[0])

R = [[2,1],[1, 2]] 
mu = [[0], [0]]
    
step = 10**(-3)
theta = np.arange(0, 2*np.pi, step)
w = np.array([np.cos(theta), np.sin(theta)])
x1 = la.sqrtm(R)@w + mu@np.ones((1, len(theta)))
x2 = np.sqrt(5)*la.sqrtm(R)@w + mu@np.ones((1, len(theta)))
x3 = np.sqrt(10)*la.sqrtm(R)@w + mu@np.ones((1, len(theta)))


#Grosse magouille sur les coordonées...à corriger
def recenter(x):
    n=len(x)
    X=[]
    for i in range(0, n):
        X.append(x[i]+cases/2)
    return X
        
X1=[]
X1.append(recenter(x1[0]))
X1.append(recenter(x1[1]))

X2=[]
X2.append(recenter(x2[0]))
X2.append(recenter(x2[1]))

X3=[]
X3.append(recenter(x3[0]))
X3.append(recenter(x3[1]))

#plt.plot(X1[0], X1[1])
#plt.plot(X2[0], X2[1])
#plt.plot(X3[0], X3[1])

#Partie 4
#tracer des histogrammes 2D des couples Bordeaux/Nantes, Bordeaux/Santiago
#et Nantes/Santiago

PBordeaux = []
PNantes = []
PSantiago = []
pluie = pluv['X_pluv']
N = len(pluie)
for i in range(0, N):
    PBordeaux.append(pluie[i][0])
    PNantes.append(pluie[i][1])
    PSantiago.append(pluie[i][2])
    
P1 = np.histogram2d(PBordeaux, PNantes, bins = 20)
P2 = np.histogram2d(PBordeaux, PSantiago, bins = 20)
P3 = np.histogram2d(PNantes, PSantiago, bins = 20)

plt.matshow(P1[0])
plt.matshow(P2[0])
plt.matshow(P3[0])

def constXk(pluie, idx1, idx2):
    x=[]
    n = len(pluie)
    for i in range(0, n):
        x.append([[pluie[i][idx1]], [pluie[i][idx2]]])
    return x

def calcmu(x):
    n = len(x)
    s=[[0], [0]]
    for i in range(0, n):
        s[0][0]+=x[i][0][0]
        s[1][0]+=x[i][1][0]
    s[0][0] = s[0][0]/n
    s[1][0] = s[1][0]/n
    return s

def calcR(x, mu):
    n = len(x)
    B=[[0], [0]]
    R= [[0, 0], [0, 0]]
    for i in range(0, n):
        B[0][0] = x[i][0][0] - mu[0][0]
        B[1][0] = x[i][1][0] - mu[1][0]
        A = np.dot(B, np.transpose(B))
        R[0][0] += A[0][0]
        R[0][1] += A[0][1]
        R[1][0] += A[1][0]
        R[1][1] += A[1][1]
    return R
plt.show()


