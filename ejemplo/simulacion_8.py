import random
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.spatial.distance import cdist

#------------------------------------------------------------------------------#
#----------------------------- Funciones creadas ------------------------------#
#------------------------------------------------------------------------------#
def create_p_grid(grid, p):
    # Creamos una matriz de probabilidad concéntrica
    try:
        lim = max(min(np.where(grid == 2)[0]), min(np.where(grid == 2)[1]))
        if len(p) >= lim:
            p_grid = np.tile(grid, 1).astype('float64')
            for i in range(len(p_grid)):
                for j in range(len(p_grid[0])):
                    if grid[i][j] != 2:
                        p_grid[i][j] = p[get_distance(grid, (i, j)) - 1]
                    else:
                        p_grid[i][j] = 0
            return(p_grid)
        else:
            print(f'Cuidado: el vector de probabilidad debe ser al menos de dimensión {lim}')
    except:
        pass

def create_grid(M, N, p = 0):
    # Creamos una matriz inicial cualquiera para probar la simulación.
    # Si se le pide una proporción de 1 en el valor p, entonces se hará
    # sin considerar la barra con valores dos.
    if p != 0:
        x = np.array([1, 0])
        lista = np.repeat(x, [round(M*N*p), round(M*N*(1 - p))], axis=0)
        random.shuffle(lista)
        grid = []
        k = 0
        for i in range(N):
            grid.append([])
            for j in range(M):
                grid[i].append(lista[k])
                k += 1
        return(grid)
    else:
        grid = []
        for i in range(N):
            grid.append([])
            for j in range(M):
                if i > N / 2 and (j > M / 3 and j < 2 * M / 3):
                    grid[i].append(2)
                else:
                    grid[i].append(0)
        return(grid)


def get_mean_distance(grid):
    def get_index_2d(a = [], val = 0, occurrence_pos = False):
        if not occurrence_pos:
            for k in range(len(a)):
                for j in range(len(a[k])):
                    if a[k][j] == val:
                        return (k, j)
        else:
            return [(k, j) for k in range(len(a)) for j in range(len(a[k])) if a[k][j] == val]
    index = get_index_2d(grid, 1, True)
    distancias = {}
    if len(index) > 1:
        for i in index:
            distancias_totales = {}
            for j in index:
                if i != j:
                    p = np.array(i)
                    q = np.array(j)
                    p, q = p.reshape(1, -1), q.reshape(1, -1)
                    out = cdist(p, q, metric='cityblock') # Utilizamos distancia manhattan
                    key = f'{p[0]}-{q[0]}'
                    #if f'{q[0]}-{p[0]}' not in distancias.keys():
                    distancias_totales[key] = out[0,0]
            distancias[key] = np.min(list(distancias_totales.values()))
        print('Distancia media: ', np.mean(list(distancias.values())))
    else:
        print('Distancia media: Deben haber al menos dos "uno", por ende no se calculará. ')


def get_distance(grid, cell):
    # Obtiene una matriz y una celda cuya distancia al dos más cercano
    # interesa conocer.
    if 0 <= cell[0] < len(grid) and 0 <= cell[1] < len(grid[0]):
        left1 = min(np.where(grid == 2)[0]), min(np.where(grid == 2)[1])
        right2 = max(np.where(grid == 2)[0]), max(np.where(grid == 2)[1])
        for r in range(0, max(len(grid), len(grid[0]))):
            min_i, max_i = left1[0] - r, right2[0] + r
            min_j, max_j = left1[1] - r, right2[1] + r
            if (min_i < cell[0] < max_i) and (min_j < cell[1] < max_j):
                #print(f'Distancia {r - 1}')
                return(r - 1)
                break
    else:
        print('Celda fuera del margen posible')


def get_distance_to_one(grid, cell):
    # Obtiene una matriz y una celda cuya distancia al uno más cercano
    # interesa conocer.
    if 0 <= cell[0] < len(grid) and 0 <= cell[1] < len(grid[0]):
        for r in range(0, max(len(grid), len(grid[0]))):
            if grid[cell[0], cell[1]] == 1:
                #print(f'Distancia {r - 1}')
                return(r - 1)
                break
    else:
        print('Celda fuera del margen posible')


