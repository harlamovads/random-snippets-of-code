from enchant.checker import SpellChecker

def spelchek(strochechka):
    checker = SpellChecker("en_US")
    checker.set_text(strochechka)
    return([i.word for i in checker])

from string import punctuation 
import re
from pymystem3 import Mystem

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

def textlemm(tekst):
    m = Mystem()
    lemmas = m.lemmatize(tekst)
    return "".join(lemmas).strip()

file = open("ENGAutumnDr.txt", "r", encoding = "utf-8")
dict1 = {}
dict2 = {}
count = 0
globallist = []
textlist = file.readlines()
for i in range (len(textlist)):
    abz = textlist[i].strip() #делим на абзацы
#    print(abz)
    pun_free = re.sub(r'[^\w\s]',' ', abz) #убираем пунктуацию, меняем на пробелы
#    print(pun_free)
    spun_free = re.sub(r' +', ' ', pun_free) #убираем двойные пробелы
#    print(spun_free)
    out = capsfinder(spun_free) #ищем слова с большой буквы
#    print(out)
    if len(out) > 0:
        res = spelchek(str(out))
        if len(res) > 0:
            print(res)