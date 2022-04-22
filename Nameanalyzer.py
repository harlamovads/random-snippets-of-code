import time
from tqdm import tqdm
from string import punctuation 
import re
from pymystem3 import Mystem
from enchant.checker import SpellChecker
import spacy

def spelchek(strochechka): #спеллчекер
    checker = SpellChecker("en_US")
    checker.set_text(strochechka)
    return([i.word for i in checker])

def normnamefinder(strocka): #(спейситыпросто)космос
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(strocka)
    spisok = []
    for token in doc:
        if token.pos_ == "PROPN":
            spisok.append(token.text)
    return(spisok)

def capsfinder(strochka):      #ищем слова капсом
    capslist = []
    wordlist = strochka.split(' ')
    for l in wordlist:
        if len(l) > 0 and l[0] == l[0].upper():
            capslist.append(l)
    return(capslist)

def lemmatizatia(spisok):      #код для лемматизации (пока не нужен)
    lemmas = []
    m = Mystem()
    for s in spisok:
        res = ''.join(m.lemmatize(s))
        lemmas.append(res.replace('\n', ''))
    return(lemmas)

def textlemm(tekst): # я бишь не помню, что это, пусть лежит пока
    m = Mystem()
    lemmas = m.lemmatize(tekst)
    return "".join(lemmas).strip()

file = open("ENGAutumnDr.txt", "r", encoding = "utf-8")
writefile = open("charlist.txt", "w")
dict1 = {} #словарь с номерами абзацев
dict2 = {} #словарь частотности
count = 0
charlist = list()
textlist = file.readlines()
#for b in tqdm(range(len(textlist))):
for i in tqdm(range(len(textlist))):
    count += 1 #счетчик номеров абзаца для словаря ниже
    abz = textlist[i].strip() #делим на абзацы
    pun_free = re.sub(r'[^\w\s]',' ', abz) #убираем пунктуацию, меняем на пробелы
    res1 = normnamefinder(pun_free) #ищем через спейси все то, что похоже на имя, теперь надо убрать оттуда все, что с маленькой буквы
#    print(abz)
    for elem in res1.copy(): # убираем из выдачи спейси все, что с маленькой буквы
        if elem.islower() == True:
            res1.remove(elem)
#    print(res1)
    dict1[count] = res1 # записываем в словарь под номером абзаца

for wtuki in dict1:
    for k in range (len(dict1[wtuki])):
        if dict1[wtuki][k] not in dict2:
            dict2[dict1[wtuki][k]] = 1
        if dict1[wtuki][k] in dict2:
            dict2[dict1[wtuki][k]] = dict2[dict1[wtuki][k]] + 1

print(dict1)
print(dict2)

for things in dict1:
    for w in range (len(dict1[things])): #записываем в charlist уникальные вхождения имен героев, потом отдадим это юзеру
        if str(dict1[things][w]) not in charlist and dict2[dict1[things][w]] > 2:
            charlist.append(dict1[things][w])
print(charlist)

#        print(things, dict1[things][w])
#    print("***")
#        if len(res) > 0:
#            print(res)
#        if len(res) == 1:
            
