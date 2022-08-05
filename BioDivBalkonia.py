import pandas as pd
from math import log as ln

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
    elif evenn > 0.8 and 1.5 < sdi <= 2:
        print("Dein Balkon eine gute Biodiversität.")
    elif evenn < 0.8 and sdi > 1.5:
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

#Zeile mit Summe je Spalte hinzufügen oder Summe score_biene berechnen.
Total = user_plants_df['score_biene'].sum()/user_df['anzahl'].sum()*100

print("Anzahl bienenfreundliche Pflanzen: ",user_plants_df['score_biene'].sum())
print("Anzahl Pflanzen gesamt: ", user_df['anzahl'].sum())
print("Dein Bienenscore ist =",Total,"%.")


#Feedback zu Bienenscore.
if Total > 85:
    print("Das ist super! Glückwunsch :-)")
else:
    print("Du solltest mehr bienenfreundliche Pflanzen pflanzen. Zum Beispiel:")
if Total <= 85:
    subset_bee_df = pd.merge(plants_df.loc[plants_df['biene'] == 1], user_df, on=['name'], how='outer')
    #Empfehlung, falls Bienenscore <=85%:
    print(subset_bee_df.name.sample(5))


##Dataframe über Monat, Blüte und bienenfreundliche Blüte:
month = ['jan', 'feb', 'mrz', 'apr', 'mai', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dez']
blossom = list(map(lambda month: user_plants_df[month].sum(), month))
subset_user_plants_df=user_plants_df.loc[user_plants_df['biene'] == 1]
blossom_bee = list(map(lambda month: subset_user_plants_df[month].sum(), month))
blossom_month_df = pd.DataFrame({'monat': month, 'blüte': blossom, 'blüte_biene': blossom_bee})

#Visualisierung der Anzahl blühender Pflanzenarten sowie bienenfreundlicher blühenden Pflanzenarten je Monat
ax_blossom = blossom_month_df.plot.bar(x='monat', rot=0)


#Hinweis, in welchen Monaten Blüte für Bienen fehlt.
no_blossom_bee = blossom_month_df.loc[blossom_month_df['blüte_biene'] == 0]

from functools import reduce
months = reduce(lambda a, b: a + ', ' + b, no_blossom_bee['monat'].tolist())

if months == 'jan, dez':
    print("Super!")
else:
    print("In den folgenden Monaten blüht keine Pflanze:", months)
    print("Du solltest beim nächsten Pflanzenkauf darauf achten eine bienenfreundliche Pflanzenart zu wählen, die in diesen Monaten blüht.")