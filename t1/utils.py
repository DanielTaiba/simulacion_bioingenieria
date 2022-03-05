import numpy as np
from simulacion import vector_vecindad,validar_posicion

def calcular_vecindad(matriz,r):#devuelve la probabilidad asociada a cada punto
  m,n = matriz.shape
  vector = vector_vecindad(r)
  prob=vector.shape[0]
  vecindad_asociada = np.zeros((m,n))

  for a,b in np.argwhere(matriz==1):
    posiciones = validar_posicion(vector+np.array([a,b]),m)
    vecindad_asociada[posiciones[:,0],posiciones[:,1]]+=1 

  for a,b in np.argwhere(matriz==1):
    vecindad_asociada[a,b]=0 
  
  return vecindad_asociada/prob

#comming soon...
def calcular_largos():
  pass
def contar_bacterias():
  pass