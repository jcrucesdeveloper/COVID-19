#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 10:56:18 2020

@author: esteban
"""

import pandas as pd
##Primero Cargamos los Datos de tests PCR del repositorio del MinCultura
path='../../fuentes/MinCiencias/output/producto7/PCR_T.csv'

df1=pd.read_csv(path)
df=df1[df1.index>2].reset_index(drop=True).rename(columns={'Region':'fecha'})
df=pd.melt(df,id_vars='fecha',value_vars=list(df.columns[1:]),var_name='nombre_region', value_name='pcr_numero')
df['id_region']=0

df.loc[df.nombre_region=='Arica y Parinacota','id_region']=15
df.loc[df.nombre_region=='Tarapacá','id_region']=1
df.loc[df.nombre_region=='Antofagasta','id_region']=2
df.loc[df.nombre_region=='Atacama','id_region']=3
df.loc[df.nombre_region=='Coquimbo','id_region']=4
df.loc[df.nombre_region=='Valparaiso','id_region']=5
df.loc[df.nombre_region=='Metropolitana','id_region']=13
df.loc[df.nombre_region=='O’Higgins','id_region']=6
df.loc[df.nombre_region=='Maule','id_region']=7
df.loc[df.nombre_region=='Ñuble','id_region']=16
df.loc[df.nombre_region=='Biobío','id_region']=8
df.loc[df.nombre_region=='Araucanía','id_region']=9
df.loc[df.nombre_region=='Los Ríos','id_region']=14
df.loc[df.nombre_region=='Los Lagos','id_region']=10
df.loc[df.nombre_region=='Aysén','id_region']=11
df.loc[df.nombre_region=='Magallanes','id_region']=12


pobla=df1[df1.index==1].reset_index(drop=True).rename(columns={'Region':'poblacion'})
pobla=pd.melt(pobla,id_vars='poblacion',value_vars=list(pobla.columns[1:]),var_name='nombre_region', value_name='pobla')
pobla=pobla[['nombre_region','pobla']]

df=df.merge(pobla, on='nombre_region')


df.pcr_numero=df.pcr_numero.replace('-',0)
df=df.fillna(0)
df.pcr_numero=df.pcr_numero.astype(int)
df.pobla=df.pobla.astype(int)



df['tasa_testeo']=df.pcr_numero/(df.pobla/10**6)

pcrsum=df.groupby('nombre_region').sum().reset_index()

pcrsum.loc[pcrsum.nombre_region=='Arica y Parinacota','id_region']=15
pcrsum.loc[pcrsum.nombre_region=='Tarapacá','id_region']=1
pcrsum.loc[pcrsum.nombre_region=='Antofagasta','id_region']=2
pcrsum.loc[pcrsum.nombre_region=='Atacama','id_region']=3
pcrsum.loc[pcrsum.nombre_region=='Coquimbo','id_region']=4
pcrsum.loc[pcrsum.nombre_region=='Valparaiso','id_region']=5
pcrsum.loc[pcrsum.nombre_region=='Metropolitana','id_region']=13
pcrsum.loc[pcrsum.nombre_region=='O’Higgins','id_region']=6
pcrsum.loc[pcrsum.nombre_region=='Maule','id_region']=7
pcrsum.loc[pcrsum.nombre_region=='Ñuble','id_region']=16
pcrsum.loc[pcrsum.nombre_region=='Biobío','id_region']=8
pcrsum.loc[pcrsum.nombre_region=='Araucanía','id_region']=9
pcrsum.loc[pcrsum.nombre_region=='Los Ríos','id_region']=14
pcrsum.loc[pcrsum.nombre_region=='Los Lagos','id_region']=10
pcrsum.loc[pcrsum.nombre_region=='Aysén','id_region']=11
pcrsum.loc[pcrsum.nombre_region=='Magallanes','id_region']=12






############################################################
# Datos confirmados por region
path='../../COVID19_Chile_Regiones-casos_totales.CSV'
casos=pd.read_csv(path)

casos=casos[['nombre_reg','2020-04-23','id_reg']]
casos=casos.rename(columns={'nombre_reg':'nombre_region','2020-04-23':'casos_totales','id_reg':'id_region'})


data=pcrsum.merge(casos, on='id_region')

data['tasa_casos']=data.casos_totales/(data.pobla/10**6)

###############################################################

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
fig, ax = plt.subplots()
g =sns.scatterplot(x="tasa_testeo", y="tasa_casos",
                   hue='nombre_region_y',
                   size='casos_totales',
                   sizes=(100, 700),
                   data=data[data.id_region!=12],ax=ax);
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#ax.set_xlim(0,0.010)
plt.show()