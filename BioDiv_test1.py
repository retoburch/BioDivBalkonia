reference = ["Rose", "Mimose", "Feilchen"]

n = int(input("Wie viele Pflanzen haben Sie insgesamt?: "))
pflanze = []
pflanze_anzahl = []

for i in range(n):
   ad = input("Name der Pflanze: ")
   nm = int(input("Anzahl: "))
   pflanze.append(ad)
   pflanze_anzahl.append(nm)

def score_flower(new_input):
   score = 0
   for x in new_input:
      if x in reference:
         score += 1
   rel_score = 100 / len(pflanze) * score
   return (rel_score)

print("Dein Score ist " + str(score_flower(pflanze)) + "%")

def pos_neg_pflanze(user_input):
   positiv_list = []
   negativ_list = []
   for x in user_input:
      if x in reference:
         positiv_list.append(x)
   for y in user_input:
      if y not in reference:
         negativ_list.append(y)

   print("Diese Pflanzen fördern die BioDiv " + str(positiv_list))
   print("Diese Pflanzen bringen nix " + str(negativ_list))

pos_neg_pflanze(pflanze)