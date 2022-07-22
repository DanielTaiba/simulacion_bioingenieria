import numpy as np
import pandas as pd
import plotly.graph_objects as go


custom_color_scale=[
        [0.0, 'rgb(255,255,255)'], 
        [.2, 'rgb(255, 255, 153)'], 
        [.4, 'rgb(153, 255, 204)'], #color bacteria mutante
        [.6, 'rgb(179, 217, 255)'],#color bacteria mutante
        [.8, 'rgb(240, 179, 255)'],
        [1.0, 'rgb(255, 77, 148)']]#color bacteria salvaje

def plot(df_iter,col):
    fig = go.Figure()
    fig.add_trace(
        go.Heatmap(
            z=df_iter[col].values,
            x=col,
            y=df_iter['fila'],
            colorscale=custom_color_scale,
            texttemplate="%{z}"
            )
        )
    fig.update_layout(
        title='titulo...',
        width=800,
        height=800,
        xaxis=dict( #no funciona el grid
            showgrid=True,
            gridwidth=1, 
            gridcolor='black',
            linewidth=2,
            linecolor='black',
            mirror=True),
        yaxis=dict( 
            showgrid=True,
            gridwidth=1, 
            gridcolor='black',
            linewidth=2,
            linecolor='black',
            mirror=True),
        )
    fig.show()

#funciones para graficar animacion
def un_subplot(df_iter,col):    
    return go.Heatmap(
                z=df_iter[col].values*0.2,
                x=col,
                y=df_iter['fila'],
                colorscale=custom_color_scale,
                #texttemplate="%{z}"
                )
    

def frame_args(duration):
    return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        }

def animation(df,col):
    nb_frames = int(max(df['iteracion']))
    fig = go.Figure(frames=[go.Frame(
        data=un_subplot(df[df['iteracion']==k],col),
        name=str(k) # you need to name the frame for the animation to behave properly
        )for k in range(nb_frames+1)])
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
        title='Animacion de la evolución bacteriana según iteración (rosado = salvaje, celeste =Mutante)',
        width=800,
        height=800,
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
        sliders=sliders,
        xaxis=dict( #no funciona el grid
            showgrid=True,
            gridwidth=1, 
            gridcolor='black',
            linewidth=2,
            linecolor='black',
            mirror=True),
        yaxis=dict( 
            showgrid=True,
            gridwidth=1, 
            gridcolor='black',
            linewidth=2,
            linecolor='black',
            mirror=True),
    )

    fig.show()
if __name__=='__main__':
    #parametros
    num_simulacion = 1
    iteracion = 100 #que iteracion graficamos
    filename = f'./experimentos/simulacion_{num_simulacion}.csv'

    #cargamos los datos
    df = pd.read_csv(filename)
    # graficar una iteracion en particular
    plot(df[df['iteracion']==0],df.columns[2:]) 
    #animacion de la evolucion de iteraciones
    animation(df,df.columns[2:]) 


    #revisar como hacer un gif con la animacion
    #https://towardsdatascience.com/a-simple-way-to-turn-your-plots-into-gifs-in-python-f6ea4435ed3c