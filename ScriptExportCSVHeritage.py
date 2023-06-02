import json
import pandas as pd
import datetime

# Ouvrir le fichier UC en mode lecture
with open("Data/BalanceHeritageUC.json", "r") as f:
    # Charger le contenu du fichier en tant qu'objet JSON
    json_data_UC = json.load(f)

# Ouvrir le fichier fonds euro en mode lecture
# with open("BalanceHeritageFdsEuro.json", "r") as f:
    # Charger le contenu du fichier en tant qu'objet JSON
    # json_data_fonds_euro = json.load(f)


BalancePatrimoine = {'ID':[],"Date_last_sync" :[], "Date_extract" : [],"Nom":[], "Type":[] ,"Solde" : []}


# Afficher l'objet JSON UC sous forme de dictionnaire Python
for i in range(len(json_data_UC["result"])):
    
    BalancePatrimoine["ID"].append(json_data_UC["result"][i]["id"])

    BalancePatrimoine["Date_last_sync"].append(json_data_UC["result"][i]["last_sync"])

    BalancePatrimoine["Date_extract"].append(datetime.datetime.now())

    BalancePatrimoine["Nom"].append(json_data_UC["result"][i]["name"])

    BalancePatrimoine["Type"].append("UC")

    BalancePatrimoine["Solde"].append(json_data_UC["result"][i]["balance"])


# Afficher l'objet JSON Fonds Euro sous forme de dictionnaire Python
# for i in range(len(json_data_fonds_euro["result"])):
    
    # BalancePatrimoine["ID"].append(json_data_fonds_euro["result"][i]["account"]["id"])

    # BalancePatrimoine["Date"].append(json_data_fonds_euro["result"][i]["account"]["last_sync"])

    # BalancePatrimoine["Nom"].append(json_data_fonds_euro["result"][i]["account"]["name"])

    # BalancePatrimoine["Type"].append("Fonds Euro")

    # BalancePatrimoine["Solde"].append(json_data_fonds_euro["result"][i]["account"]["balance"])

# Convertir le dictionnaire en DataFrame
df = pd.DataFrame(BalancePatrimoine)

# convertir les colonnes "Dates" en date en utilisant la methode to_datetime()
df['Date_last_sync'] = pd.to_datetime(df['Date_last_sync']).dt.tz_localize(None)
df['Date_extract'] = pd.to_datetime(df['Date_extract']).dt.tz_localize(None)

dfComptes = pd.read_excel('Param/Description_Comptes.xlsx')

# fusionner les deux DataFrame sur la colonne "ID"
dfAgregat = pd.merge(df, dfComptes, on='ID', how='left')

dfGrouped = dfAgregat.groupby('Agregat1').agg(Date_last_sync = ('Date_last_sync', 'first'), Date_extract = ('Date_extract', 'first'), Agregat1_ID = ('Agregat1_ID', 'first'), Organisme =('Organisme', 'first'), Produit =('Produit', 'first'), Solde = ('Solde', 'sum'))

dfGrouped['Week_number'] = dfGrouped['Date_extract'].dt.isocalendar().week

#Concatenation des dataframes
dfConcat = pd.read_csv('Data/Solde_Patrimoine.csv')

dfConcat['Date_last_sync'] = pd.to_datetime(dfConcat['Date_last_sync']).dt.tz_localize(None)
dfConcat['Date_extract'] = pd.to_datetime(dfConcat['Date_extract']).dt.tz_localize(None)

dfConcat = pd.concat([dfConcat, dfGrouped], ignore_index=True, sort=False)


dfConcat.to_csv('Data/Solde_Patrimoine.csv', sep=',', encoding='utf-8', index=False)
dfConcat.to_excel('Data/Solde_Patrimoine.xlsx', sheet_name='Feuille1', index=False)