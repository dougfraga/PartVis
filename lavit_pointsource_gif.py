"""
Created on Feb 28 18:44:56 2024

@author: Douglas Fraga Rodrigues
"""
###############################################################################
# Bibliotecas
###############################################################################
import numpy as np
from datetime import datetime
import h5py as hdf
import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io import shapereader
import os
import aux_funcs as axf


###############################################################################
# Definição dos parâmetros pelo usuário
###############################################################################
# Definir o caminho completo onde os arquivos .hdf5 gerados pelo postproc
# foram armazenados
hdf5_path = 'C:\mohid\lagrangian\MOHID-Lagrangian-master\RUN_Cases\BG\BG_winter_rivers_out\postProcess_PostRecipe_winter_poly_hdf5'


# Definir o título da figura
simulation_type = 'Simulação de Inverno'


# Definir os limites do mapa a ser gerado
extent = [
    -43.3,      # Longitude Mínima
    -43,        # Logitude Máxima
    -23,        # Latitude Mínima
    -22.65      # Latitude Máxima
    ]


# Definir o intervalo entre passos de tempo que será gerado um gráfico
dt = 1


# Definir o nome dos rios dentro do dicionário
river_name = {
    1: 'Canal do Mangue',
    2: 'Canal do Cunha',
    3: 'Rio Irajá',
    4: 'Rio São João de Meriti',
    5: 'Rio Sarapuí',
    6: 'Rio Iguaçu',
    7: 'Rios Estrela Inhomirim Saracuruna',
    8: 'Rio Suruí',
    9: 'Rio Iriri',
    10: 'Rio Roncador',
    11: 'Canal de Magé',
    12: 'Rio Macacu',
    13: 'Rio Guapimirim',
    14: 'Rio Caceribu',
    15: 'Rios Guaxindiba Alcantra',
    16: 'Rio Imboassu'
}


###############################################################################
# Rotina
###############################################################################
abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

# Define the coast boundary shape file
shp = shapereader.Reader(r'aux_files\BR_Pais_2022.shp')

list_files = glob.glob(os.path.join(hdf5_path,'*.hdf5'))
list_files = list_files[::dt]

for file in list_files:
    filename = file[:-5]
    f = hdf.File(file, 'r')
    
    lon = f['Results/Group_1/Data_1D/Longitude/Longitude_00001'][:]
    lat = f['Results/Group_1/Data_1D/Latitude/Latitude_00001'][:]
    origin_id = f['Results/Group_1/Data_1D/Origin ID/Origin ID_00001'][:]

    # Acessando o valor bruto (raw) do DataArray
    dt_value = f['Time/Time_00001'][:]

    # Convertendo para objeto datetime
    ano, mes, dia, hora, minuto, segundo = [int(valor) for valor in dt_value]
    dt_py = datetime(ano, mes, dia, hora, minuto, segundo)
    
    # Formatando a string de data e hora usando strftime
    datetime_label = dt_py.strftime('%d/%m/%Y %H:%M')
    datetime_filename = dt_py.strftime('%Y%m%d_%H%M')
    print(datetime_label)
    
    ###############################################################################
    # Gráficos
    ###############################################################################    
    fig, ax = axf.make_map(projection=ccrs.PlateCarree())
    ax.set_extent(extent)
    
    scatter = plt.scatter(lon, lat, c=origin_id, cmap='turbo', s=2)

    # Criar uma legenda para cada valor único em origin_id
    unique_origin_ids = np.unique(origin_id)
    legend_labels = [f'{river_name[int(origin_id)]}' for origin_id in unique_origin_ids]

    # Criar uma legenda com cores correspondentes às classes
    handles = [plt.Line2D([0], [0], linestyle='None', marker='o', color=scatter.to_rgba(origin_id), 
                          markersize=10, label=label) for origin_id, label in zip(unique_origin_ids, legend_labels)]

    # Adicionar a legenda
    plt.legend(handles=handles, title='Legenda', bbox_to_anchor=(.9, -.03), ncol=2)
    
    for record, geometry in zip(shp.records(), shp.geometries()):
        ax.add_geometries([geometry], ccrs.PlateCarree(), facecolor='lightgray')

    plt.title(f'{simulation_type}\n{datetime_label}')
    plt.savefig(f'{filename}_map_{datetime_filename}.png')

    # GIF output file name
    gif_name = f'{file[:-11]}.gif'


# Número de quadros (frames) no GIF
num_frames = np.size(list_files)


# Chamada da função para criação do gif
if __name__ == '__main__':
    axf.criar_gif(gif_name, fps=2, frames=num_frames)
