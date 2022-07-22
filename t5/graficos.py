import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots #https://plotly.com/python-api-reference/generated/plotly.subplots.make_subplots.html
from utils import calcular_vecindad

#funcion para graficar una matriz
def plot(df_iter,col,incluir_vecindad,title,r,type_neighboor):
    if incluir_vecindad:
        vecindad = calcular_vecindad(df_iter[col].values,r,type_neighboor)
        fig = go.Figure()
        fig.add_trace(
        go.Heatmap(
                    z=df_iter[col].values*1.1+vecindad,
                    x=col,
                    y=df_iter['fila'],
                    colorscale='Blues',
                    texttemplate="%{z}"
                    )
        )
        fig.update_layout(
        title=title+' mostrando su vecindad ',
        #legend_title_text='1.1 -> esta la bacteria ahi\n[0.0,1.0] -> no hay bacteria pero se le asigna una probabilidad segun la cantidad de bacterias vecinas que tiene esa casilla'
        )
    else:
        fig = go.Figure()
        fig.add_trace(
        go.Heatmap(
                    z=df_iter[col].values,
                    x=col,
                    y=df_iter['fila'],
                    colorscale='Blues',
                    texttemplate="%{z}"
                    )
        )
        fig.update_layout(
        title=title+' sin vecindad'
        )
    fig.show()

#funciones para graficar multiples iteraciones
def un_subplot(df_iter,col,color='Blues'):
  return go.Heatmap(
                z=df_iter[col].values,
                x=col,
                y=df_iter['fila'],
                colorscale=color,
                #texttemplate="%{z}"
                )

def definir_grid(n):
    min_cols,max_cols = 2,5
    cant_cols=min(max(int(round(n**0.5)+0.5),min_cols),max_cols)
    cant_rows=n//cant_cols
    if n%cant_cols>0:
        cant_rows+=1
    return cant_rows,cant_cols

def subplots(df,n):
    max_iter = int(max(df['iteracion']))
    nums_iter = [i for i in range(0,max_iter,n)] + [max_iter]
    cant_rows,cant_cols = definir_grid(len(nums_iter))
    subtitles= tuple([f'Iteracion {i}' for i in nums_iter])
    col_names = df.columns[2:]

    fig  = make_subplots(
            rows = cant_rows, cols = cant_cols,
            subplot_titles=subtitles,
            )
    
    cont=0
    for r in range(1,cant_rows+1):
        for c in range(1,cant_cols+1):
            if cont<len(nums_iter):
                fig.add_trace(un_subplot(df[df['iteracion']==nums_iter[cont]],col_names),
                            row=r,col=c)
        cont+=1
    
    fig.update_layout(
            title="Posicion bacterias segun iteracion",
            showlegend=False
        ) 
    
    fig.show()

#funciones para hacer la animacion
def frame_args(duration):
    return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        }

def animation(df,col):
    nb_frames = int(max(df['iteracion']))
    fig = go.Figure(frames=[go.Frame(data=un_subplot(df[df['iteracion']==k],col),
        name=str(k) )# you need to name the frame for the animation to behave properly
        for k in range(nb_frames+1)])
    # Add data to be displayed before animation starts
    fig.add_trace(un_subplot(df[df['iteracion']==0],col))
    sliders = [
                {
                    "pad": {"b": 10, "t": 60},
                    "len": 0.9,
                    "x": 0.1,
                    "y": 0,
                    "steps": [
                        {
                            "args": [[f.name], frame_args(0)],
                            "label": str(k),
                            "method": "animate",
                        }
                        for k, f in enumerate(fig.frames)
                    ],
                }
            ]

    # Layout
    fig.update_layout(
            title='Animacion de la evolución bacteriana según iteración',
            width=900,
            height=900,
            scene=dict(
                        zaxis=dict(range=[-0.1, 6.8], autorange=False),
                        aspectratio=dict(x=1, y=1, z=1),
                        ),
            updatemenus = [
                {
                    "buttons": [
                        {
                            "args": [None, frame_args(500)],
                            "label": "&#9654;", # play symbol
                            "method": "animate",
                        },
                        {
                            "args": [[None], frame_args(0)],
                            "label": "&#9724;", # pause symbol
                            "method": "animate",
                        },
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 70},
                    "type": "buttons",
                    "x": 0.1,
                    "y": 0,
                }
            ],
            sliders=sliders
    )

    fig.show()

if __name__=='__main__':
    #parametros
    num_simulacion = 3
    R=1
    type_neighboor = 'Moore'
    iteracion = 100 #que iteracion graficamos
    filename = f'./experimentos/simulacion_{num_simulacion}.csv'

    #cargamos los datos
    df = pd.read_csv(filename)
    jump_plots = 5 #cada cuantas iteraciones se muestra un grafico en subplots
    jump_animations = 5 # cada cuantas iteracionse se muestra un grafico en la animacion (aun no implementado)
    incluir_vecindad = True

    ## graficos

    ### importante: en la funcion plot() si se agrega vecindad la nomenclatura es la siguiente, caso sin vecindad se asignan valores 0 o 1 como siempre
    ###     valor 1.1 indica que la bacteria esta en esta posicion, 
    ###     valores en el intervalo [0.0,1.0] indica que no hay bacteria pero se le asigna una probabilidad calculada como (total de vecinos posibles/vecinos reales de la casilla)
    
    # grafico de una iteracion 
    # plot(df[df['iteracion']==iteracion],df.columns[2:],incluir_vecindad,'Matriz incial',R) #matriz 
    plot(df[df['iteracion']==0],df.columns[2:],True,'Matriz incial',R,type_neighboor) #matriz  sin vecindad
    plot(df[df['iteracion']==iteracion],df.columns[2:],True,'Matriz final',R,type_neighboor) #matriz  sin vecindad
    #subplots con una muestra general de las iteraciones
    subplots(df,jump_plots) 
    #animacion de la evolucion de iteraciones
    animation(df,df.columns[2:]) 