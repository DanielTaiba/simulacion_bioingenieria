import numpy as np

def dist(x,y):
  return np.power((np.power(x,2)+np.power(y,2)),0.5)

def definir_vecindad_general(r):
  x = np.linspace(-r,r,2*r+1)
  y = np.linspace(-r,r,2*r+1)
  X,Y = np.meshgrid(abs(x),abs(y))
  P=np.where(dist(X,Y)<=(((r+1)**2)-2)**0.5,1,0)
  c=(2*r+1)//2 
  P[c,c]=0
  return P
  
def vector_vecindad(r):
  vecindad = definir_vecindad_general(r)
  return np.argwhere(vecindad==1) - r
 
if __name__=='__main__':
  for i in range (1,16):
    print(definir_vecindad_general(i))

  print(vector_vecindad(1))