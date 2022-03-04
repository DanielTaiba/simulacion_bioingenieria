from matplotlib.pyplot import grid
import plotly.express as px
import numpy as np 

def plot(matriz):
  fig = px.imshow(matriz.T,
                labels=dict(x="pos_X", y="pos_Y", color="Existe bacteria"),
                x=[str(i)for i in range(matriz.shape[0])],
                y=[str(i)for i in range(matriz.shape[1])],
                color_continuous_scale='Blues'
               )
  fig.update_xaxes(side="top")

  fig.show()

def subplots():
  pass

matriz=[[0,0,0,0,1],
        [0,0,0,0,0],
        [0,0,1,0,0],
        [0,0,0,0,0],
        [1,0,0,0,1]]

matriz = np.array(matriz)
plot(matriz)