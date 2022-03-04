import numpy as np
import pandas as pd
from itertools import product

matriz=[[1,0,0,0,4],
        [2,0,0,0,0],
        [3,0,1,0,0],
        [0,0,0,0,0],
        [5,0,0,0,1]]
matriz = np.array(matriz)
M=5
filename = 'test.csv'
colum=[f'{i},{j}' for i,j in product(range(M),range(M))]
pd.DataFrame(columns=colum).to_csv(filename)
print(matriz.reshape(-1))
df = pd.DataFrame(matriz.reshape(1,M*M),columns=colum)
print(df)
df.to_csv(filename, mode='a', index=False, header=False)