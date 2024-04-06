"""
Created on Feb 28 18:44:56 2024

@author: Douglas Fraga Rodrigues
"""
###############################################################################
# Bibliotecas
###############################################################################
import numpy as np
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
nc_path = 'C:\mohid\lagrangian\MOHID-Lagrangian-master\RUN_Cases\BG\BG_winter_rivers_out\postProcess_PostRecipe_winter_poly'


# Definir o título do gráfico
title = 'Inverno'


# Definir o tipo de métrica
# 0: Contagem de partículas por caixa
# 1: Concentração de partículas por área da caixa
metrica = 0


# Definir o nome dos rios dentro do dicionário
river_name = {
    1: ['Canal do Mangue', 1],
    2: ['Canal do Cunha', 1],
    3: ['Rio Irajá', 1],
    4: ['Rio São João de Meriti', 3],
    5: ['Rio Sarapuí', 1],
    6: ['Rio Iguacu', 3],
    7: ['Rios Estrela Inhomirim Saracuruna', 3],
    8: ['Rio Suruí', 3],
    9: ['Rio Iriri', 1],
    10:[ 'Rio Roncador', 1],
    11:[ 'Canal de Magé', 1],
    12:[ 'Rio Macacu', 1],
    13:[ 'Rio Guapimirim', 3],
    14:[ 'Rio Caceribu', 3],
    15:[ 'Rios Guaxindiba Alcantra', 1],
    16:[ 'Rio Imboassu', 1],
}


# Definir o nome das caixas dentro do dicionário
# com base no índice do arquivo .shp configurado no postproc
boxes_name = {
    0: 'Caixa 6',
    1: 'Caixa 5',
    2: 'Caixa 2',
    3: 'Caixa 7',
    4: 'Caixa 8',
    5: 'Caixa 1',
    6: 'Controle',
    7: 'Caixa 4',
    8: 'Caixa 3'
    }


# Definir quais caixas serão analisadas com base no índce do dicionário boxes_name
boxes_to_analyze = [5, 8, 7, 3]    # ex: caixas 1, 3, 4 e 7


###############################################################################
# Rotina
###############################################################################
metric_option = {
    0: ['n_counts_',
        'Contagem de partículas\npor caixa', 
        'particulas_por_caixa'],
    1: ['concentration_area_n_counts_',
        'Concentração de partículas\npor área da caixa',
         'concentracao_por_area']
    }

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
# Definir os valores extremos do eixo y
###############################################################################
miny = 999999999999999
maxy = 0

for i in boxes_to_analyze:
    for k, v in enumerate(river_name.items()):
        counts = ds[f'{metric_option[metrica][0]}{river_name[v[0]][0]}'].values[:,i]       
        # Desconsiderar os rios que as partículas não chegaram na caixa em questão
        mask_nan = np.isnan(counts)
        all_nan = mask_nan.all()
        if all_nan == False:
            min_temp = np.nanmin(counts)
            max_temp = np.nanmax(counts)
            if min_temp < miny:
                miny = min_temp
            if max_temp > maxy:
                maxy = max_temp


###############################################################################
# Gráficos
###############################################################################
# Gerar figuras para cada caixa selecionada
for i in boxes_to_analyze:
    fig, ax = plt.subplots(figsize=(10, 9))
    for k, v in enumerate(river_name.items()):
        counts = ds[f'{metric_option[metrica][0]}{river_name[v[0]][0]}'].values[:,i]
        
        # Desconsiderar os rios que as partículas não chegaram na caixa em questão
        mask_nan = np.isnan(counts)
        all_nan = mask_nan.all()
        if all_nan == False:
            ax.plot(dt, counts, label=v[1][0], linewidth=river_name[v[0]][1])

    ax.legend(title='Legenda', bbox_to_anchor=(.55, -.3), ncol=2)
                    
    ax.set_ylabel(f'{metric_option[metrica][1]}', size=11)
    ax.grid()
    ax.set_xlim(min(dt), max(dt))
    ax.set_ylim(miny, maxy)
    
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.xticks(dt[::2], rotation=80)            # Define o intervalo dos dias e rotaciona as datas para melhor visualização
    plt.title(f'{boxes_name[i]} / {title}', size=15)
    fig.subplots_adjust(left=0.12, right=0.95, top=0.9, bottom=0.4)
    plt.savefig(f'{filename}_{metric_option[metrica][2]}_{boxes_name[i]}.png')
    print(f'Gráfico da {boxes_name[i]} criado com sucesso!')

