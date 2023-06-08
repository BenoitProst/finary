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



# append data frame to CSV file
dfGrouped.to_csv('Data/Solde_Patrimoine.csv', mode='a', index=False, header=False)

# Update Excel Solde File
dfExcel = pd.read_csv('Data/Solde_Patrimoine.csv')

dfExcel['Date_last_sync'] = pd.to_datetime(dfExcel['Date_last_sync']).dt.tz_localize(None)
dfExcel['Date_extract'] = pd.to_datetime(dfExcel['Date_extract']).dt.tz_localize(None)

dfExcel.to_excel('Data/Solde_Patrimoine.xlsx', sheet_name='Feuille1', index=False)