def simulation_by_cell(grid, p_grid, max_iterations = 1000, rule = 1,
 phi = 0, phi_max = 0, prints = True):
    # Se simulan cambios de estado sobre las celdas cuyo valor sea 0.
    # Se recibe la matriz grid y la matriz de probabilidad p_grid que
    # hará cambiar o no los valores de la matriz. Se considera un máx
    # de un millón de iteraciones. Se retorna la matriz acualizada.
    # Existen cuatro posibles reglas para realizar la simulación. Por
    # defecto se considerará un rule = 1 y phi = 0.
    init_time = time.time()
    t = 0

    while len((np.where(grid == 0))[1]) > 0 and t < max_iterations:
        #print(grid)
        p = random.randrange(0, len(np.where(grid == 0)[0]))
        i_p, j_p = np.where(grid == 0)[0][p], np.where(grid == 0)[1][p]
        if rule == 1:
            p_t = random.random()
            if p_grid[i_p][j_p] >= p_t:
                grid[i_p][j_p] = 1
                #print('Se cambió una celda')
            else:
                #print('Una celda no cambió')
                pass
        elif rule == 2:
            c = list(get_neighbours(grid, (i_p, j_p)).values()).count(1)
            if c == 0:
                p_t = random.random()
                if p_grid[i_p][j_p] >= p_t:
                    grid[i_p][j_p] = 1
                    #print('Se cambió una celda')
                else:
                    #print('Una celda no cambió')
                    pass
        elif rule == 3:
            c = list(get_neighbours(grid, (i_p, j_p)).values()).count(1)
            if c >= phi:
                grid[i_p][j_p] = 1
            else:
                # Qué pasaría si no es mayor o igual a phi?
                pass
        elif rule == 4:
            c = list(get_neighbours(grid, (i_p, j_p)).values()).count(1)
            if c >= phi:
                grid[i_p][j_p] = 0
            else:
                # Qué pasaría si no es mayor o igual a phi?
                grid[i_p][j_p] = 1
                pass
        elif rule == 5:
            c = list(get_neighbours(grid, (i_p, j_p)).values()).count(1)
            if (c >= phi and c <= phi_max):
                grid[i_p][j_p] = 1
            else:
                pass
        t += 1
    end_time = time.time()
    if prints:
        if t == max_iterations:
            print(f'Se ha alcanzado el máximo de iteraciones')
            print(f'Quedan aún {len((np.where(grid == 0))[1])} ceros')
        else:
            print(f'No quedan celdas negativas luego de {t} iteraciones')
        print(f'Tiempo transcurrido: {round(end_time - init_time, 1)} ')
    return(grid)


def get_neighbours(grid, cell):
    # Se recibe una matriz y la tupla referente a la posición de la celda
    # cuyos vecinos interesa encontrar. Se retorna un diccionario tal que
    # sus llaves correspondan a la posición de cada celda adyacente y los
    # valores corresponden a la representación numérica de dicha celda.
    neighbours = {}
    N, M = len(grid), len(grid[0])
    # Se verifican las ocho celdas adyacentes a la celda dada.
    options = ((-1, 0), (0, -1),
               (+1, 0), (0, +1),
               (+1, +1), (-1, -1),
               (+1, -1), (-1, +1))
    for d_i, d_j in options:
        if (0 <= cell[0] + d_i < N) and (0 <= cell[1] + d_j < M):
            x, y = cell[0] + d_i, cell[1] + d_j
            # Se agregan las celdas adyacentes a un diccionario.
            neighbours[(x, y)] = grid[x][y]
        else:
            # Se ponen las opciones en caso de considerar vecindad infinita
            x, y = cell[0] + d_i, cell[1] + d_j
            if (cell[0] + d_i >= N):
                x = 0
            if (cell[0] + d_i < 0):
                x = -1
            if (cell[1] + d_j >= M):
                y = 0
            if (cell[1] + d_j < 0):
                y = -1
            neighbours[(x, y)] = grid[x][y]


    return(neighbours)


