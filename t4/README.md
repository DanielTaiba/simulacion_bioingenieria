# Funcionamiento
1. se correra la simulacion, la cual creara una carpeta llamada experimentos (puede se modificable este directorio) con los detalles de cada simulacion
2. tambien se creara un archivo llamado "general_stats.csv" con todos los del pedido 2
3. para graficar se debera ejecutar el archivo graficos.py para ver la simulacion X en la iteracion Y (son parametros)

# Pasos para ejecutarlo
## instalar librerias
```
pip install -r requirements.txt
```

## ejecutar simulacion.py
- se pueden cambiar los parametros cuando iniciamos la simulacion: (mas menos linea 160)
```
simulacion=lab(
            M=32,
            P=0.15,
            R=1,
            PM=0.05,
            T1=5,
            T2=7,
            num_simulacion=i,
            path=dir
        )
```

## ver graficos: ejecutar graficos.py
