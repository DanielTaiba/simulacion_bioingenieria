import numpy as np
import pandas as pd
import json

def dist(x,y):
  return np.power((np.power(x,2)+np.power(y,2)),0.5)

def definir_vecindad_general(r:int,type_neighbor:str):
    x = np.linspace(-r,r,2*r+1)
    y = np.linspace(-r,r,2*r+1)
    X,Y = np.meshgrid(abs(x),abs(y))
    
    if type_neighbor == 'Circle':
        P=np.where(dist(X,Y)<=(((r+1)**2)-2)**0.5,1,0)  # funcion de la vecindad redonda
        c=(2*r+1)//2 #centro
        P[c,c]=0

    elif type_neighbor == 'Neumann':
        P=np.where(X+Y<=r,1,0)
        c=(2*r+1)//2 #centro
        P[c,c]=0

    elif type_neighbor == 'Moore':
        P=np.where(dist(X,Y)>=0,1,0)
        c=(2*r+1)//2 #centro
        P[c,c]=0
    
    else:
        assert False, 'escoja un tipo de vecindad valida (Circle, Neumann or Moore)'
    
    return P

def vector_vecindad(r:int,type_neighbor:str):
  vecindad = definir_vecindad_general(r,type_neighbor)
  return np.argwhere(vecindad==1) - r

def validar_posicion(pos,m):
    pos=np.where(pos>=m,pos-m,pos)
    pos=np.where(pos<0,m+pos,pos)
    return pos

def calcular_vecindad(matriz,r,type_neighbor):#devuelve la probabilidad asociada a cada punto
  m,n = matriz.shape
  vector = vector_vecindad(r,type_neighbor)
  prob=vector.shape[0]
  vecindad_asociada = np.zeros((m,n))

  for a,b in np.argwhere(matriz==1):
    posiciones = validar_posicion(vector+np.array([a,b]),m)
    vecindad_asociada[posiciones[:,0],posiciones[:,1]]+=1 

  for a,b in np.argwhere(matriz==1):
    vecindad_asociada[a,b]=0 
  
  return vecindad_asociada/prob


########## Files #################
def writeJsonFile(data:dict,fileName:str, mode:str = 'w'):
    with open(fileName,mode) as file:
        file.write(json.dumps(data,indent=4))

def write_csv(matriz,filename,colum,i):
	M,N=matriz.shape
	iteracion = np.zeros((1,N))
	fila = np.array([[i for i in range(N)]]) 
	pd.DataFrame(np.concatenate((iteracion+i,fila,matriz),axis=0).T,columns=colum).to_csv(filename,mode='a',index=False,header=False)

def general_stats(dir,nro_sim,cant_iter):
    flag = True
    for i in range(1,nro_sim+1):
        with open(dir+f'simulacion_{i}.json','r') as f:
            data = json.load(f)
            data['simulacion'] = [i for _ in range(cant_iter+1)]
            data['iteracion'] = [j for j in range(cant_iter+1)]
            if flag:
                pd.DataFrame(data=data).to_csv('general_stats.csv',index=False)
                flag=False
            else:
                pd.DataFrame(data=data).to_csv('general_stats.csv',index=False,mode='a',header=False)

if __name__=='__main__':
    general_stats('./experimentos/',10,100)