def plot_ts(time_serie):
    x, y = time_serie
    fig, ax = plt.subplots()
    ax.set_title('Serie temporal: Cantidad de unos por iteración',
                 fontsize = 14)

    plt.xlabel('Número de iteraciones')
    plt.ylabel('Cantidad de celdas == 1')
    plt.plot(x,y,marker="o")
    plt.gcf().set_size_inches(12, 9)
    plt.show()


def plot_matrix(iter, size, grid, p_grid, rule = 1, phi = 0, phi_max = 0):
    i, j = size
    
    
    fig, axs = plt.subplots(i, j)
    fig.suptitle('Evolución de matriz conforme al número de iteraciones')
    iter_t = iter
    x, y = [], []
    for i in range(len(axs[0])):
        for j in range(len(axs)):
            grid = simulation_by_cell(grid, p_grid, iter, rule, phi, phi_max, prints = False)
            colors = ['#252850'] # Colores para [2, 0, 1]
            cmap = mpl.colors.ListedColormap(colors, name='colors', N=None)
            if np.count_nonzero(grid == 0) == 0:
                axs[i, j].imshow(grid,  cmap=cmap)
            else:
                axs[i, j].imshow(grid,  cmap=plt.cm.Blues)
            #cmap = mpl.colors.ListedColormap(colors, name='colors', N=None)
            #axs[i, j].imshow(grid,  cmap=plt.cm.Blues)
            axs[i, j].set_title(f'Iter = {iter_t}')
            occurrences = np.count_nonzero(grid == 1)
            y.append(occurrences)
            x.append(iter_t)
            print(f'Cantidad de unos en iteración {iter_t}: {occurrences}')
            iter_t += iter
    densidad = np.count_nonzero(grid == 1) / abs(np.count_nonzero(grid == 1) + np.count_nonzero(grid == 0))
    print(f'Densidad poblacional de unos: {densidad}')
    plt.gcf().set_size_inches(12, 9)
    fig.tight_layout()
    return(x, y)


#------------------------------------------------------------------------------#
#------------------------- Cálculo real de los largos -------------------------#
#------------------------------------------------------------------------------#

def ignorarConexiones(matriz, indice1, indice2):
  matriz[indice1,indice2] = 0
  if (indice1 < matriz.shape[0]-1) and (matriz[indice1+1,indice2]): matriz = ignorarConexiones(matriz, indice1+1, indice2)
  if (indice1 > 0) and (matriz[indice1-1,indice2]): matriz = ignorarConexiones(matriz, indice1-1, indice2)
  if (indice2 < matriz.shape[1]-1) and (matriz[indice1,indice2+1]): matriz = ignorarConexiones(matriz, indice1, indice2+1)
  if (indice2 > 0) and (matriz[indice1,indice2-1]): matriz = ignorarConexiones(matriz, indice1, indice2-1)
  return matriz

def todosLosCaminos(matriz, indice1, indice2, caminos, raiz=False):
  matriz[indice1,indice2] = 0
  los_caminos = [[[indice1,indice2]]]+[camino+[[indice1,indice2]] for camino in caminos]
  los_caminos1 = []
  los_caminos2 = []
  los_caminos3 = []
  los_caminos4 = []
  if (indice1 < matriz.shape[0]-1) and (matriz[indice1+1,indice2]):
    los_caminos1 += todosLosCaminos(matriz, indice1+1, indice2, los_caminos)
  if (indice1 > 0) and (matriz[indice1-1,indice2]):
    los_caminos2 += todosLosCaminos(matriz, indice1-1, indice2, los_caminos)
  if (indice2 < matriz.shape[1]-1) and (matriz[indice1,indice2+1]):
    los_caminos3 += todosLosCaminos(matriz, indice1, indice2+1, los_caminos)
  if (indice2 > 0) and (matriz[indice1,indice2-1]):
    los_caminos4 += todosLosCaminos(matriz, indice1, indice2-1, los_caminos)
  los_caminos += los_caminos1+los_caminos2+los_caminos3+los_caminos4
  if (raiz):
    n_caminos = len(los_caminos)
    for camino_ind1 in range(n_caminos-1):
      for camino_ind2 in range(camino_ind1+1,n_caminos):
        conectables = (los_caminos[camino_ind1][0] == los_caminos[camino_ind2][0]) or\
                      (los_caminos[camino_ind1][0] == los_caminos[camino_ind2][-1]) or\
                      (los_caminos[camino_ind1][-1] == los_caminos[camino_ind2][0]) or\
                      (los_caminos[camino_ind1][-1] == los_caminos[camino_ind2][-1])
        compartido = []
        if (conectables == 1):
          conectables = 0
          for par in los_caminos[camino_ind1]:
            if (par in los_caminos[camino_ind2]):
              conectables += 1
              compartido = par
              if (conectables == 2): break
        if (conectables == 1):
          los_caminos += [los_caminos[camino_ind1]+[par for par in los_caminos[camino_ind2] if (par != compartido)]]
  matriz[indice1,indice2] = 1
  return los_caminos

