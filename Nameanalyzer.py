import time
from tqdm import tqdm
import re
#from enchant.checker import SpellChecker
import spacy
from itertools import combinations

#def spelchek(strochechka): #спеллчекер (не нужен, но мне жалко удалять, он хороший)
#    checker = SpellChecker("en_US")
#    checker.set_text(strochechka)
#    return([i.word for i in checker])

def normnamefinder(strocka): #(спейситыпросто)космос
    doc = nlp(strocka)
    spisok = []
    for token in doc:
        if token.pos_ == "PROPN":
            almost = token.text
            pun_free = re.sub(r"[^\w\s]","", almost) #убираем пунктуацию
            if len(pun_free) > 0:
                spisok.append(pun_free) 
    return(spisok)

filename = input("Введите, пожалуйста, имя файла с расширением ")
chastfilter = int(input("С какой минимальной частотой будут встречаться значимые имена персонажей? "))
abzinfo = input("Чем разделены абзацы в документе? Если двумя отступами - введите 1, одним отступом - нажмите 2, табуляцией - нажмите 3 ")
file = open(filename, "r", encoding = "utf-8")
writefile = open("charlist.txt", "w")
writecsv = open(filename.split(".")[0] + "_graph.csv", "w")
writefile.write(filename + "\n" + str(chastfilter) + "\n" + abzinfo + "\n")
nlp = spacy.load("en_core_web_sm")
dict1 = {} #словарь с номерами абзацев
dict2 = {} #словарь частотности
dict3 = {} #вспомогательный словарь для сортировки charlist по частотности
pairdict = {}
charlist = [] #список персонажей
finallist = [] #charlist но по частотности
count = 0
check = 0
text = file.read()
if abzinfo == "1":
    textlist = text.split("\n\n")
if abzinfo == "2":
    textlist = text.split("\n")
if abzinfo == "3":
    textlist = text.split("\t")
#print(textlist)
for i in tqdm(range(len(textlist))):
    count += 1 #счетчик номеров абзаца для словаря ниже
    abz = textlist[i].strip() #делим на абзацы
    res1 = normnamefinder(abz) #ищем через спейси все то, что похоже на имя, теперь надо убрать оттуда все, что с маленькой буквы
#    print(abz)
    for elem in res1.copy(): # убираем из выдачи спейси все, что с маленькой буквы, итерируемся по копии списка во избежание
        if elem.islower() == True:
            res1.remove(elem)
#    print(res1)
    dict1[count] = res1 # записываем в словарь под номером абзаца

for wtuki in dict1: # собираем словарь частотности
    for k in range (len(dict1[wtuki])):
        if dict1[wtuki][k] not in dict2:
            dict2[dict1[wtuki][k]] = 0
        if dict1[wtuki][k] in dict2:
            dict2[dict1[wtuki][k]] = dict2[dict1[wtuki][k]] + 1

#print(str(dict1)) # с номерами абзацев
writefile.write(str(dict1) + "\n")
#print(dict2) # с частотностью
writefile.write(str(dict2) + "\n")

for things in dict1:
    for w in range (len(dict1[things])): #записываем в charlist уникальные вхождения имен героев, потом отдадим это юзеру
        if str(dict1[things][w]) not in charlist and dict2[dict1[things][w]] > chastfilter: #фильтр для отсечения возможных опечаток.
            charlist.append(dict1[things][w])

for es in charlist: #формируем список по убыванию частотности
    dict3[es] = dict2[es]
for l in range (len(charlist)):
    for key in dict3:
        if dict3[key] >= check:
            check = dict3[key]
            mean = key
    finallist.append(mean)
    check = 0
    dict3.pop(mean)
print("Вот оно всё: ", finallist)
writefile.write("Вот оно все: " + str(finallist))

print("Введите, пожалуйста, имена героев, которые Вас интересуют, разделяя их пробелами.")
readstr = input("")
worklist = readstr.split(" ")
for pair in dict1.items(): #чистим словарик от не интересующих юзера имен
    for name in pair[1].copy():
        if name not in worklist:
            pair[1].remove(name)
    cleary = set(pair[1])
    clearly = list(cleary)
    dict1[pair[0]] = clearly
for pair in dict1.items(): # считаем пары героев в каждом абзаце
    if len(pair[1]) > 1:
        for j in combinations(pair[1],2):
            j = tuple(sorted(j))
            if j in pairdict:
                pairdict[j] += 1
            if j not in pairdict:
                pairdict[j] = 1
writecsv.write("Source,Type,Target,Weight" + "\n")
for enters in pairdict.items():
    writecsv.write(enters[0][0] + "," + "Undirected" + "," + enters[0][1] + "," + str(enters[1]) + "\n")
file.close()
writefile.close()
writecsv.close()
