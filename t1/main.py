from simulacion import crear_matriz,write_csv,step
from graficos import plot,subplots,animation
import pandas as pd

if __name__ == '__main__':
  #Parametros
  M = 32
  P = 0.08
  T1,T2 = 5,7 #T1 = phi1,T2 = phi2
  PM = 0.6
  R = 1
  iteraciones = 100
  filename = 'simulacion.csv' #aqui guardamos los datos de la simulacion

  #Creamos matriz inicial
  matriz = crear_matriz(M,P)

  #iniciamos csv
  colum= ['iteracion','fila']+[str(i) for i in range(M)]
  pd.DataFrame(columns=colum).to_csv(filename,mode='w',index=False)
  write_csv(matriz,filename,colum,0)

  #Realizamos iteraciones y guardamos sus datos
  for i in range(iteraciones):
    matriz,vecinos = step(matriz,M,T1,T2,R,PM)
    write_csv(matriz,filename,colum,i+1)
  
  #graficando
  ## parametros
  df = pd.read_csv(filename)
  jump_plots = 5 #cada cuantas iteraciones se muestra un grafico en subplots
  jump_animations = 5 # cada cuantas iteracionse se muestra un grafico en la animacion (aun no implementado)
  incluir_vecindad = True

  ## graficos

  ### importante: en la funcion plot() si se agrega vecindad la nomenclatura es la siguiente, caso sin vecindad se asignan valores 0 o 1 como siempre
  ###     valor 1.1 indica que la bacteria esta en esta posicion, 
  ###     valores en el intervalo [0.0,1.0] indica que no hay bacteria pero se le asigna una probabilidad calculada como (total de vecinos posibles/vecinos reales de la casilla)
  
  plot(df[df['iteracion']==0],df.columns[2:],incluir_vecindad,'Matriz incial',R) #matriz inicial
  plot(df[df['iteracion']==0],df.columns[2:],False,'Matriz incial',R) #matriz inicial sin vecindad
  plot(df[df['iteracion']==iteraciones],df.columns[2:],incluir_vecindad,'Matriz incial',R) #matriz final
  plot(df[df['iteracion']==iteraciones],df.columns[2:],False,'Matriz incial',R) #matriz final sin vecindad
  subplots(df,jump_plots) #subplots con una muestra general de las iteraciones
  animation(df,df.columns[2:]) #animacion de la evolucion de iteraciones