def caminosMasLargos(matriz):
  #Hay que partir identificando un elemento de cada isla
  islas = matriz.copy()
  for ind1 in range(matriz.shape[0]):
    for ind2 in range(matriz.shape[1]):
      if (islas[ind1, ind2]):
        islas = ignorarConexiones(islas, ind1, ind2)
        islas[ind1, ind2] = 1
  #A continuación, toca ver todos los caminos posibles
  caminos_mas_largos = []
  for ind1 in range(matriz.shape[0]):
    for ind2 in range(matriz.shape[1]):
      if (islas[ind1, ind2]):
        caminos = todosLosCaminos(matriz.copy(), ind1, ind2, [], True)
        caminos_mas_largos += [max(caminos,key=len)]
  return caminos_mas_largos#, islas #(En caso de que quieras ver un punto de cada isla)

#------------------------------------------------------------------------------#
#-------------------------- Estimación de los largos --------------------------#
#------------------------------------------------------------------------------#

def generarDirectorio(matriz, indice1, indice2):
  matriz[indice1,indice2] = 0
  coordenadas = [np.array([indice1,indice2])]
  if (indice1 < matriz.shape[0]-1) and (matriz[indice1+1,indice2]):
    coordenadas_temp = generarDirectorio(matriz, indice1+1, indice2)
    coordenadas += coordenadas_temp
  if (indice1 > 0) and (matriz[indice1-1,indice2]):
    coordenadas_temp = generarDirectorio(matriz, indice1-1, indice2)
    coordenadas += coordenadas_temp
  if (indice2 < matriz.shape[1]-1) and (matriz[indice1,indice2+1]):
    coordenadas_temp = generarDirectorio(matriz, indice1, indice2+1)
    coordenadas += coordenadas_temp
  if (indice2 > 0) and (matriz[indice1,indice2-1]):
    coordenadas_temp = generarDirectorio(matriz, indice1, indice2-1)
    coordenadas += coordenadas_temp
  return coordenadas

def estimacionRapidoDeLargos(matriz):
  #Hay que partir identificando cada isla
  islas = matriz.copy()
  coor = []
  for ind1 in range(matriz.shape[0]):
    for ind2 in range(matriz.shape[1]):
      if (islas[ind1, ind2]):
        coor_temp = generarDirectorio(islas, ind1, ind2)
        coor += [coor_temp]
        islas[ind1, ind2] = 1
  #Y luego se hace la estimación sobre cada isla
  largos = []
  for isla in coor:
    adyacencia = np.zeros((len(isla), len(isla)))
    for ind1 in range(len(isla)):
      for ind2 in range(len(isla)):
        if (np.abs(isla[ind1]-isla[ind2]).sum() == 1):
          adyacencia[ind1, ind2] = 1
          adyacencia[ind2, ind1] = 1
    largos += [len(adyacencia) - round((adyacencia.sum(axis=1) > 2).sum()/2)] 
  return largos#, (np.vstack(np.where(islas == 1)).T).tolist() #(En caso de querer una coordenada de cada isla)



