import pandas as pd

df = pd.read_csv('Market_Basket_Optimisation-tests.csv', header=None)
dataset = df.values
# print (dataset)

# passo 1: definir o threshhold 

sThreshold = 0.1
numberOfTransactions = len(dataset)

# passo 2: definir uma tabela que expressa a frequência de cada item

# Primeiro criamos uma lista de todos os produtos disponíveis
listOfItems = []

for i in range(len(dataset)):
        for j in range(len(dataset[i])):
                if(dataset[i][j] not in listOfItems):
                    listOfItems.append(dataset[i][j])

# agora criamos contamos qual a frequência de cada item nas transações

singleItemFrequency = {}

for item in listOfItems:
    frequency = 0
    for i in range(len(dataset)):
        if(item in dataset[i]):
            frequency += 1
    singleItemFrequency[item] = frequency
    
# print(singleItemFrequency)

# Aplicando a exclusão baseado no threshold

supportThreshold = len(dataset) * sThreshold
# print("Support Threshold number: ", supportThreshold)

afterCleaning = {}


for key, value in singleItemFrequency.items():
    if(value > supportThreshold):
        afterCleaning[key]= value
        
# print (afterCleaning)
# Agora fazendo o mesmo procedimento com grupos de 2 produtos

def is_in_array(item1, item2, tocheck):
    for i in range(len(tocheck)):
        if item1 in tocheck[i] and item2 in tocheck[i]:
            return True
    return False

itemFrequency = []

for item1 in listOfItems:
    for item2 in listOfItems:
        if(item1 == item2):
            continue
        frequency = 0
        isIn = is_in_array(item1, item2, itemFrequency)
        if (isIn):
            continue
        for i in range(len(dataset)):
            if(item1 and item2 in dataset[i]):
                frequency += 1
        itemFrequency.append([item1,item2,frequency])
    
# print(itemFrequency)
twoItemsAfterCleaning = []


for i in range(len(itemFrequency)):
    if(itemFrequency[i][2] > supportThreshold):
        twoItemsAfterCleaning.append(itemFrequency[i])
# print (twoItemsAfterCleaning)

for item in twoItemsAfterCleaning:
    value = singleItemFrequency[item[0]]
    if value <= 0:
        value = 1
    confiance = (item[2]/numberOfTransactions)/value
    print(item[2], numberOfTransactions, value, '\n')

    print ("confiança de quem comprou ", item[0], " em comprar ", item[1], " = ", confiance)