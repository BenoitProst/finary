import json
import pandas as pd
import datetime

from pyxirr import xirr

# Création du dataframe pour calcul de la rentabilité

## Production fichier solde ouverture
TimeOuverture = datetime.date(2023, 1, 1)

dfOuverture = pd.read_excel('Data/Ouverture_Patrimoine.xlsx')

dfYDTOuverture = dfOuverture[pd.to_datetime(dfOuverture['Date']).dt.date == TimeOuverture].drop_duplicates(subset='Agregat1_ID', keep="first")

### Préparation du fichier dataframe pour concatenation
dfYDTOuverture['Solde'] = dfYDTOuverture['Solde'] * -1
dfYDTOuverture['Type'] = "Ouverture"



## Production fichier solde YDT

dfSolde = pd.read_csv('Data/Solde_Patrimoine.csv')

dfSolde['Date_last_sync'] = pd.to_datetime(dfSolde['Date_last_sync']).dt.tz_localize(None)
dfSolde['Date_extract'] = pd.to_datetime(dfSolde['Date_extract']).dt.tz_localize(None)

### get all differences with date as values

TimeYDT = datetime.datetime(1900, 1, 1)

for i in dfSolde['Date_extract']:
        if (i - datetime.datetime.now()) > (TimeYDT - datetime.datetime.now()):
            TimeYDT = i


dfYDTSolde = dfSolde[pd.to_datetime(dfSolde['Date_extract']).dt.date == TimeYDT.date()].drop_duplicates(subset='Agregat1_ID', keep="first")

### Préparation du fichier dataframe pour concatenation

dfYDTSolde["Type"] = "Solde"
dfYDTSolde.rename(columns = {'Date_extract':'Date'}, inplace = True)
dfYDTSolde = dfYDTSolde.drop(columns=['Date_last_sync'])


## Production fichier mouvement YDT
dfMouvement = pd.read_excel('Data/Mouvement_Patrimoine.xlsx')


dfMouvementYDT = dfMouvement[(pd.to_datetime(dfMouvement['Date']).dt.date >= TimeOuverture) & (pd.to_datetime(dfMouvement['Date']).dt.date <= TimeYDT.date())]

### Préparation du fichier dataframe pour concatenation
dfMouvementYDT["Solde"] = dfMouvementYDT["Solde"] * -1
dfMouvementYDT["Type"] = "Mouvement"
dfMouvementYDT["Agregat1_ID"] = dfMouvementYDT["Agregat1_ID"].astype(str)

## Concatenation des 3 dataframes
dfXirrYdt = pd.concat([dfYDTOuverture, dfMouvementYDT, dfYDTSolde])

# Création du dataframe pour calcul de la rentabilité

TRI_Patrimoine = {'Agregat1_ID':[], "Date" : [],"Organisme":[], "Produit":[] ,"TRI YTD" : [],"Rendement" :[], "Solde":[], "Total Mouvements":[]}


for i in dfXirrYdt[['Agregat1_ID']].drop_duplicates(keep = 'first')['Agregat1_ID']:
    TRI_Patrimoine['Agregat1_ID'].append(i)
    
    TRI_Patrimoine['Date'].append(TimeYDT)
    
    for j in dfXirrYdt[dfXirrYdt['Agregat1_ID'] == i][['Organisme']].drop_duplicates(keep = 'first')['Organisme']:
        TRI_Patrimoine['Organisme'].append(j)
 
    for k in dfXirrYdt[dfXirrYdt['Agregat1_ID'] == i][['Produit']].drop_duplicates(keep = 'first')['Produit']:
        TRI_Patrimoine['Produit'].append(k)
    
    TRI_Patrimoine['TRI YTD'].append(xirr(dfXirrYdt[dfXirrYdt['Agregat1_ID'] == i][['Date','Solde']]))
    
    TRI_Patrimoine['Rendement'].append(dfXirrYdt[dfXirrYdt['Agregat1_ID'] == i]['Solde'].sum())
    
    TRI_Patrimoine['Solde'].append(dfXirrYdt[(dfXirrYdt['Agregat1_ID'] == i) & (dfXirrYdt['Type'] == "Solde")]["Solde"].sum())
    
    TRI_Patrimoine['Total Mouvements'].append(dfXirrYdt[(dfXirrYdt['Agregat1_ID'] == i) & (dfXirrYdt['Type'] == "Mouvement")]["Solde"].sum() * -1)
    
TRI_Patrimoine['Agregat1_ID'].append("0.0")   
TRI_Patrimoine['Date'].append(TimeYDT)
TRI_Patrimoine['Organisme'].append("Total")
TRI_Patrimoine['Produit'].append(" - ")
TRI_Patrimoine['TRI YTD'].append(xirr(dfXirrYdt[['Date','Solde']]))
TRI_Patrimoine['Rendement'].append(dfXirrYdt['Solde'].sum())
TRI_Patrimoine['Solde'].append(dfXirrYdt[(dfXirrYdt['Type'] == "Solde")]["Solde"].sum())
TRI_Patrimoine['Total Mouvements'].append(dfXirrYdt[(dfXirrYdt['Type'] == "Mouvement")]["Solde"].sum() * -1)

dfResultatXirrYDT = pd.DataFrame(TRI_Patrimoine)

dfResultatXirrYDT.to_excel('Data/TRI_Ydt.xlsx', sheet_name='TRI YDT', index=False)

