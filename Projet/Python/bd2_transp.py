# -*- coding: utf-8 -*-
"""BD2-transp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jCUPWss7PBXMjGrz-4Aa2XQKhm2qYrhT
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def concordance_partiel_1(H, b, j, critere):
  H=new_data[new_data['productname']==H]
  b=profil[profil['profil']==b]
  c=0
  if critere == 'max':
    if H.iloc[0][j] >= b.iloc[0][j]:
      c=1
      return c
    else :
      return c
  if critere == 'min':
      if b.iloc[0][j] >= H.iloc[0][j]:
        c =1 
        return c
      else :
        return c
  return

def concordance_partiel_2(b, H, j, critere):
  H=new_data[new_data['productname']==H]
  b=profil[profil['profil']==b]
  c=0
  if critere == 'min':
    if H.iloc[0][j] >= b.iloc[0][j]:
      c=1
      return c
    else :
      return c
  if critere == 'max':
      if b.iloc[0][j] >= H.iloc[0][j]:
        c =1 
        return c
      else :
        return c
  return

def concondance_global_1(H_in, b_in, critere):
  H=new_data[new_data['productname']==H_in]
  b=profil[profil['profil']==b_in]
  num=0
  den=0
  for i in range(1,len(H.columns)):
    num += poids.iloc[0][i-1]*concordance_partiel_1(H_in, b_in, i, critere[i-1])
    den += poids.iloc[0][i-1]
  return num/den

def concondance_global_2(b_in, H_in, critere):
  H=new_data[new_data['productname']==H_in]
  b=profil[profil['profil']==b_in]
  num=0
  den=0
  for i in range(1,len(H.columns)):
    num += poids.iloc[0][i-1]*concordance_partiel_2(b_in, H_in, i, critere[i-1])
    den += poids.iloc[0][i-1]
  return num/den

def surclassament_1(H_in, b_in, lamb, critere):
    if concondance_global_1(H_in, b_in, critere) >= lamb:
      #print(str(H_in)+" S "+str(b_in)) 
      return 1
    else:
      #print(str(H_in)+" ne surclasse pas "+str(b_in))
      return
    return

def surclassament_2(b_in, H_in, lamb, critere):
    if concondance_global_2(b_in, H_in, critere) >= lamb:
      #print(str(b_in)+" S "+str(H_in)) 
      return 1
    else:
      #print(str(b_in)+" ne surclasse pas "+str(H_in)) 
      return 0
    return

def pessimiste(H_in, lamb, critere):
    for i in range(len(profil)):
      b_in= profil.iloc[i][0]
      if surclassament_1(H_in, b_in, lamb, critere) == 1:
        #print("cat:", nutri_cat[i-1])
        break
    return nutri_cat[i-1]

def optimiste(H_in, lamb, critere):
    for i in range(len(profil)-1,-0,-1):
        b_in= profil.iloc[i][0]
        if surclassament_2(b_in, H_in, lamb, critere) == 1 and i==len(profil)-1:
          return nutri_cat[len(profil)-2]
        if surclassament_2(b_in, H_in, lamb, critere) == 1:
        #print("cat:", nutri_cat[i])
            break
    return nutri_cat[i]

nutri_cat=['a','b','c','d']

notre_data = pd.read_excel("data1000.xlsx")

new_data= notre_data[["productname",'energy100g', 'saturatedfat100g', 'sugars100g','fiber100g','proteins100g','sodium100g']]

new_data

poids = pd.read_csv("notre_poids.csv")
profil = pd.read_csv("profil_up.csv")

profil

pessimiste("Galettes De MaÃ¯s", 0.5, ['max','min','min','min','max','max'])

optimiste("Galettes De MaÃ¯s", 0.5, ['max','min','min','min','max','max'])

bd2=new_data.copy()
bd2["pessimiste_05"]=1

for i in range(len(bd2)):
    bd2["pessimiste_05"][i] = pessimiste(new_data.iloc[i]["productname"], 0.5, ['max','min','min','min','max','max'])

bd2["pessimiste_06"]=1

for i in range(len(bd2)):
    bd2["pessimiste_06"][i] = pessimiste(new_data.iloc[i]["productname"], 0.6, ['max','min','min','min','max','max'])

bd2["pessimiste_07"]=1

for i in range(len(bd2)):
    bd2["pessimiste_07"][i] = pessimiste(new_data.iloc[i]["productname"], 0.7, ['max','min','min','min','max','max'])

bd2["optimiste_05"]=1

for i in range(len(bd2)):
    #print(i)
    bd2["optimiste_05"][i] = optimiste(new_data.iloc[i]["productname"], 0.5, ['max','min','min','min','max','max'])

bd2["optimiste_06"]=1

for i in range(len(bd2)):
    #print(i)
    bd2["optimiste_06"][i] = optimiste(new_data.iloc[i]["productname"], 0.6, ['max','min','min','min','max','max'])

bd2["optimiste_07"]=1

for i in range(len(bd2)):
    #print(i)
    bd2["optimiste_07"][i] = optimiste(new_data.iloc[i]["productname"], 0.7, ['max','min','min','min','max','max'])

bd2["nutriscoregrade"]=notre_data["nutritiongradefr"]

bd2["nova_group"] = notre_data["nova_group"]

bd2

from openpyxl.workbook import Workbook
bd2.to_excel("bd2.xlsx",
             sheet_name='lambda')

notre_data = pd.read_excel("data1000.xlsx")

notre_data

notre_data = notre_data.drop(['Unnamed: 13'], axis=1)

notre_data

bd2 = pd.read_excel("bd2.xlsx")

bd2

lista = ["pessimiste_05",	"pessimiste_06",	"pessimiste_07",	"optimiste_05",	"optimiste_06",	"optimiste_07"]

for el in lista:
  notre_data[el] = bd2[el]

notre_data

from openpyxl.workbook import Workbook
notre_data.to_excel("bd2_elec.xlsx",
             sheet_name='lambda')

