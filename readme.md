# PartVis - Ferramentas para Visualização de Partículas
Conjunto de rotinas para auxiliar os usuários de língua portuguesa do modelo MOHID Lagrangian (http://www.mohid.com/pages/models/mohidlagrangian/mohid_lagrangian_home.shtml) no processo de visualização dos resultados gerados.
## Mapas
As rotinas para geração de mapas utiliza os arquivos HDF5 para criar um mapa para cada passo de tempo selecionado pelo usuário. Ao final do processamento, é criando um arquivo animado em formato gif contendo todos os passos de tempo selecionados.
### partvis_caixas_gif.py
Gera mapas com a posição das partículas emitidas pelo método de caixas.
### partvis_fontepontual_gif.py
Gera mapas com a posição das partículas emitidas a partir de fontes pontais.

## Gráficos
Os gráficos são gerados a partir dos arquivos netCDF obtidos após a etapa de "postproc".
### partvis_caixas_tempoderesidencia_postproc.py
Gera um gráfico de tempo no eixo X e percentual das partículas que deixaram o domínio do modelo no eixo Y. Aplicável a simulações onde a emissão das partículas se deu apenas em um instante inicial.
### partvis_fontepontual_postproc.py
Gera um gráfico de tempo no eixo X e número de partículas de cada fonte no interior da caixa selecionada para a análise. Aplicável a simulações onde a emissão das partículas se dá de forma pontual contínua.