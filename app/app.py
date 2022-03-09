from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from fnc import plot,animation,subplots
from dash.dependencies import Input, Output

app = Dash(__name__)

df = pd.read_csv('csv/t1.csv')
min_iter,max_iter = int(min(df['iteracion'])),int(max(df['iteracion']))

titulo = html.H1(children='Simulación 1',style={'text-align':'center'})
descripcion = html.Div(children=[
    html.H2(children="Descripcion de la simulacion",style={'padding-bottom':'40px'}),
    html.P("Se pretende simular la dinamica de cambio de un entorno bacteriano con tiempos sucesivos en base a las siguientes reglas establecidas empiricamente "),
    
    html.Li('una bacteria se moverá de espacio en cada iteracion con probabilidad P en su vecindad de radio R siempre y cuando esa casilla no este ocupada',style={'margin-left':'50px'}),
    html.Li('para cada casilla vacia cuya vecindad este entre parametros T1<= cant vecinos <= T2 se asignará una bacteria',style={'margin-left':'50px'}),
    html.Li('el espacio simulado representa una vecindad infinita, por lo cual en condiciones borde se incluyen vecinos al otro lado de la matriz',style={'margin-left':'50px'})
],style={'width':'50%','margin':'50px','margin-top':'0','margin-left':'0'})
simulacion = html.Div(children = [
    dcc.Graph(
        id='animation',
        figure=animation(df,df.columns[2:]),)
],style={'width':'50%'})

nums_iter=[i for i in range(min_iter,max_iter+1,1)]
comparacion = html.Div(children = [
    html.H2('Comparacion de estados (default: inicial vs final)'),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                dcc.Dropdown(nums_iter,nums_iter[0],id='comp-drop-1'),
                dcc.Tabs(id="comp-tabs-1", value='sin vecindad', children=[
                    dcc.Tab(label='Sin Vecindad', value='sin vecindad'),
                    dcc.Tab(label='Con Vecindad', value='con vecindad'),
                ],style={'margin':'10px'}),
                dcc.RadioItems([i for i in range(1,4,1)],1,inline=True,id='r-1'),
            ]),
            dcc.Graph(id='comp-graph-1')
        ],
        style={
            'width':'50%',
            'height':'600px'
        }),
        html.Div(children=[
            html.Div(children=[
                dcc.Dropdown(nums_iter,nums_iter[-1],id='comp-drop-2'),
                dcc.Tabs(id="comp-tabs-2", value='sin vecindad', children=[
                    dcc.Tab(label='Sin Vecindad', value='sin vecindad'),
                    dcc.Tab(label='Con Vecindad', value='con vecindad'),
                ],style={'margin':'10px'}),
                dcc.RadioItems([i for i in range(1,4,1)],1,inline=True,id='r-2'),
            ]),
            dcc.Graph(id='comp-graph-2')
        ],
        style={
            'width':'50%',
            'height':'100%'
        }),
    ],
    style={
        'display': 'flex',
        'align-items': 'flex-end',
        'height':'600px'
    }),

    ],style={'height':'1000px'})


ver_iter = html.Div(children=[
    html.H2('overview iteraciones'),
    dcc.Slider(1, 50, 1, value=10,id='slider-ver-iter'),
    dcc.Graph(id='subplots'),
    
],style={'height':'1200px'})

@app.callback(Output('comp-graph-1', 'figure'),
              Input('comp-tabs-1', 'value'),
              Input('comp-drop-1','value'),
              Input('r-1','value'))
def render_content(tab,num_iter,r):
    if tab == 'sin vecindad':
        return plot(df[df['iteracion']==num_iter],df.columns[2:],False,f'iteracion {num_iter}',r)
    elif tab == 'con vecindad':
        return plot(df[df['iteracion']==num_iter],df.columns[2:],True,f'iteracion {num_iter}',r)
@app.callback(Output('comp-graph-2', 'figure'),
              Input('comp-tabs-2', 'value'),
              Input('comp-drop-2','value'),
              Input('r-2','value'))
def render_content(tab,num_iter,r):
    if tab == 'sin vecindad':
        return plot(df[df['iteracion']==num_iter],df.columns[2:],False,f'iteracion {num_iter}',r)
    elif tab == 'con vecindad':
        return plot(df[df['iteracion']==num_iter],df.columns[2:],True,f'iteracion {num_iter}',r)
@app.callback(Output('subplots', 'figure'),
              Input('slider-ver-iter', 'value'))
def render_content(jump_plots):
    return subplots(df,jump_plots)

app.layout = html.Div(children=[
    titulo,
    html.Div(children=[descripcion,simulacion],style={'display': 'flex','align-items': 'flex-start',}),
    comparacion,
    ver_iter
])

if __name__ == '__main__':
    app.run_server(debug=True)