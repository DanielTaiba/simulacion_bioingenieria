import numpy as np
from test_vecindad import *

def validar_posicion(pos,m):
  pos=np.where(pos>=m,pos-m,pos)
  pos=np.where(pos<0,m+pos,pos)
  return pos


r=4
m=5
matriz=[[1,0,0,0,1],
        [0,0,0,0,0],
        [0,0,1,0,0],
        [0,0,0,0,0],
        [1,0,0,0,1]]

matriz = np.array(matriz)
vector = vector_vecindad(r)
vecindad_asociada = np.zeros((5,5))

#posiciones = vector+np.array([5,5])
#print(posiciones)
#posiciones = validar_posicion(posiciones,5)
#print(posiciones)
for a,b in np.argwhere(matriz==1):
  posiciones = validar_posicion(vector+np.array([a,b]),m)
  vecindad_asociada[posiciones[:,0],posiciones[:,1]]+=1 

for a,b in np.argwhere(matriz==1):
  vecindad_asociada[a,b]=0 


print(matriz)
print(vecindad_asociada)
