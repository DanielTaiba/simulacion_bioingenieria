import numpy as np

def dist(x,y):
  return np.power((np.power(x,2)+np.power(y,2)),0.5)

def definir_vecindad_general(r:int,type_neighbor:str):
    x = np.linspace(-r,r,2*r+1)
    y = np.linspace(-r,r,2*r+1)
    X,Y = np.meshgrid(abs(x),abs(y))
    
    if type_neighbor == 'Circle':
        P=np.where(dist(X,Y)<=(((r+1)**2)-2)**0.5,1,0)  # funcion de la vecindad redonda
        c=(2*r+1)//2 #centro
        P[c,c]=0

    elif type_neighbor == 'Neumann':
        P=np.where(X+Y<=r,1,0)
        c=(2*r+1)//2 #centro
        P[c,c]=0

    elif type_neighbor == 'Moore':
        P=np.where(dist(X,Y)>=0,1,0)
        c=(2*r+1)//2 #centro
        P[c,c]=0
    
    else:
        assert False, 'escoja un tipo de vecindad valida (Circle, Neumann or Moore)'
    
    return P

def vector_vecindad(r:int,type_neighbor:str):
  vecindad = definir_vecindad_general(r,type_neighbor)
  return np.argwhere(vecindad==1) - r


if __name__=='__main__':
    print(vector_vecindad(1,'Moore'))