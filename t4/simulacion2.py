import numpy as np
import pandas as pd
import random
from itertools import product
from utils import definir_vecindad_general,validar_posicion,writeJsonFile,write_csv,general_stats
import os



class lab():
    def __init__(
            self,
            M:int=32,
            P:float=0.15,
            R:int=1,
            PM:float=0.6,
            T1:int=5,
            T2:int=7,
            num_simulacion:int=0,
            path:str='./experimentos/'
            ) -> None:
        
        #Parametos iniciales
        self.rows=M
        self.proporcion_inicial = P
        self.radio=R
        self.num_simulacion = num_simulacion
        #files
        self.name_csv = f'simulacion_{num_simulacion}.csv'
        self.name_json = f'simulacion_{num_simulacion}.json'
        self.path = path
        ## Parametros Regla A
        self.prob_mov=PM
        ## Parametros Regla B
        self.t1 = T1
        self.t2 = T2
        # Calculos iniciales
        self.matriz_inicial = self.__crear_matriz()
        self.vector_vecindad = self.__calcular_vector_vecindad()
        # Estados
        self.num_iteracion=0
        self.matriz_actual = self.matriz_inicial
        self.stats = {
            'cambios_regla_A':[0],
            'cambios_regla_B':[0],
            'cambios_regla_C':[0],
            'cantidad_bacterias':[np.count_nonzero(self.matriz_inicial)],
        }
        ## Creamos CSV para guardar los estados de la matriz
        self.columns= ['iteracion','fila']+[str(i) for i in range(M)]
        pd.DataFrame(columns=self.columns).to_csv(self.path+self.name_csv,mode='w',index=False)
        write_csv(
            self.matriz_inicial,
            self.path+self.name_csv,
            self.columns,
            self.num_iteracion)
                
    def __crear_matriz(self):
        matriz  = np.zeros((self.rows,self.rows))
        bacterias = int(self.rows*self.rows*self.proporcion_inicial)
        asignaciones = 0

        while asignaciones<bacterias:
            x,y = np.random.randint(self.rows),np.random.randint(self.rows)
            if matriz[x,y]==0:
                matriz[x,y]=1
                asignaciones+=1

        return matriz
        
    def __calcular_vector_vecindad(self):
        vecindad = definir_vecindad_general(self.radio)
        return np.argwhere(vecindad==1) - self.radio

    def regla_A(self,posicion,vecindad):
        x,y=posicion
        cambiar=np.array([True,False])
      
        if np.random.choice(cambiar,p=[self.prob_mov,1-self.prob_mov]):
            #buscamos celdas vacias dentro de la vecindad para seleccionar una al azar (x1,y1)
            posicion_valida = np.where((self.matriz_actual[vecindad[:,0],vecindad[:,1]]==0))
            try: #intentamos seleccionar una posicion, pero puede suceder que esten todas ocupadas
                choice = np.random.choice(posicion_valida[0])
                x1,y1=vecindad[choice,:]
                #cambiamos las celdas
                self.matriz_actual[x,y] = 0
                self.matriz_actual[x1,y1] = 1
                return 1
            except:
                return 0
        
        else:
            return 0
    
    def regla_B(self,posicion,vecindad):
        x,y = posicion
        #contamos la cantidad de vecinos
        vecinos = np.where((self.matriz_actual[vecindad[:,0],vecindad[:,1]]==1))
        cant_vecinos= vecinos[0].size
        # si esta dentro de los parametros se agrega una bacteria
        if cant_vecinos>=self.t1 and cant_vecinos<=self.t2:
            self.matriz_actual[x,y] = 1
            return 1
        else:
            return 0

    def regla_C(self,posicion,vecindad):
        x,y=posicion
        cambiar=np.array([True,False])
      
        if np.random.choice(cambiar,p=[self.prob_mov,1-self.prob_mov]):
            #buscamos celdas vacias dentro de la vecindad para seleccionar una al azar (x1,y1)
            posicion_valida = np.where((self.matriz_actual[vecindad[:,0],vecindad[:,1]]==0))
            try: #intentamos seleccionar una posicion, pero puede suceder que esten todas ocupadas
                choice = np.random.choice(posicion_valida[0])
                x1,y1=vecindad[choice,:]
                #cambiamos las celdas
                self.matriz_actual[x1,y1] = 1
                return 1
            except:
                return 0
        
        else:
            return 0
    
    def step(self,rules):
        self.num_iteracion+=1
        #definimos el orden de las casillas para aplicar regla A y B
        posiciones_matriz = [(a,b) for a,b in product(range(self.rows),range(self.rows))]
        random.shuffle(posiciones_matriz)#ordenamos al azar las posiciones de la matriz

        #variables para almacenar la cuando cambian por cada regla
        cambios_A = 0
        cambios_B = 0
        cambios_C = 0
        for x,y in posiciones_matriz:
            vecindad = validar_posicion(self.vector_vecindad+np.array([x,y]),self.rows)
            for rul in rules:
                if rul == 'A':
                    if  self.matriz_actual[x,y]==1:
                        cambios_A += self.regla_A(posicion=(x,y),vecindad=vecindad)
                    else:
                        pass
                elif rul == 'B':
                    if self.matriz_actual[x,y]==0:
                        cambios_B += self.regla_B(posicion=(x,y),vecindad=vecindad)
                elif rul == 'C':
                    if  self.matriz_actual[x,y]==1:
                        cambios_C += self.regla_C(posicion=(x,y),vecindad=vecindad)
                else:
                    print('no existe esta regla: ',rul)
    
        #update stats
        self.stats['cambios_regla_A'].append(cambios_A)
        self.stats['cambios_regla_B'].append(cambios_B)
        self.stats['cambios_regla_C'].append(cambios_C)
        self.stats['cantidad_bacterias'].append(np.count_nonzero(self.matriz_actual))
        #escribit la matriz actual en un csv
        write_csv(
            self.matriz_actual,
            self.path+self.name_csv,
            self.columns,
            self.num_iteracion)

