import pandas as pd
from math import log as ln

reference = ["Rose", "Mimose", "Feilchen"]

n = int(input("Wie viele Pflanzen haben Sie insgesamt?: "))
pflanze = []
pflanze_anzahl = []

for i in range(n):
   ad = input("Name der Pflanze: ")
   nm = int(input("Anzahl: "))
   pflanze.append(ad)
   pflanze_anzahl.append(nm)

list_user = {"Pflanzen": pflanze, "Anzahl": pflanze_anzahl}
frame_user = pd.DataFrame(list_user)

def simpson_index(user_input):
   total_count = user_input.Anzahl.sum()
   pflanzen_count = user_input.Pflanzen.count()
   prop = [Anzahl / total_count for Anzahl in user_input.Anzahl]
   user_input["prop"] = prop
   user_input["prop2"] = user_input["prop"] ** 2
   D = 1 - user_input['prop2'].sum()
   print("Der Simpson's diversity index is {:.4f}".format(D))

simpson_index(frame_user)


def shannon_index(user_input):
   def p(n, N):
      if n == 0:
         return 0
      else:
         return (float(n) / N) * ln(float(n) / N)
   N = user_input.Anzahl.sum()
   return -sum(p(n, N) for n in user_input.Anzahl if n != 0)

print("Der Shannon-Index ist " + str(shannon_index(frame_user)))


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