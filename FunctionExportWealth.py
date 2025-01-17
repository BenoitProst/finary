import json
import pandas as pd
import datetime
import subprocess


def ExportCSVWealth(dfComptes):

    subprocess.run(["./ScriptExportCSVWealth.sh"])
    

    # Ouvrir le fichier UC en mode lecture
    with open("Data/BalanceHeritageUC.json", "r") as f:
        # Charger le contenu du fichier en tant qu'objet JSON
        json_data_UC = json.load(f)

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


# Définition de la fonctionalité export détaillé
def ExportCSVWealthDetailled(dfComptes):

    #Quand test concluant, enlever le v2
    subprocess.run(["./ScriptExportCSVWealthDetailledv2.sh"])

    Date_Extract = datetime.datetime.now()

    # Construction partie UC

    ## Ouvrir le fichier détaillé en mode lecture
    with open("Data/BalanceWealthDetailled.json", "r") as f:
        # Charger le contenu du fichier en tant qu'objet JSON
        json_data_detailled = json.load(f)


    BalancePatrimoine_detailled = {'ID':[], "Date_last_sync" :[], "Date_extract" : [], "Actif" : [], "ISIN" : [], "Type" : [],"Montant Solde" : [], "Quantité" : [], "Prix unitaire" : []}

    for l in range(len(json_data_detailled['result']['accounts'])):

        for i in range(len(json_data_detailled['result']['accounts'][l]["securities"])):
            
            BalancePatrimoine_detailled["ID"].append(json_data_detailled['result']['accounts'][l]['id'])
            
            BalancePatrimoine_detailled["Date_last_sync"].append(json_data_detailled['result']['accounts'][l]['last_sync'])

            BalancePatrimoine_detailled["Date_extract"].append(Date_Extract)
            
            BalancePatrimoine_detailled["Actif"].append(json_data_detailled['result']['accounts'][l]["securities"][i]['security']["name"])
            
            BalancePatrimoine_detailled["ISIN"].append(json_data_detailled['result']['accounts'][l]["securities"][i]['security']["isin"])
            
            BalancePatrimoine_detailled["Type"].append("UC")
            
            BalancePatrimoine_detailled["Prix unitaire"].append(json_data_detailled['result']['accounts'][l]["securities"][i]['security']["current_price"])
            
            BalancePatrimoine_detailled["Quantité"].append(json_data_detailled['result']['accounts'][l]["securities"][i]['quantity'])
            
            BalancePatrimoine_detailled["Montant Solde"].append(json_data_detailled['result']['accounts'][l]["securities"][i]['current_value'])
            

    df_brut = pd.DataFrame(BalancePatrimoine_detailled)

    # convertir les colonnes "Dates" en date en utilisant la methode to_datetime()
    df_brut['Date_last_sync'] = pd.to_datetime(df_brut['Date_last_sync']).dt.tz_localize(None)
    df_brut['Date_extract'] = pd.to_datetime(df_brut['Date_extract']).dt.tz_localize(None)

    # fusionner les deux DataFrame sur la colonne "ID"
    dfAgregat = pd.merge(df_brut, dfComptes, on='ID', how='left')

    #Aggrégation
    dfGroupedUC = dfAgregat.groupby(['Agregat1_ID' , 'Actif']).agg(Date_last_sync = ('Date_last_sync', 'first'), Date_extract = ('Date_extract', 'first'), Agregat1_ID = ('Agregat1_ID', 'first'), Organisme =('Organisme', 'first'), Produit =('Produit', 'first'), ISIN = ('ISIN', 'first'), Actif = ('Actif', 'first'), Type =  ('Type', 'first'), Prix_unitaire = ('Prix unitaire', 'first'), Quantité = ('Quantité', 'first'), Montant_Solde = ('Montant Solde', 'sum'))

    #Rajout numéro de semaine
    dfGroupedUC['Week_number'] = dfGroupedUC['Date_extract'].dt.isocalendar().week

    # Construction partie fonds euros


    ## Ouvrir le fichier détaillé en mode lecture
    with open("Data/BalanceWealthFondsEuros.json", "r") as f:
        # Charger le contenu du fichier en tant qu'objet JSON
        json_data_FondsEuros = json.load(f)
        

    BalancePatrimoine_FondsEuros = {'ID':[], "Date_last_sync" :[], "Date_extract" : [], "Actif" : [], "ISIN" : [], "Type" : [],"Montant Solde" : [], "Quantité" : [], "Prix unitaire" : []}

    for l in range(len(json_data_FondsEuros['result'])):
        
        BalancePatrimoine_FondsEuros["ID"].append(json_data_FondsEuros['result'][l]['bank_account']['id'])
        
        BalancePatrimoine_FondsEuros["Date_last_sync"].append(json_data_FondsEuros['result'][l]['bank_account']['last_sync'])
        
        BalancePatrimoine_FondsEuros["Date_extract"].append(Date_Extract)
        
        BalancePatrimoine_FondsEuros["Actif"].append(json_data_FondsEuros['result'][l]['bank_account']['name'])
        
        BalancePatrimoine_FondsEuros["ISIN"].append("")
        
        BalancePatrimoine_FondsEuros["Type"].append("Fonds Euros")
        
        BalancePatrimoine_FondsEuros["Montant Solde"].append(json_data_FondsEuros['result'][l]['current_value'])

        BalancePatrimoine_FondsEuros["Quantité"].append("")
            
        BalancePatrimoine_FondsEuros["Prix unitaire"].append("")    
            
    df_brut = pd.DataFrame(BalancePatrimoine_FondsEuros)

    # convertir les colonnes "Dates" en date en utilisant la methode to_datetime()
    df_brut['Date_last_sync'] = pd.to_datetime(df_brut['Date_last_sync']).dt.tz_localize(None)
    df_brut['Date_extract'] = pd.to_datetime(df_brut['Date_extract']).dt.tz_localize(None)

    # fusionner les deux DataFrame sur la colonne "ID"
    dfAgregat = pd.merge(df_brut, dfComptes, on='ID', how='left')

    dfAgregat = dfAgregat.dropna(subset=['Agregat1_ID'])

    #Aggrégation
    dfGroupedFondsEuros = dfAgregat.groupby(['Agregat1_ID' , 'Actif']).agg(Date_last_sync = ('Date_last_sync', 'first'), Date_extract = ('Date_extract', 'first'), Agregat1_ID = ('Agregat1_ID', 'first'), Organisme =('Organisme', 'first'), Produit =('Produit', 'first'), ISIN = ('ISIN', 'first'), Actif = ('Actif', 'first'), Type =  ('Type', 'first'), Prix_unitaire = ('Prix unitaire', 'first'), Quantité = ('Quantité', 'first'), Montant_Solde = ('Montant Solde', 'sum'))

    #Rajout numéro de semaine
    dfGroupedFondsEuros['Week_number'] = dfGroupedFondsEuros['Date_extract'].dt.isocalendar().week

    dfGrouped = pd.concat([dfGroupedUC, dfGroupedFondsEuros])


    # append data frame to CSV file
    dfGrouped.to_csv('Data/SoldeDetailled_Patrimoine.csv', mode='a', index=False, header=False)

    # Update Excel Solde File
    dfExcel = pd.read_csv('Data/SoldeDetailled_Patrimoine.csv')

    dfExcel['Date_last_sync'] = pd.to_datetime(dfExcel['Date_last_sync']).dt.tz_localize(None)
    dfExcel['Date_extract'] = pd.to_datetime(dfExcel['Date_extract']).dt.tz_localize(None)

    dfExcel.to_excel('Data/SoldeDetailled_Patrimoine.xlsx', sheet_name='Feuille1', index=False)

