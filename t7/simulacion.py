import numpy as np
import pandas as pd
from itertools import product
import random
import os
from utils import definir_vecindad_general, validar_posicion, writeJsonFile, write_csv, general_stats

class lab():
    def __init__(
        self,
        M:int=32,
        PiW:float=0.05,
        PiM:float=0.05,
        R:int=1,
        M_T1:int=5,
        M_T2:int=7,
        W_T1:int=5,
        W_T2:int=7,
        W_EV:int=3,
        M_EV:int=3,
        type_neighboor:str='Circle',
        num_simulacion:int=0,
        path:str='./t7/experimentos/'
        ) -> None:

        #Parametos iniciales
        self.rows = M
        assert (PiM+PiW) < 1, f'la suma de las probabilidades debe ser menor a 1 => PiM:{PiM} + PiW:{PiW} es mayor a 1'
        self.proporcion_mutante_inicial = PiM
        self.proporcion_salvaje_inicial = PiW
        self.radio = R

        #files
        self.name_csv = f'simulacion_{num_simulacion}.csv'
        self.name_json = f'simulacion_{num_simulacion}.json'
        self.path = path

        ## Parametros Regla B
        self.wt1 = W_T1
        self.wt2 = W_T2
        self.mt1 = M_T1
        self.mt2 = M_T2

        #parametros Regla E
        self.wev = W_EV
        self.mev = M_EV

        # Calculos iniciales
        self.type_neighboor = type_neighboor
        self.matriz_inicial = self.__crear_matriz()
        self.vector_vecindad = self.__calcular_vector_vecindad()

        # Estados
        self.num_iteracion = 0
        self.matriz_actual = self.matriz_inicial
        self.stats = {
            'cambios_mutantes':[0],
            'cambios_salvajes':[0],
            'cantidad_mutantes':[int(np.where(self.matriz_inicial == 1,1,0).sum())],
            'cantidad_salvajes':[int(np.where(self.matriz_inicial == 2,1,0).sum())],
            'cantidad_total':[int(np.count_nonzero(self.matriz_inicial))],
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
        bacterias_mutantes = int(self.rows*self.rows*self.proporcion_mutante_inicial)
        bacterias_salvajes = int(self.rows*self.rows*self.proporcion_salvaje_inicial)
        asignaciones = 0

        #asignamos bacterias mutantes
        while asignaciones<bacterias_mutantes:
            x,y = np.random.randint(self.rows),np.random.randint(self.rows)
            if matriz[x,y]==0:
                matriz[x,y]=1
                asignaciones+=1
        #asignamos bacterias salvajes
        while asignaciones<(bacterias_mutantes+bacterias_salvajes):
            x,y = np.random.randint(self.rows),np.random.randint(self.rows)
            if matriz[x,y]==0:
                matriz[x,y]=2
                asignaciones+=1
        
        return matriz
    
    def __calcular_vector_vecindad(self):
        vecindad = definir_vecindad_general(self.radio,self.type_neighboor)
        return np.argwhere(vecindad==1) - self.radio

    def step_paralelo(self):
        self.num_iteracion += 1

        #identificamos posicion bacterias en la matriz
        pos_mutantes=np.argwhere(self.matriz_actual==1)
        pos_salvajes=np.argwhere(self.matriz_actual==2)

        #variables para almacenar la cuando cambian por cada regla
        cambios_bact_mutante = 0
        cambios_bact_salvaje = 0
        matriz_cambios = np.zeros((self.rows,self.rows))
        vecindad_asociada_mutante =  np.zeros((self.rows,self.rows))
        vecindad_asociada_salvaje =  np.zeros((self.rows,self.rows))
        
        #contamos la cantidad de vecinos por celda
        for x,y in pos_mutantes:
            vecindad = validar_posicion(self.vector_vecindad+np.array([x,y]),self.rows)
            vecindad_asociada_mutante[vecindad[:,0],vecindad[:,1]]+=1 

        #eliminamos la vecindad asociada para aquellas celdas donde hay bacterias
        for a,b in pos_mutantes:
            vecindad_asociada_mutante[a,b]=0 
        
        ## Repetimos para bacterias salvajes
        for x,y in pos_salvajes:
            vecindad = validar_posicion(self.vector_vecindad+np.array([x,y]),self.rows)
            vecindad_asociada_salvaje[vecindad[:,0],vecindad[:,1]]+=1 
        for a,b in pos_salvajes:
            vecindad_asociada_salvaje[a,b]=0 

        ## Aplicamos Regla B
        for a,b in product(range(self.rows),range(self.rows)):
            #si existe una bacteria en la posicion
            if self.matriz_actual[a,b] == 1 or self.matriz_actual[a,b] == 2:
                #no hace nada, ya hay una bacteria en esta posicion
                pass
            
            #si ambas bacterias estan dentro de los parameros t1...t2
            elif ((vecindad_asociada_mutante[a,b]>=self.mt1) and (vecindad_asociada_mutante[a,b]<=self.mt2)) and \
                ((vecindad_asociada_salvaje[a,b]>=self.wt1) and (vecindad_asociada_salvaje[a,b]<=self.wt2)):
                #lanzar una moneda al azar
                if random.randint(0, 1) == 0:
                    #agregamos mutante
                    matriz_cambios[a,b]=1
                    cambios_bact_mutante+=1
                else:
                    #agregamos salvaje
                    matriz_cambios[a,b]=2
                    cambios_bact_salvaje+=1

            #si la bacteria mutante esta en los parametros t1...t2
            elif ((vecindad_asociada_mutante[a,b]>=self.mt1) and (vecindad_asociada_mutante[a,b]<=self.mt2)) and \
                not ((vecindad_asociada_salvaje[a,b]>=self.wt1) and (vecindad_asociada_salvaje[a,b]<=self.wt2)):
                
                matriz_cambios[a,b]=1
                cambios_bact_mutante+=1
            
            #si la bacteria salvaje esta en los parametros t1...t2
            elif not((vecindad_asociada_mutante[a,b]>=self.mt1) and (vecindad_asociada_mutante[a,b]<=self.mt2)) and \
                ((vecindad_asociada_salvaje[a,b]>=self.wt1) and (vecindad_asociada_salvaje[a,b]<=self.wt2)):
                
                matriz_cambios[a,b]=2
                cambios_bact_salvaje+=1

        #actualizamos el estado de la matriz
        self.matriz_actual = self.matriz_actual+matriz_cambios
        #update stats
        self.stats['cambios_mutantes'].append(cambios_bact_mutante)
        self.stats['cambios_salvajes'].append(cambios_bact_salvaje)
        self.stats['cantidad_mutantes'].append(int(np.where(self.matriz_actual == 1,1,0).sum()))
        self.stats['cantidad_salvajes'].append(int(np.where(self.matriz_actual == 2,1,0).sum()))
        self.stats['cantidad_total'].append(np.count_nonzero(self.matriz_actual))
        #escribir la matriz actual en un csv
        write_csv(
            self.matriz_actual,
            self.path+self.name_csv,
            self.columns,
            self.num_iteracion)
        
    def eliminacion_bacterias(self):
        self.num_iteracion += 1

        #identificamos posicion bacterias en la matriz
        pos_mutantes=np.argwhere(self.matriz_actual==1)
        pos_salvajes=np.argwhere(self.matriz_actual==2)

        #variables para almacenar la cuando cambian por cada regla
        cambios_bact_mutante = 0
        cambios_bact_salvaje = 0
        matriz_cambios = np.zeros((self.rows,self.rows))
        
        #contamos la cantidad de vecinos por cada bacteria
        for x,y in pos_mutantes:
            vecindad = validar_posicion(self.vector_vecindad+np.array([x,y]),self.rows)
            if np.where(self.matriz_actual[vecindad[:,0],vecindad[:,1]]==1,1,0).sum() <= self.mev:
                matriz_cambios[x,y] = -1
                cambios_bact_mutante -= 1

        ## Repetimos para bacterias salvajes
        for x,y in pos_salvajes:
            vecindad = validar_posicion(self.vector_vecindad+np.array([x,y]),self.rows)
            if np.where(self.matriz_actual[vecindad[:,0],vecindad[:,1]]==2,1,0).sum() <= self.mev:
                matriz_cambios[x,y] = -2
                cambios_bact_salvaje -= 1

        #actualizamos el estado de la matriz
        self.matriz_actual = self.matriz_actual+matriz_cambios
        #update stats
        self.stats['cambios_mutantes'].append(cambios_bact_mutante)
        self.stats['cambios_salvajes'].append(cambios_bact_salvaje)
        self.stats['cantidad_mutantes'].append(int(np.where(self.matriz_actual == 1,1,0).sum()))
        self.stats['cantidad_salvajes'].append(int(np.where(self.matriz_actual == 2,1,0).sum()))
        self.stats['cantidad_total'].append(np.count_nonzero(self.matriz_actual))
        #escribir la matriz actual en un csv
        write_csv(
            self.matriz_actual,
            self.path+self.name_csv,
            self.columns,
            self.num_iteracion)


if __name__ == '__main__':

    #nombre de la carpeta donde se guardará la info
    dir = './experimentos/'
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    # cantidad de veces que se hará un experimento
    cantidad_simulaciones = 5
    # cantidad de ciclos que tendra cada experimento
    ciclo = {
        'adicion_bacterias' : 3, #cuantas veces se hace la regla B "de corrido"
        'eliminacion_bacterias' : 1, #cuantas veces se hace la regla E "de corrido"
        'total_ciclos': 5 #cuantos ciclos de regla B y E se completan -> total iteraciones = (regla_B + regla_E)* total_ciclos
    }

    print(f"""OJO:
    en total se realizaran {ciclo['total_ciclos'] * (ciclo['adicion_bacterias']+ciclo['eliminacion_bacterias'])} iteraciones por simulacion
    """)

    # ciclo para experimento
    for i in range(1,cantidad_simulaciones+1):
        print ('simulacion',i,'...')
        # iniciamos la simulacion del laboratorio con los parametros
        simulacion=lab(
            M=100,
            PiW=0.05,
            PiM=0.15,
            R=1,
            M_T1=3,
            M_T2=4,
            W_T1=2,
            W_T2=3,
            
            W_EV=2, #nuevas variables
            M_EV=2,
            
            type_neighboor='Circle', #opciones validas: Moore , Neumann , Circle (default) 
            #no cambiar
            num_simulacion=i,
            path=dir
        )
        for _ in range(ciclo['total_ciclos']):
            #se van agregando bacterias en cada iteracion
            [simulacion.step_paralelo() for _ in range(ciclo['adicion_bacterias'])]
            #se eliminan bacterias en cada iteracion
            [simulacion.eliminacion_bacterias() for _ in range(ciclo['eliminacion_bacterias'])]

        writeJsonFile(simulacion.stats,fileName=dir+f'simulacion_{i}.json')
    
    #datos de todos los experimentos como en el pedido 2
    general_stats(dir,cantidad_simulaciones,ciclo['total_ciclos'] * (ciclo['adicion_bacterias']+ciclo['eliminacion_bacterias']))