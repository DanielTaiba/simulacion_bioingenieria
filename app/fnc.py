import plotly.graph_objects as go
from simulacion import vector_vecindad,validar_posicion
import numpy as np
from plotly.subplots import make_subplots 

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

def plot(df_iter,col,incluir_vecindad,title,r):
  if incluir_vecindad:
    vecindad = calcular_vecindad(df_iter[col].values,r)
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
      title=title+f' con vecindad {r}',
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
  fig.update_layout(
    width=800,
    height=800,
  )
  return fig

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
        showlegend=False,
        height=cant_rows*450,
      ) 
  return fig
  
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
          width=700,
          height=700,
          scene=dict(
                      zaxis=dict(range=[-0.1, 6.8], autorange=False),
                      aspectratio=dict(x=1, y=1, z=1),
                      ),
          updatemenus = [
              {
                  "buttons": [
                      {
                          "args": [None, frame_args(150)],
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

  return fig