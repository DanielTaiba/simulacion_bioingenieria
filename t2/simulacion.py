import numpy as np
import pandas as pd
from itertools import product
import random

#funcion para crear matriz
def crear_matriz(M,P):
  matriz  = np.zeros((M,M))
  bacterias = int(M*M*P)
  asignaciones = 0

  while asignaciones<bacterias:
    x,y = np.random.randint(M),np.random.randint(M)
    if matriz[x,y]==0:
      matriz[x,y]=1
      asignaciones+=1

  return matriz

#funciones para definir un vector que indique todos los puntos asociados a la vecindad desde un centro 0,0
def dist(x,y):
  return np.power((np.power(x,2)+np.power(y,2)),0.5)

def definir_vecindad_general(r):
  x = np.linspace(-r,r,2*r+1)
  y = np.linspace(-r,r,2*r+1)
  X,Y = np.meshgrid(abs(x),abs(y))
  P=np.where(dist(X,Y)<=(((r+1)**2)-2)**0.5,1,0)
  c=(2*r+1)//2 #centro
  P[c,c]=0
  return P
  
def vector_vecindad(r):
  vecindad = definir_vecindad_general(r)
  return np.argwhere(vecindad==1) - r

#propiedad vecindad infinita
def validar_posicion(pos,m):
  pos=np.where(pos>=m,pos-m,pos)
  pos=np.where(pos<0,m+pos,pos)
  return pos

#funcion para cambios de estados 
def step(matriz,m,t1,t2,r,pm):
  
  #calculamos los vectores de la vecindad asociada
  vector = vector_vecindad(r)
  
  #definimos el orden de las casillas para aplicar regla A y B
  posiciones_matriz = [(a,b) for a,b in product(range(m),range(m))]
  random.shuffle(posiciones_matriz)#ordenamos al azar las posiciones de la matriz
  #variables para almacenar los cambios
  cant_regla_A = 0
  cant_regla_B = 0

  for x,y in posiciones_matriz:

    posicion_vecindad = validar_posicion(vector+np.array([x,y]),m)

    if matriz[x,y]==1:#aplicar regla A
      
      cambiar=np.array([True,False])
      
      if np.random.choice(cambiar,p=[pm,1-pm]):
        #buscamos celdas vacias dentro de la vecindad para seleccionar una al azar (x1,y1)
        posicion_valida = np.where((matriz[posicion_vecindad[:,0],posicion_vecindad[:,1]]==0))
        try: #intentamos seleccionar una posicion, pero puede suceder que esten todas ocupadas
          
          choice = np.random.choice(posicion_valida[0])
          x1,y1=posicion_vecindad[choice,:]
          #cambiamos las celdas
          matriz[x,y] = 0
          matriz[x1,y1] = 1
          cant_regla_A+=1
        except:
          pass

    else: #regla B
      #contamos la cantidad de vecinos
      vecinos = np.where((matriz[posicion_vecindad[:,0],posicion_vecindad[:,1]]==1))
      cant_vecinos= vecinos[0].size
      # si esta dentro de los parametros se agrega una bacteria
      if cant_vecinos>=t1 and cant_vecinos<=t2:
        cant_regla_B+=1
        matriz[x,y] = 1
    
  return matriz,cant_regla_A,cant_regla_B


def simulacion(m,p,t1,t2,pm,r,iteraciones,salto_iter,nro_exp):
  #Simular matriz inicial
  matriz = crear_matriz(m,p)
  #datos
  results = []
  sum_regla_A,sum_regla_B = 0,0
  results.append([nro_exp,0,np.count_nonzero(matriz)/(m*m),sum_regla_A,sum_regla_B])

  for i in range(1,iteraciones+1):
    matriz,regla_A,regla_B = step(matriz,m,t1,t2,r,pm)
    sum_regla_A+=regla_A
    sum_regla_B+=regla_B

    if i%salto_iter==0:
      results.append([nro_exp,i,np.count_nonzero(matriz)/(m*m),sum_regla_A,sum_regla_B])
      sum_regla_A=0
      sum_regla_B=0


  if iteraciones%salto_iter!=0 :
    results.append([nro_exp,i,np.count_nonzero(matriz)/(m*m),sum_regla_A,sum_regla_B])

  return results

if __name__ == '__main__':
  #parametros
  M = 32
  P = 0.2
  T1,T2 = 6,7 #T1 = phi1,T2 = phi2
  PM = 0.4
  R = 1
  iteraciones = 102

  #parametros experimentos en simultaneo
  salto_iter = 10 #cada cuantas iteraciones medimos
  cant_experimentos= 50
  

  #datos df
  filename='experimentos.csv'
  col = ['nro_experimento','iteracion','cant_bacterias','cant_cambios_regla_A','cant_cambios_regla_B']
  pd.DataFrame(columns=col).to_csv(filename,mode='w',index=False)
  
  #experimentos
  for nro_exp in range(1,cant_experimentos+1):
    print(f'realizando experimento {nro_exp} ...')
    result = simulacion(M,P,T1,T2,PM,R,iteraciones,salto_iter,nro_exp)
    pd.DataFrame(np.array(result),columns=col).to_csv(filename,mode='a',index=False,header=False)

  
  