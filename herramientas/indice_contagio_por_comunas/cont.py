#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 11:55:42 2020
@author: esteban
"""

# Este script necesita que instales 
# conda install geopandas
#conda install -c conda-forge descartes


import geopandas as gp
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys



shp_path = "../../fuentes/geometrias_comunas/comunas.shp"
comunasChile = gp.read_file(shp_path)
#aprovechamos al toque de calcular la superficie de cada comuna en km2
comunasChile['superficie']=comunasChile.to_crs({'init': 'epsg:3035'}).area/10**6


## Primero necesitamos cargar los polígonos de las comunas.
# poligonos descargados desde https://www.bcn.cl/siit/mapas_vectoriales/index_html
shp_path = "../../fuentes/geometrias_comunas/comunas.shp"
comunasChile = gp.read_file(shp_path)
#aprovechamos al toque de calcular la superficie de cada comuna en km2
comunasChile['superficie']=comunasChile.to_crs({'init': 'epsg:3035'}).area/10**6



## Luego cargamos los datos del COVID19
datosComunas = datosComunas = pd.read_excel('info.xlsx')


'''
comunasChile.columns =  
Index(['objectid', 'shape_leng', 'dis_elec', 'cir_sena', 'cod_comuna',
       'codregion', 'st_area_sh', 'st_length_', 'Region', 'Comuna',
       'Provincia', 'geometry'],
      dtype='object')
'''
## Necesitamos que las columnas tengan el mismo nombre:
comunasChile['nombre_comuna']=comunasChile.Comuna
############################################################

df=comunasChile.merge(datosComunas, on='nombre_comuna')
'''
df.columns=
Index(['id_region', 'nombre_region', 'id_comuna', 'nombre_comuna', 'poblacion',
       'casos_totales', 'tasa', 'objectid', 'shape_leng', 'dis_elec',
       'cir_sena', 'cod_comuna', 'codregion', 'st_area_sh', 'st_length_',
       'Region', 'Comuna', 'Provincia', 'geometry'],
      dtype='object')
 '''
 
### Los datos por Comuna tienen que ser arreglados.
#   Primero, a partir de la columna de tasa y la de población, hay que
#   reconstruir los datos de los casos (porque sólo informan cuando hay más
# de 4 casos)

df['casos_totales']=df.casos_totales.replace('-',0)
df['casos_totales']=df.casos_totales.fillna(0)
df['casos_totales']=df.casos_totales.astype(int)
df['tasa']=df.tasa.fillna(0)
df['tasa']=df.tasa.astype(float)
df['poblacion']=df.poblacion.fillna(0)

##Ahora corregimos los datos de los casos totales.
df['casos_totales']=(df.tasa*df.poblacion/100000).round(0).astype(int)

df['nombre_comuna']=df.nombre_comuna.replace('San Juan de la Costa','S.J. de la Costa')

######################################
######################################
######################################
######################################

#   CALCULO DE RIESGO = casos*poblacion/superficie

######################################
######################################
######################################
######################################
df['riesgo']=df['casos_totales']*df['poblacion']/df['superficie']
# Lo normalizamos!
df['riesgo']=df['riesgo']/df['riesgo'].max()
df['casos_pp']=df['casos_totales']/df['poblacion']*100000

df['casos_totales']=df['casos_totales'].astype(int)
import seaborn as sns

#c=[['casos_totales','Casos Totales','%i'],['casos_pp','Casos por 100.000 habitantes','%i'],['riesgo','Indice de Riesgo','%.2f']]

c=[['riesgo','Indice de Riesgo','%.2f']]



caracteristica=caso[0]
titulo=caso[1]
t=caso[2]


#top10=df[df.nombre_region!='Metropolitana'][['nombre_comuna',caracteristica]].sort_values(caracteristica,ascending=False).head(10)
top10=df[['nombre_comuna',caracteristica]].sort_values(caracteristica,ascending=False).head(10)
top10=top10.reset_index(drop=True)


cuarentena_total=['Las Condes', 'Hualpén', 'San Pedro', 'Chillán', 'Chillán Viejo',\
                  'Temuco', 'Padre las Casas', 'Nueva Imperial', 'Osorno','Punta Arenas']    
cuarentena_parcial=['Puente Alto', 'Santiago','Ñuñoa']
paleta_rojos=['red']*10#sns.color_palette("Reds",10)#sns.color_palette("bwr",50)[40:50]
paleta_verdes=['lime']*10#sns.color_palette("Greens_r",20)[0:10]
paleta_naranjos=['yellow']*10#sns.color_palette("Oranges_r",20)[0:10]


paleta=paleta_verdes#['green']*10 #sns.color_palette("winter",10)
i=0
for bool in top10.nombre_comuna.isin(cuarentena_total):
    if bool:
        paleta[i]=paleta_rojos[i]#'tomato'
    i+=1
i=0
for bool in top10.nombre_comuna.isin(cuarentena_parcial):
    if bool:
        paleta[i]=paleta_naranjos[i]#'lightyellow'
    i+=1    


#sns.set(font_scale=2)
#    sns.set_style("ticks")
sns.set_style("whitegrid")
alto=11
ancho=10
f, ax = plt.subplots(figsize=(16,8))

sns.barplot(x=caracteristica, y='nombre_comuna',data=top10,palette=paleta)

sns.despine(left=True, bottom=True)
#ax.set_xticklabels(top10[caracteristica])
for p in ax.patches:
    ax.annotate(t % p.get_width(), (p.get_x() + p.get_width(), p.get_y() + 1.2),
            xytext=(5, 40), textcoords='offset points')

    
plt.xlabel(titulo)
plt.title("Comunas de Chile - "+titulo + " al 10 de Abril")
plt.ylabel('')
#plt.yticks(rotation=45)
plt.show()

#plt.tight_layout()
    
#plt.savefig('indice_comunas'+caracteristica+'.png')
    
    


#plt.figure(figsize=(12,8))
## plot barh chart with index as x values
#ax = sns.barplot(top10.index, top10.riesgo)
#ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
#ax.set(xlabel="Dim", ylabel='Count')
## add proper Dim values as x labels
#ax.set_xticklabels(top10.nombre_comuna)
#for item in ax.get_xticklabels(): 
#    item.set_rotation(90)
#    for i, v in enumerate(top10["nombre_comuna"].iteritems()):
#        ax.text(i, v[1], "{:,}".format(v[1]), color='m', va ='bottom', rotation=45)
#plt.tight_layout()
#plt.show()






# rm= df[df.Region=='Región Metropolitana de Santiago']
# rm.plot()


# # Control del tamaño de la figura del mapa
# fig, ax = plt.subplots(figsize=(30, 30))
# # Control del título y los ejes
# ax.set_title(u'Comunas del Gran Santiago por Índice de Riesgo de Contagio', 
#              pad = 20, 
#              fontdict={'fontsize':20, 'color': 'black'})
                       
# # Control del título y los ejes
# #ax.set_xlabel('Longitud')
# #ax.set_ylabel('Latitud')
# plt.axis('off')
# #ax.legend(fontsize=1000)
# # Añadir la leyenda separada del mapa
# from mpl_toolkits.axes_grid1 import make_axes_locatable
# divider = make_axes_locatable(ax)
# cax = divider.append_axes("right", size="5%", pad=0.2)
# #map_STGO[(map_STGO.NOMBRE!='Santiago')&(map_STGO.NOMBRE!='Providencia')&(map_STGO.NOMBRE!='Ñuñoa')&(map_STGO.NOMBRE!='Las Condes')] 
# # Mostrar el mapa finalizado
# rm.plot(column='riesgo', 
#         cmap='Reds', ax=ax,
#         legend=True,
#         legend_kwds={'label': "Riesgo de Contagio",},
#         cax=cax, zorder=5,
#         missing_kwds={"color": "lightgrey",
#                       "edgecolor": "black",
#                       "hatch": "///"#,
#                                               #"label": "Missing values",
#                       })








# plt.rcParams['font.size'] = 7


# map_STGO[(map_STGO.NOMBRE!='Santiago')&&(map_STGOOMBRE!='Providencia')&&(map_STGO.NOMBRE!='Nunoa')]






# comunasChile = gp.read_file(shp_path)


#  '''
# comunasChile.columns =  
# Index(['objectid', 'shape_leng', 'dis_elec', 'cir_sena', 'cod_comuna',
#        'codregion', 'st_area_sh', 'st_length_', 'Region', 'Comuna',
#        'Provincia', 'geometry'],
#       dtype='object')
# '''
# ## Necesitamos que las columnas tengan el mismo nombre:
# comunasChile['nombre_comuna']=comunasChile.Comuna
# ############################################################

# df=datosComunas.merge(comunasChile, on='nombre_comuna')






