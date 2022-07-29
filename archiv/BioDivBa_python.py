user_input = ["Rose", "Mimose", "Topfpflanze"]
reference = ["Rose", "Mimose", "Feilchen"]

# Methode 1: nested for loop
score = 0
positiv_list = []
negativ_list = []
for x in user_input:
    if x in reference:
        positiv_list.append(x)
        score += 1
for y in user_input:
    if y not in reference:
        negativ_list.append(y)

print(positiv_list)
print(negativ_list)
print(score)

# Method 2: List Comprehension gibt gleich wieder eine Liste aus. Funktioniert nicht für count
result = [x for x in user_input if x in set(reference)]
score = 0
print(result)

# set() Funktion ist scheinbar viel schneller


user_input = ["Rose", "Mimose", "Topfpflanze"]


def comp_flower(new_input):
    reference = ["Rose", "Mimose", "Feilchen"]
    positiv_list = []
    score = 0
    for x in new_input:
        if x in reference:
            positiv_list.append(x)
            score += 1
    return score, positiv_list


comp_flower(user_input)

user_input = ["Rose", "Mimose", "Topfpflanze"]


def comp_flower(new_input):
    reference = ["Rose", "Mimose", "Feilchen"]
    score = 0
    positiv_list = []
    negativ_list = []
    for x in new_input:
        if x in reference:
            positiv_list.append(x)
            score += 1
    for y in new_input:
        if y not in reference:
            negativ_list.append(y)

    print(positiv_list)
    print(negativ_list)
    print(score)


comp_flower(user_input)