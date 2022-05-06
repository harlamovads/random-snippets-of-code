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
abzinfo = input("Чем разделены абзацы в документе? Если двумя отступами - введите 1, одним отступом - нажмите 2, табуляцией - нажмите 3 ")
searchmode = input("Вы хотите провести поиск по конкретным именам персонажей? Если да, нажмите 1, если нет - нажмите 2 ")
if searchmode == "1":
    worklist_us = input("Введите через пробел все имена персонажей, которые Вас интересуют ")
    worklist_us = worklist_us.split(" ")
    changebiglist_us = []
    for wds in worklist_us:
        if "_" in wds:
            worklist_us.remove(wds)
            changelist_us = wds.split("_")
            changebiglist_us.append(changelist_us)
            for thns in changelist_us:
                worklist_us.append(thns)
            changelist_us = []
if searchmode == "2":
    chastfilter = int(input("С какой минимальной частотой будут встречаться значимые имена персонажей? "))
file = open(filename, "r", encoding = "utf-8")
writefile = open("log.txt", "w")
writecsv = open(filename.split(".")[0] + "_graph.csv", "w")
writefile.write(filename + "\n" + str(chastfilter) + "\n" + abzinfo + "\n")
nlp = spacy.load("en_core_web_sm")
dict1 = {} #словарь с номерами абзацев
dict2 = {} #словарь частотности
dict3 = {} #вспомогательный словарь для сортировки charlist по частотности
pairdict = {}
charlist = [] #список персонажей
finallist = [] #charlist но по частотности2
count = 0
check = 0
text = file.read()
if abzinfo == "1":
    textlist = text.split("\n\n")
if abzinfo == "2":
    textlist = text.split("\n")
if abzinfo == "3":
    textlist = text.split("\t")
for i in tqdm(range(len(textlist))):
    count += 1 #счетчик номеров абзаца для словаря ниже
    abz = textlist[i].strip() #чистим
    if searchmode == "2":
        res1 = normnamefinder(abz) #ищем через спейси все то, что похоже на имя, теперь надо убрать оттуда все, что с маленькой буквы
        for elem in res1.copy(): # убираем из выдачи спейси все, что с маленькой буквы, итерируемся по копии списка во избежание
            if elem.islower() == True:
                res1.remove(elem)
        dict1[count] = res1 # записываем в словарь под номером абзаца
    if searchmode == "1":
        res1 = []
        for ima in worklist_us:
            if ima in abz:
                res1.append(ima)
            dict1[count] = res1
            
if searchmode == "1":
    for pair_us in dict1.items():
        for nme in pair_us[1].copy():
            for clist_us in changebiglist_us:
                if nme in clist_us:
                    pair_us[1].remove(nme)
                    if clist_us[0] not in pair_us[1]:
                        pair_us[1].append(clist_us[0])
print(dict1)

for wtuki in dict1: # собираем словарь частотности
    for k in range (len(dict1[wtuki])):
        if dict1[wtuki][k] not in dict2:
            dict2[dict1[wtuki][k]] = 0
        if dict1[wtuki][k] in dict2:
            dict2[dict1[wtuki][k]] = dict2[dict1[wtuki][k]] + 1

writefile.write(str(dict1) + "\n\n") # с номерами абзацев
writefile.write(str(dict2) + "\n\n") # с частотностью

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
    
writefile.write("Список частотности: " + str(finallist))    
if searchmode == "2":
    print("Вот оно всё: ", finallist)
    print("Введите, пожалуйста, имена героев, которые Вас интересуют, разделяя их пробелами. Если разные имена в списке - варианты имени одного персонажа, то введите их через _ Первым впишите то имя, которое хотите видеть в графике")
    readstr = input("")
    changebiglist = []
    worklist = readstr.split(" ")
    for wrds in worklist:
        if "_" in wrds:
            worklist.remove(wrds)
            changelist = wrds.split("_")
            changebiglist.append(changelist)
            for ths in changelist:
                worklist.append(ths)
            changelist = []
    for pair in dict1.items(): #чистим словарик от не интересующих юзера имен
        for name in pair[1].copy():
            if name not in worklist:
                pair[1].remove(name)
            for clist in changebiglist:
                if name in clist:
                    pair[1].remove(name)
                    pair[1].append(clist[0])
        cleary = set(pair[1])
        clearly = list(cleary)
        dict1[pair[0]] = clearly
    
for pair in dict1.items():
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