##############################################################################
##############################################################################
##############################################################################
##############################################################################
########################## Parámetros modificables: ##########################

# Sistema en posición inicial
M, N = 16, 16 # Columns, Rows
proporcion = 0.1  # Se pone la proporción de unos, ejemplo: 0.4 indica un 40% de unos.
phi_max = 2 #Phi máximo para considerar regla 5
phi_min = 1 # Phi mínimo para considerar regla 4
N_iteracion = 50 # Aquí se pone cada cuantas iteraciones quieres ver el gráfico

#########################################b############bb##b###################1
##########b#######b#################b###########################################
##########################bbb########################bb##########################
##############################################################################
##############################################################################

grid = np.array(create_grid(M, N, proporcion))
# No olvidar de definir la matriz de probabilidad cada vez que se cree
# una nueva matriz de valores.
p = [0.8, 0.7, 0.6, 0.4, 0.3, 0.25, 0.2, 0.1, 0.01, 0.005, 0.003, 0.001]
p_grid = create_p_grid(grid, p)
#print('Matriz inicial:')
#print(grid)
#print('---------------------------------------------------------------------------------------------------------------')

fig, ax = plt.subplots()

 ################## RRESULTADOS ###########################

# Imprimiremos la matriz inicial

ax.matshow(grid, cmap=plt.cm.Blues)
 

#---------Estimación de largos inicial------------#

print("Maximo en largos inicial :", estimacionRapidoDeLargos(grid))

data=estimacionRapidoDeLargos(grid)
mean=sum(data)/len(data)

print("Promedio de islas inicial: ", mean)
Max_value=max(data)
print("Isla MAX inicial: ", Max_value)
Min_value=min(data)
print("Isla MIN inicial : ",Min_value)
Largoi=len(data)
print("Cantidad de islas inicial: ",Largoi)


#______________________________________-

time_serie = plot_matrix(1, (4, 4), grid, p_grid, 5, phi_min, phi_max)


time_serie2 = plot_matrix(N_iteracion, (4, 4), grid, p_grid, 5, phi_min, phi_max)


t1 = time_serie[0]
t1 = t1 + time_serie2[0]
t2 = time_serie[1]
t2 = t2 + time_serie2[1]
print('>>', (t1, t2))


plot_ts((t1, t2)) # Aquí se grafica la serie de tiempo
plt.show()


#---------Distancia promedio 1 ------------#

#-------------------------- Distancia promedio de 1s --------------------------#
#------------------------------------------------------------------------------#

#Esta función toma una matriz de 1s y 0s, y retorna la distancia promedio entre todos los 1s
def distanciaPromedio1s(matriz):
  #Primero hay que encontrar todas las ubicaciones de los 1s
  coor_1s = []
  for ind1 in range(matriz.shape[0]):
    for ind2 in range(matriz.shape[1]):
      if (matriz[ind1, ind2]): coor_1s += [np.array([ind1, ind2])]
  #Luego sólo hay que sumar las distancias
  n_distancias = len(coor_1s)*(len(coor_1s)-1)/2 #(Fórmula del número triangular)
  distancia_promedio = 0
  for coor1 in range(len(coor_1s)-1):
    for coor2 in range(coor1+1, len(coor_1s)):
      distancia_promedio += np.abs(coor_1s[coor1] - coor_1s[coor2]).sum()
  #Y, finalmente, sólo queda dividirlas por el número de distancias sumadas
  distancia_promedio /= n_distancias
  return distancia_promedio

#print('Distancia promedio entre 1s:', distanciaPromedio1s(grid))



#---------Estimación de largos final ------------#

print("Maximo en largos:", estimacionRapidoDeLargos(grid))

data=estimacionRapidoDeLargos(grid)
mean=sum(data)/len(data)

print("Promedio de islas: ", mean)
Max_value=max(data)
print("Isla MAX: ", Max_value)
Min_value=min(data)
print("Isla MIN: ",Min_value)
Largoi=len(data)
print("Cantidad de islas final: ",Largoi)