class labRandom(lab):
    def __init__(self, M: int = 32, P: float = 0.15, R: int = 1, PM: float = 0.6, T1: int = 5, T2: int = 7, num_simulacion: int = 0, path: str = './experimentos/') -> None:
        super().__init__(M, P, R, PM, T1, T2, num_simulacion, path)

    def step(self,rules):
        self.num_iteracion+=1
        #definimos el orden de las casillas para aplicar regla A y B
        posiciones_matriz = [(a,b) for a,b in product(range(self.rows),range(self.rows))]
        random.shuffle(posiciones_matriz)#ordenamos al azar las posiciones de la matriz

        #variables para almacenar la cuando cambian por cada regla
        cambios_A = 0
        cambios_B = 0
        cambios_C = 0
        for x,y in posiciones_matriz:
            vecindad = validar_posicion(self.vector_vecindad+np.array([x,y]),self.rows)
            for rul in rules:
                if rul == 'A':
                    if  self.matriz_actual[x,y]==1:
                        cambios_A += self.regla_A(posicion=(x,y),vecindad=vecindad)
                    else:
                        pass
                elif rul == 'B':
                    if self.matriz_actual[x,y]==0:
                        cambios_B += self.regla_B(posicion=(x,y),vecindad=vecindad)
                elif rul == 'C':
                    if  self.matriz_actual[x,y]==1:
                        cambios_C += self.regla_C(posicion=(x,y),vecindad=vecindad)
                else:
                    print('no existe esta regla: ',rul)
    
        #update stats
        self.stats['cambios_regla_A'].append(cambios_A)
        self.stats['cambios_regla_B'].append(cambios_B)
        self.stats['cambios_regla_C'].append(cambios_C)
        self.stats['cantidad_bacterias'].append(np.count_nonzero(self.matriz_actual))
        #escribit la matriz actual en un csv
        write_csv(
            self.matriz_actual,
            self.path+self.name_csv,
            self.columns,
            self.num_iteracion)
        

