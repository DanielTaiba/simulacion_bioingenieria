import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
import cv2 as cv

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
            )
        )
    fig.update_layout(
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
    return fig

def write_video(file_path, frames, fps):
    """
    https://www.youtube.com/watch?v=y4v6K3-s3mE
    https://docs.opencv.org/3.4/dd/d9e/classcv_1_1VideoWriter.html#ad59c61d8881ba2b2da22cff5487465b5
    Writes frames to an mp4 video file
    :param file_path: Path to output video, must end with .mp4
    :param frames: List of PIL.Image objects
    :param fps: Desired frame rate
    """

    w, h = cv.imread(frames[0]).shape[:2]
    fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
    
    img_array = []
    for frame in frames:
        img_array.append( cv.imread(frame))

    video = cv.VideoWriter(file_path, fourcc, fps, (w, h))
    for i in range(0, len(img_array)):
        video.write(img_array[i])
    
    video.release()

if __name__=='__main__':
    #parametros
    num_simulacion = 1
    filename = f'./experimentos/simulacion_{num_simulacion}.csv'

    #cargamos los datos
    df = pd.read_csv(filename)
    #creamos la carpeta para las imagenes y video
    if not os.path.exists("images"):
        os.mkdir("images")

    #guardamos las imagenes
    nb_frames = int(max(df['iteracion']))
    for i in range(nb_frames+1):
        plot(df[df['iteracion']==i],df.columns[2:]).write_image(f"images/fig{i}.png") #https://plotly.com/python/static-image-export/

    #creamos video
    frames = [f"images/fig{i}.png" for i in range(nb_frames+1)]
    write_video('images/video.mp4',frames,1)