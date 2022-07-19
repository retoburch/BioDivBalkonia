import pandas as pd
from math import log as ln

#Import der Daten
plantfacts_df = pd.read_csv('/Users/burchr/Documents/GitHub/pruefungsleistung/Import/DatenBalkonien.csv',sep=",")

# alle Blumennamen klein geschrieben
plantfacts_df["Name"] = plantfacts_df["Name"].str.lower()

#Kopie des dataframes und Aussortieren der Attribute, die nicht weiter verwendet werden
plants_df = plantfacts_df.copy()
plants_df.drop(plants_df.columns[[5,6,7,8,9,10,11,12,13,26]], axis = 1, inplace = True)
plants_df.drop_duplicates(subset=['Name'], keep='first', inplace=True, ignore_index=True)
plants_df = plants_df.rename(columns={"botanischer Name": "botanischer_Name"})
plants_df = plants_df.rename(str.lower, axis='columns')

def user_input():
    n = int(input("Wie viele Pflanzenarten haben Sie insgesamt?: "))
    pflanze = []
    pflanze_anzahl = []

    for i in range(n):
        ad = input("Name der Pflanzenart: ")
        nm = int(input("Anzahl: "))
        ad_l = ad.lower()
        pflanze.append(ad_l)
        pflanze_anzahl.append(nm)

    list_user = {"name": pflanze, "anzahl": pflanze_anzahl}
    user_df = pd.DataFrame(list_user)
    return user_df

user_df = user_input()

def shannon_index(user_input):
    def p(n, N):
        return (float(n) / N) * ln(float(n) / N)
    N = user_input.anzahl.sum()
    sdi = -sum(p(n, N) for n in user_input.anzahl if n != 0)
    evern = sdi / ln(user_input.name.count())

    if evern > 0.5:
        print("Dein Balkon hat eine guten BioDiv")
    else:
        print("Dein Balkon hat einen niedrigen BioDiv")

shannon_index(user_df)

#neues Dataframe mit allen Spalten aus plants_df zu Usereingabe erstellen
user_plants_df = pd.merge(plants_df, user_df, on=['name'], how='right')
#Spalte mit Score für für Bienen wertvolle Pflanzen
user_plants_df = user_plants_df.assign(score_biene=user_plants_df['biene']*user_plants_df['anzahl'])
print(user_plants_df)

#Zeile mit Summe je Spalte hinzufügen oder Summe score_biene berechnen (merge mit right kann user_plants_df stehen. Bei Merge "inner" braucht es die user_df Anzahl
Total = user_plants_df['score_biene'].sum()/user_df['anzahl'].sum()*100
print("Dein Bienenscore ist =",Total,"%.")