class labParalelo(lab):

    def __init__(self, M: int = 32, P: float = 0.15, R: int = 1, PM: float = 0.6, T1: int = 5, T2: int = 7, num_simulacion: int = 0, path: str = './experimentos/') -> None:
        super().__init__(M, P, R, PM, T1, T2, num_simulacion, path)
        self.matriz_cambios = np.zeros((self.rows,self.rows))
        self.matriz_vecindad_asociada = np.zeros((self.rows,self.rows))

    def step(self,rules):
        self.num_iteracion+=1

        #identificamos posicion y cantidad de bacterias en la matriz
        pos_bacterias=np.argwhere(self.matriz_actual==1)
        cant_bacterias =pos_bacterias.shape[0]
        #variables para almacenar la cuando cambian por cada regla
        cambios_A = 0
        cambios_B = 0
        cambios_C = 0
        matriz_cambios = np.zeros((self.rows,self.rows))
        vecindad_asociada =  np.zeros((self.rows,self.rows))
        
        
        for x,y in pos_bacterias:
            vecindad = validar_posicion(self.vector_vecindad+np.array([x,y]),self.rows)
            vecindad_asociada[vecindad[:,0],vecindad[:,1]]+=1 

        #eliminamos la vecindad asociada para aquellas celdas donde hay bacterias
        for a,b in pos_bacterias:
            vecindad_asociada[a,b]=0 
        """Regla B"""
        pos_vecindad_asociada = np.argwhere((vecindad_asociada>=self.t1) & (vecindad_asociada<=self.t2)) 
        for a,b in pos_vecindad_asociada:
            if matriz_cambios[a,b]==0:
                matriz_cambios[a,b]=1
                cambios_B+=1

        self.matriz_actual = self.matriz_actual+matriz_cambios
        #update stats
        self.stats['cambios_regla_A'].append(cambios_A)
        self.stats['cambios_regla_B'].append(cambios_B)
        self.stats['cambios_regla_C'].append(cambios_C)
        self.stats['cantidad_bacterias'].append(np.count_nonzero(self.matriz_actual))
        #escribit la matriz actual en un csv
        write_csv(
            self.matriz_actual,
            self.path+self.name_csv,
            self.columns,
            self.num_iteracion)

if __name__=='__main__':
    #nombre de la carpeta donde se guardará la info
    dir = './experimentos3/'
    if not os.path.exists(dir):
        os.makedirs(dir)

    # cantidad de veces que se hará un experimento
    cantidad_simulaciones = 10
    # cantidad de iteraciones que tendra cada experimento
    cantidad_iteraciones = 100

    # ciclo para experimento
    for i in range(1,cantidad_simulaciones+1):
        print ('simulacion',i,'...')
        # iniciamos la simulacion del laboratorio con los parametros
        simulacion=labParalelo(
            M=32,
            P=0.15,
            R=1,
            PM=0.05,
            T1=3,
            T2=5,
            #no cambiar
            num_simulacion=i,
            path=dir
        )
        # ciclo para iterar
        for _ in range(cantidad_iteraciones):
            #rules es una lista que hace referencia a la secuencia de reglas que utilizara en las iteraciones 
            ## ejemplo => rules = ['A','B'] indica que cada iteracion se ejecuta la regla A y luego la regla B
            ## ejemplo => rules = ['B','C'] indica que cada iteracion se ejecuta la regla B y luego la regla C
            simulacion.step(rules = ['C','B'])
        
        writeJsonFile(simulacion.stats,fileName=dir+f'simulacion_{i}.json')
    
    #datos de todos los experimentos como en el pedido 2
    general_stats(dir,cantidad_simulaciones,cantidad_iteraciones)
        