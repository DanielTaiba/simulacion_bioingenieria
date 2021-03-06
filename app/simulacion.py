import numpy as np
import pandas as pd

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
  #identificamos posicion y cantidad de bacterias en la matriz
  pos_bacterias=np.argwhere(matriz==1)
  cant_bacterias =pos_bacterias.shape[0]
  
  #aqui se almacenan los cambios que se realizarán (-1 si cambia de posicion la bacteria, 0 si no hace nada, 1 si llega a la posicion la bacteria)
  matriz_cambio = crear_matriz(m,0.0)  
  #aqui se almacenan los vecinos asociados a cada celda vacia(valores de 0 a cant_bacterias)
  vecindad_asociada = crear_matriz(m,0.0)

  #definimos que bacterias cambian
  cambios = np.random.binomial(n=1,p=pm,size=cant_bacterias) #1 si cambia -> hacemos match entre la posicion del array con pos_bacterias

  for index in np.argwhere(cambios==1):
    
    a,b = pos_bacterias[index[0]]

    #definimos posiciones de la vecindad asociada a ese punto
    posiciones = validar_posicion(vector+np.array([a,b]),m)

    """Regla A"""
    #elegimos una posicion al azar
    try:

      posiciones_validas = np.where((matriz[posiciones[:,0],posiciones[:,1]]==0)&(matriz_cambio[posiciones[:,0],posiciones[:,1]]<1))#seleccionamos solo aquellas posiciones que estan libres y aun no han sido asignadas
      choice = np.random.choice(posiciones_validas[0])
      a1,b1=posiciones[choice,:]

      #almacenamos cambios
      
      if matriz[a1,b1]==0:#si la casilla no esta ocupada
        matriz_cambio[a,b]=-1
        matriz_cambio[a1,b1]=1
    except: # si no hay espacios donde asignar, no hace nada
      pass

    """se utiliza para regla B"""
    #contamos la cantidad de vecinos asociados a una celda
    vecindad_asociada[posiciones[:,0],posiciones[:,1]]+=1 
  
  #eliminamos la vecindad asociada para aquellas celdas donde hay bacterias
  for a,b in pos_bacterias:
    vecindad_asociada[a,b]=0 
  """Regla B"""
  pos_vecindad_asociada = np.argwhere((vecindad_asociada>=t1) & (vecindad_asociada<=t2)) 
  for a,b in pos_vecindad_asociada:
    if matriz_cambio[a,b]==0:
      matriz_cambio[a,b]=1
  
  #devolvemos la matriz resultante y la vecindad por si a caso
  return matriz+matriz_cambio,vecindad_asociada

def write_csv(matriz,filename,colum,i):
	M,N=matriz.shape
	iteracion = np.zeros((1,N))
	fila = np.array([[i for i in range(N)]]) 
	pd.DataFrame(np.concatenate((iteracion+i,fila,matriz),axis=0).T,columns=colum).to_csv(filename,mode='a',index=False,header=False)

if __name__ == '__main__':
  #parametros
  M = 32
  P = 0.08
  T1,T2 = 5,7 #T1 = phi1,T2 = phi2
  PM = 0.6
  R = 2
  iteraciones = 1000


  #Simular matriz inicial
  matriz = crear_matriz(M,P)
  print('bacterias iniciales: ',np.count_nonzero(matriz))
  #iniciamos csv
  filename = 'test.csv'
  colum= ['iteracion','fila']+[str(i) for i in range(M)]
  pd.DataFrame(columns=colum).to_csv(filename,mode='w',index=False)
  write_csv(matriz,filename,colum,0)

  for i in range(iteraciones):
    matriz,vecinos = step(matriz,M,T1,T2,R,PM)
    write_csv(matriz,filename,colum,i+1)
  print('bacterias finales: ',np.count_nonzero(matriz))