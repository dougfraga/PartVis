"""
Created on Feb 28 18:44:56 2024

@author: Douglas Fraga Rodrigues
"""
###############################################################################
# Bibliotecas
###############################################################################
import numpy as np
from datetime import timedelta
import matplotlib.dates as mdates
import xarray as xr
import glob
import matplotlib.pyplot as plt
import os


###############################################################################
# Definição dos parâmetros pelo usuário
###############################################################################
# Definir o caminho completo os os resultados gerados pelo postproc foram
# armazenados
nc_path = 'C:\mohid\lagrangian\MOHID-Lagrangian-master\RUN_Cases\BG\BG_summer_boxes_out\postProcess_PostRecipe_summer_poly'


# Definir o título do gráfico
title = 'Verão'


# Definir o nome das caixas dentro do dicionário
# com base no índice do arquivo .shp configurado no postproc
boxes_name = {
    0: 'bg',
    1: 'global'
    }


# Definir quais caixas serão analisadas com base no índce do dicionário boxes_name
boxes_to_analyze = [0]    # ex: caixa bg


###############################################################################
# Rotina
###############################################################################
# Configurar o diretório de trabalho
abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

# Listar os arquivos .nc armazenados no diretório de trabalho
list_files = glob.glob(os.path.join(nc_path,'*.nc'))

# Definir o nome do arquivo de entrada
file = list_files[0]
filename = file[:-3]

# Carregar o arquivo de entrada
ds = xr.open_dataset(file)

# Converter a variável de tempo para formato de texto
dt = ds.time.to_pandas().dt.strftime('%d/%m/%Y')


###############################################################################
# Gráficos
###############################################################################
# Gerar figuras para cada caixa selecionada
for i in boxes_to_analyze:
    fig, ax = plt.subplots(figsize=(10, 6))
    for k, v in enumerate(boxes_name.items()):
        counts = ds[f'n_counts_{boxes_name[v[0]]}'].values[:,:]
        rt = (1 - (counts/counts[0])) * 100
        
        # Desconsiderar os rios que as partículas não chegaram na caixa em questão
        mask_nan = np.isnan(counts)
        all_nan = mask_nan.all()
        if all_nan == False:
            ax.plot(dt, rt, label=v[1], linewidth=2)

                    
    ax.set_ylabel('Percentual de partículas que deixaram o domínio', size=11)
    ax.grid()
    ax.set_xlim(min(dt), max(dt))
    ax.set_ylim(0, 100)
    
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.xticks(dt[::2], rotation=80)            # Define o intervalo dos dias e rotaciona as datas para melhor visualização
    plt.title(title, size=15)
    fig.subplots_adjust(left=0.12, right=0.95, top=0.9, bottom=0.2)
    plt.savefig(f'{filename}_residence_time_{boxes_name[i]}.png')
    print(f'Gráfico da {boxes_name[i]} criado com sucesso!')

