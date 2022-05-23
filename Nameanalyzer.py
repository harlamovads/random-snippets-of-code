import time
from tqdm import tqdm
import re
import spacy
from itertools import combinations

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
searchmode = input("Что вы хотите сделать? Если собирать граф по конкретным именам персонажей, нажмите 1, если хотите сначала найти все имена - нажмите 2, если хотите посмотреть самые частотные имена по главам - нажмите 3 ")
if searchmode == "3":
    utoch = input("Если Вы хотите использовать для разделения слово, нажмите 1, если количество пустых строк - нажмите 2 ")
    if utoch == "1":
        abzinfo = input("Введите без кавычек слово, которое Вы хотите использовать для разделения текста. ")
if searchmode == "1" or searchmode == "2":
    utoch = input("Чем разделены абзацы в документе? Если табуляцией - нажмите 1, если пустыми строками - нажмите 2 ")
    if utoch == "1":
        abzinfo = "\t"
if utoch == "2":
        perem = int(input("Сколько пустых строк будут отделять новый кусок текста? "))
        abzinfo = "\n" * perem
if searchmode == "3":
    skolkoizglavy = int(input("Сколько героев вывести для каждого куска текста? "))
if searchmode == "1" or searchmode == "2":
    min_weight = int(input("Какой вес связи между героями будет минимально значимым и будет показан в графе? Введите число: "))
    

if searchmode == "1":
    worklist_1 = input("Введите через пробел все имена персонажей, которые Вас интересуют ")
    worklist_1 = worklist_1.split(" ")
    changebiglist_1 = []
    for wds_1 in worklist_1:
        if "_" in wds_1:
            worklist_1.remove(wds_1)
            changelist_1 = wds_1.split("_")
            changebiglist_1.append(changelist_1)
            for things_1 in changelist_1:
                worklist_1.append(things_1)
            changelist_1 = []

if searchmode == "2":
    chastfilter = int(input("С какой минимальной частотой будут встречаться значимые имена персонажей? "))   

file = open(filename, "r", encoding = "utf-8")
writefile = open("log.txt", "w")

if searchmode == "1" or searchmode == "2":
    writecsv = open(filename.split(".")[0] + "_graph.csv", "w")
    writefile.write(filename + "\n" + abzinfo + "\n")

nlp = spacy.load("en_core_web_sm")

dict1 = {} #словарь с номерами кусков текста и именами
dict2 = {} #словарь для частотности
dict3 = {} #вспомогательный словарь для сортировки charlist по частотности
pairdict = {} # словарь для вывода режима 2
maindict = {}
charlist = [] #список персонажей
finallist = [] #charlist но по частотности
finallist_chast = []
finaldict = {} # то же, что finallist, но для режима 3
chapterlist = [] # для режима 3: сюда пока идут словари с частотностью имен по главам
count = 0
check = 0
text = file.read()

import itertools
from collections import Counter
words = text.split(" ")
nextword = iter(words)
next(nextword)
freq=Counter(zip(words,nextword))
print(dict(freq))

textlist = text.split(abzinfo)
for i in tqdm(range(len(textlist))):
    count += 1 #счетчик номеров абзаца для словаря ниже
    abz = textlist[i].strip() #чистим текст
    res = normnamefinder(abz) #ищем через спейси все то, что похоже на имя
    for elem in res.copy(): #убираем из выдачи спейси все, что с маленькой буквы, итерируемся по копии списка во избежание
        if elem.islower() == True:
            res.remove(elem)
    dict1[count] = res # записываем в словарь под номером абзаца
    if searchmode == "3": # для режима 3: собираем список со словарями частотности для каждого куска текста
        for wgs in res:
            if wgs not in dict3:
                dict3[wgs] = 0
            if wgs in dict3:
                dict3[wgs] += 1
        chapterlist.append(dict3)
        dict3 = {}
    if searchmode == "1":
        for ima in res.copy():
            if ima not in worklist_1:
                res.remove(ima)
            dict1[count] = res

if searchmode == "3": # для режима 3: для каждого словаря из chapterlist ищем топ-n самых частотных имени собственных. 
    for dh in range(len(chapterlist)):
        if len(chapterlist[dh]) > skolkoizglavy:
            for s in range (skolkoizglavy):
                for keys in chapterlist[dh]:
                    if chapterlist[dh][keys] >= check:
                        check = chapterlist[dh][keys]
                        mean = keys
                finallist_chast.append(mean)
                check = 0
                chapterlist[dh].pop(mean)
            finaldict[dh] = finallist_chast
            finallist_chast = []
        if len(chapterlist[dh]) <= skolkoizglavy:
            for elems in chapterlist[dh]:
                finallist_chast.append(elems)
            finaldict[dh] = finallist_chast
            finallist_chast = []
    for numer, info in finaldict.items():
        print("Глава", int(numer)+1, ": ", info)
        writefile.write("Глава" + str(int(numer)+1) + ": " + str(info) + "\n")
        
    cont = input("Хотите, чтобы я попробовал угадать, какой герой главный? Введите да, если да, и нет, если нет ")
    if cont == "да":
        for ens, lists in finaldict.items():
            for h in range (len(lists)):
                if lists[h] not in maindict:
                    maindict[lists[h]] = 1            
                if lists[h] in maindict:
                    maindict[lists[h]] = maindict[lists[h]] + 1
#        print(maindict)
        check = 0
        for key1 in maindict:
            if maindict[key1] >= check:
                check = maindict[key1]
                mean = key1
        print(mean)

if searchmode == "1":
    for pair_1 in dict1.items():
        for name_1 in pair_1[1].copy():
            for clist_1 in changebiglist_1:
                if name_1 in clist_1:
                    pair_1[1].remove(name_1)
                    if clist_1[0] not in pair_1[1]:
                        pair_1[1].append(clist_1[0])

if searchmode == "1" or searchmode == "2":
    for wtuki in dict1: # собираем словарь частотности
        for k in range (len(dict1[wtuki])):
            if dict1[wtuki][k] not in dict2:
                dict2[dict1[wtuki][k]] = 0
            if dict1[wtuki][k] in dict2:
                dict2[dict1[wtuki][k]] = dict2[dict1[wtuki][k]] + 1
    
    for things in dict1:
        for w in range (len(dict1[things])): #записываем в charlist уникальные вхождения имен героев, потом отдадим это юзеру
            if searchmode == "2":
                if str(dict1[things][w]) not in charlist and dict2[dict1[things][w]] >= chastfilter: #фильтр для отсечения возможных опечаток.
                    charlist.append(dict1[things][w])
            if searchmode == "1":
                if str(dict1[things][w]) not in charlist: #фильтр для отсечения возможных опечаток.
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
    
    writefile.write(str(dict1) + "\n\n") #с номерами абзацев 
    writefile.write(str(dict2) + "\n\n") # с частотностью
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

if searchmode == "1" or searchmode == "2":
    for pair in dict1.items():
        if len(pair[1]) > 1:
#            print(pair[0], pair[1])
            for j in combinations(pair[1],2):
                j = tuple(sorted(j))
                if j in pairdict:
                    pairdict[j] += 1
                if j not in pairdict:
                    pairdict[j] = 1
    writecsv.write("Source,Type,Target,Weight" + "\n")
    for enters in pairdict.items():
        if int(enters[1]) >= min_weight:
            writecsv.write(enters[0][0] + "," + "Undirected" + "," + enters[0][1] + "," + str(enters[1]) + "\n")
    writecsv.close()
  
file.close()
writefile.close()
