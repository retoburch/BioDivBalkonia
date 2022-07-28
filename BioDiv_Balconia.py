import pandas as pd
from math import log as ln
from functools import reduce
import matplotlib.pyplot as plt

#Import der Daten als Dataframe
plantfacts_df = pd.read_csv('./Import/DatenBalkonien.csv',sep=",")

#Kopie des Dataframes und Aussortieren der Attribute (Spalten), die nicht weiter verwendet werden.
plants_df = plantfacts_df.copy()
plants_df. drop(plants_df.columns[[1,4,5,6,7,8,9,10,11,12,13,26]],
                    axis = 1,
                    inplace = True)

#Löschen von Duplikaten in der Spalte 'Namen' aus dem Dataframe, da dieser für den Abgleich mit der Usereingabe benötigt wird:
plants_df.drop_duplicates(subset=['Name'], keep='first', inplace=True, ignore_index=True)

#Spaltenbezeichnungen: Lowercase und _ statt Leerzeichen.
plants_df = plants_df.rename(str.lower, axis='columns')

#Pflanzennamen: Lowercase.
plants_df['name'] = plants_df['name'].str.lower()
plants_df['kategorie'] = plants_df['kategorie'].str.lower()
plants_df.head()

#Ausgeben als csv file.
plants_df.to_csv('./Import/plants_df.csv', index=False)

#User Eingabe
# Check, ob die eingebenen Pflanzenart im Dataframe der Pflanzen überhaupt vorhanden ist
# sowie ebefalls, ob die Pflanzenart bereits eingegeben wurde
def input_plant_name(plant):
    ad = input("Name der Pflanzenart: ")

    # check 1: in Liste?
    if ad.lower() not in plants_df["name"].tolist():
        print("Pflanzenart ist nicht bekannt. Bitte erneut eingeben.")
        ad = input_plant_name(plant)

    # check 2: Eingabe bereits erfolgt
    if ad.lower() in plant:
        print("Du hast diese Pflanzenart bereits eingegeben. Bitte eine andere Art eingeben.")
        ad = input_plant_name(plant)
    return ad

# Check, ob die eingegeben Anzahl von Pflanzen ein Integer ist
def check_plant_number(input):
    try:
        # Convert it into integer
        val = int(input)
        return val
    except ValueError:
        print("Anzahl ist keine Zahl. Bitte erneut eingeben.")
        return input_plant_number()
    return val


def input_plant_number():
    return check_plant_number(input("Anzahl: "))

# Schleife für die Eingabe der Pflanzenarten und deren Namen sowie Anzahl
def user_input():
    n = int(input("Wie viele Pflanzenarten haben Sie insgesamt?: "))
    plant = []
    plant_number = []
    for i in range(n):
        ad = input_plant_name(plant)
        nm = input_plant_number()
        ad_l = ad.lower()
        plant.append(ad_l)
        plant_number.append(nm)
    list_user = {"name": plant, "anzahl": plant_number}
    user_df = pd.DataFrame(list_user)
    return user_df

user_df = user_input()

#Diversitätsberechnung
def shannon_index(user_input):
    def p(n, N):
        return (float(n) / N) * ln(float(n) / N)

    N = user_input.anzahl.sum()

    sdi = -sum(p(n, N) for n in user_input.anzahl if n != 0)

    # Diversitätswert in Relation zu dem maximal möglichen Diversitätswert
    evenn = sdi / ln(user_input.name.count())

    print("Dein Shannon-Index (H) ist:", round(sdi, 4))
    print("Die Evenness (w) beträgt:", round(evenn, 4))

    if evenn > 0.8 and sdi > 2:
        print("Dein Balkon ist ausgeglichen bepflanzt und hat eine sehr gute Biodiversität")
    elif evenn > 0.8 and sdi > 1.5:
        print("Dein Balkon eine gute Biodiversität. Der geringere Evenness (w) kann darauf hindeuten, dass eine oder wenige Pflanzenarten verhältnismäßig oft vorkommen.")
    elif evenn > 0.8 and sdi <= 1.0:
        print("Dein Balkon ist ausgeglichen bepflanzt, hat jedoch eine geringe Biodiversität.")
    else:
        print(
            "Dein Balkon hat eine geringe Biodiversität. Es scheint, dass eine oder wenige Pflanzenarten verhältnissmässig oft vorkommen.")


shannon_index(user_df)


#neues Dataframe mit allen Spalten aus plants_df zu Usereingabe erstellen.
user_plants_df = pd.merge(plants_df, user_df, on=['name'], how='inner')

#Spalte mit Score für für Bienen wertvolle Pflanzen.
user_plants_df = user_plants_df.assign(score_biene=user_plants_df['biene']*user_plants_df['anzahl'])
user_plants_df

#Zeile mit Summe je Spalte hinzufügen oder Summe score_biene berechnen.
Total = user_plants_df['score_biene'].sum()/user_df['anzahl'].sum()*100

print("Anzahl bienenfreundliche Pflanzen: ",user_plants_df['score_biene'].sum())
print("Anzahl Pflanzen gesamt: ", user_df['anzahl'].sum())
print("Dein Bienenscore ist =",Total,"%.")

#Feedback zu Bienenscore:
if Total > 85:
    print("Das ist super! Glückwunsch :-)")
else:
    print("Du solltest mehr bienenfreundliche Pflanzen pflanzen. Zum Beispiel:")
if Total <= 85:
    subset_biene_df = plants_df.loc[plants_df['biene'] == 1]
    #Empfehlung, falls Bienenscore <=85%:
    print(subset_biene_df.name.sample(5))

#Dataframe über Monat, Blüte und bienenfreundliche Blüte:
monat = ['jan', 'feb', 'mrz', 'apr', 'mai', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dez']
blüte = list(map(lambda monat: user_plants_df[monat].sum(), monat))
subset_user_plants_df=user_plants_df.loc[user_plants_df['biene'] == 1]
blüte_biene = list(map(lambda monat: subset_user_plants_df[monat].sum(), monat))

blüte_anz_monat_df = pd.DataFrame({'monat': monat, 'blüte': blüte, 'blüte_biene': blüte_biene})

#Visualisierung der Anzahl blühender Pflanzenarten sowie bienenfreundlicher blühenden Pflanzenarten je Monat
ax_blüte = blüte_anz_monat_df.plot.bar(x='monat', rot=0)

#Hinweis, in welchen Monaten Blüte für Bienen fehlt.
keine_blüte_biene = blüte_anz_monat_df.loc[blüte_anz_monat_df['blüte_biene'] == 0]


monate = reduce(lambda a, b: a + ', ' + b, keine_blüte_biene['monat'].tolist())

if monate == 'jan, dez':
    print("Super!")
else:
    print("In den folgenden Monaten blüht keine Pflanze:", monate)
    print("Du solltest beim nächsten Pflanzenkauf darauf achten Pflanzen zu wählen, die bienenfreundlich sind und in diesen Monaten blühen.")
