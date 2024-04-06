import os
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import cartopy.crs as ccrs
import numpy as np
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


def make_map(projection=ccrs.PlateCarree()):
    fig, ax = plt.subplots(figsize=(9, 13),
                           subplot_kw=dict(projection=projection))

    gl = ax.gridlines(draw_labels=True)
    gl.top_labels = gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return fig, ax


# Função para criar um quadro (frame) do GIF
def create_frame(angle):
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x + angle)

    plt.plot(x, y)
    
    # Salvar o gráfico como uma imagem temporária
    filename = f'frame_{angle:.2f}.png'
    plt.savefig(filename)
    plt.close()

    return filename


def criar_gif(output_path, fps, frames):
    # Número de quadros (frames) no GIF
    num_frames = frames

    # Criar os quadros e salvá-los como imagens temporárias
    filenames = [create_frame(angulo) for angulo in np.linspace(0, 2*np.pi, num_frames)]

    # Inverter a ordem dos quadros
    filenames.reverse()

    # Criar o GIF usando os quadros gerados e configurar a velocidade de reprodução (fps)
    with imageio.get_writer(output_path, mode='I', fps=fps) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    # Remover as imagens temporárias
    for filename in set(filenames):
        os.remove(filename)

    print(f'GIF criado com sucesso em: {output_path}')

