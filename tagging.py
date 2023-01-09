def list_parser (stroka, typ):
    if typ == "lemma":
        lemma_list = []
        for token in nlp(stroka):
            lemma_list.append(token.lemma_)
        return (lemma_list)
    if typ == "pos":
        pos_list = []
        for token in nlp(stroka):
            pos_list.append(token.pos_)
        return(pos_list)
    if typ == "tag":
        tag_list = []
        for token in nlp(stroka):
            tag_list.append(token.tag_)
        return(tag_list)   
    if typ == "dep":
        dep_list = []
        for token in nlp(stroka):
            dep_list.append(token.dep_)
        return(dep_list)


from string import punctuation
import spacy
import re
import os
nlp = spacy.load("en_core_web_sm")

adres = "/mnt/c/Users/dasha/OneDrive/Документы/ЦГ/Прога/Практика"
try:
    os.mkdir("Размеченные файлы")
except FileExistsError:
    pass

adres1 = adres + "/Размеченные файлы/"

for files in os.listdir(adres):
    if files.endswith(".ann"):
        file = open(files, "r")
        text = file.readlines()
    
        writefile = open(adres1 + files, "w")
    
        file_essay = open(files[:-3]+"txt", "r")
        essay = file_essay.read()
        sentence_array = essay.split(".")
        vocab_sent = {}
        next = 0
        for sentence in sentence_array:
            next = next + len(sentence)
            vocab_sent[sentence] = next
    
        R1_1_condition = 0
        RC_list = ["that", "which", "who", "whom", "whose", "where", "when", "why"]
        addlist = []
        max_T = 0
        max_n = 0
        max_a = 0
    
        prev_line = ""
        for line in text:
            if line[0] == "T" and int(line.split("\t")[0].replace("T", "")) > max_T:
                max_T = int(line.split("\t")[0].replace("T", ""))
            if line[0] == "#" and int(line.split("\t")[0].replace("#", "")) > max_n:
                max_n = int(line.split("\t")[0].replace("#", ""))
            if line[0] == "A" and int(line.split("\t")[0].replace("A", "")) > max_a:
                max_a = int(line.split("\t")[0].replace("A", ""))
            change_check = 0
            if prev_line != "":
                if "disc " not in prev_line or "lemma" in line or "lemma" in prev_line:
                    if "Noerror" not in prev_line:
                        writefile.write(prev_line)
                    prev_line = ""
                if "Choice of tense" in prev_line: #проверка условия коррекции области исправления для R1_1
                    check_foe = prev_line.split("\t")[2]
                    check_foc = line.split("\t")[2] 
                    if "VBZ" in list_parser(check_foe, tag) and "VBD" in list_parser(check_foc, tag):
                        R1_1_condition = 1
                if "disc " in prev_line:
                    foe = prev_line.split("\t")[2].replace("\n", "")
                    foe_start = int(prev_line.split("\t")[1].split(" ")[1]) #получаем начало области ошибки
                    foe_fin = int(prev_line.split("\t")[1].split(" ")[2]) #получаем окончание области ошибки
                    if line.split("\t")[0][0] == "A": #получаем область исправления, если исправление - удаление компонента
                        foc = "Delete"
                    if line.split("\t")[0][0] != "A": #получаем область исправления
                        foc = line.split("\t")[2].replace("\n", "")
                    for numbers in vocab_sent.items(): #получаем предложение, с которым будем работать
                        if numbers[1] >= foe_start:
                            change_check = 1
                            working_sentence = numbers[0] 
                            break
                    if change_check == 0:
                        working_sentence = sentence_array[-1]
                    if "-" in foe and (foc == "- it" or foc == "it" or foc == "is"): #R1_1
                        prev_line = prev_line.replace("disc", "Absence_comp_sent", 1)
                        if R1_1_condition == 1 and "is" in foc:
                            line = line.replace("is", "was")
                    for rc_words in RC_list:
                        if rc_words in foe and rc_words in foc:
                            break
                        if rc_words in foc:
                            if re.sub(r"[^\w\s]","", foe) == re.sub(r"[^\w\s]","", foc):
                                prev_line = prev_line.replace("disc", "Relative_clause")
                        if rc_words in foe and foc == "Delete":
                            for tokens in nlp(working_sentence):
                                if tokens.text == rc_words:
                                    if tokens.dep_ == "nsubj":
                                        prev_line = prev_line.replace("disc", "Relative_clause")
                        if rc_words in foe and "that" in foc:
                            for tokens in nlp(working_sentence):
                                if tokens.text == rc_words:
                                    if tokens.dep_ == "nsubj":
                                        prev_line = prev_line.replace("disc", "Relative_clause")
                    if "NOUN" in list_parser(foc, "pos") and "NOUN" not in list_parser(foe, "pos"):
                        prev_line = prev_line.replace("disc", "Absence_comp_sent")
                    if ("AUX" in list_parser(foc, "pos") and not ("be" in list_parser(foe, "lemma") and "be" in list_parser(foc, "lemma"))) or ("NOUN" in list_parser(foc, "pos") and len(list_parser(foc, "pos")) == 1): #R1_5
                        if "can" in list_parser(foc, "lemma") and "can" not in list_parser(foe, "lemma"):
                            prev_line = prev_line.replace("disc", "Modals")
                        if "AUX" in list_parser(foc, "pos") and ("VBN" in list_parser(essay[foe_fin+1:][:essay[foe_fin+1:].find(" ")], "tag") or ("JJ" in list_parser(essay[foe_fin+1:][:essay[foe_fin+1:].find(" ")], "tag") and essay[foe_fin+1:][:essay[foe_fin+1:].find(" ")][-2:] == "ed")):
                            prev_line = prev_line.replace("disc", "Voice", 1)
                            prev_line = prev_line.replace(foe, essay[foe_fin+1:foe_fin+1 + essay[foe_fin+1:].find(" ")])
                            prev_line = prev_line.replace(str(foe_start), str(foe_fin+1))
                            prev_line = prev_line.replace(str(foe_fin), str(foe_fin+1 + essay[foe_fin+1:].find(" ")))
                            for token_2 in nlp(foc):
                                if token_2.pos_ == "AUX":
                                    line = line.replace(foc, token_2.text + " " + essay[foe_fin+1:foe_fin+1 + essay[foe_fin+1:].find(" ")])
                        if "AUX" in list_parser(foc, "pos") and "VBN" in list_parser(foc, "tag"):
                            prev_line = prev_line.replace("disc", "Voice", 1)
                            for tokeny in nlp(foc):
                                if tokeny.tag_ == "VBN":
                                    if tokeny.text not in working_sentence:
                                        for words in working_sentence.split(" "):
                                            if words[-2:] == "ed" and essay.find(words) > foe_start:
                                                prev_line = prev_line.replace(foe, words)
                                                prev_line = prev_line.replace(str(foe_start), str(essay.find(words)))
                                                prev_line = prev_line.replace(str(foe_fin), str(essay.find(words) + essay[essay.find(words):].find(" ")))
                        if "nsubj" not in list_parser(working_sentence, "dep") and "NOUN" in list_parser(foc, "pos"):
                            prev_line = prev_line.replace("disc", "Absence_comp_sent", 1)
                        if "be" in list_parser(foc, "lemma"):
                            prev_line = prev_line.replace("disc", "Absence_comp_sent", 1)
                    if "it" in list_parser(foe, "lemma") and foc == "Delete": #R2_1
                        prev_line = prev_line.replace("disc", "Redundant_comp", 1)
                    if "?" in foc and "What about" in working_sentence: #R3_1_1
                        prev_line = prev_line.replace(str(foe_start), str(essay.find("What about")), 1)
                        prev_line = prev_line.replace(str(foe_fin), str(essay.rfind("What about")), 1)
                        prev_line = prev_line.replace(foe, "What about")
                        line = line.replace(foc, "As for")
                        prev_line = prev_line.replace("disc", "Linking_device")
                    if "?" in foc and "what about" in working_sentence: #R3_1_2
                        prev_line = prev_line.replace(str(foe_start), str(essay.find("What about")), 1)
                        prev_line = prev_line.replace(str(foe_fin), str(essay.rfind("What about")), 1)
                        prev_line = prev_line.replace(foe, "what about")
                        line = line.replace(foc, "as for")
                        prev_line = prev_line.replace("disc", "Linking_device")
                    if (foe == ", an" or foe == ", a" or foe == ", the") and foc == "Delete": #R4_1
                        prev_line = prev_line.replace("disc", "Articles")
                    if "$" in foe: #R18_1, #R6_3
                        match = re.findall(r"[0-9]", foe)
                        if match:
                            if int(foe.find("$")) > int(foe.find(match[0])):
                                prev_line = prev_line.replace("disc", "Punctuation", 1)
                            if "million" in foc:
                                line = line.replace("million", "")
                                newline_1 = "T*\tNumerals " + str(foe_start) + " " + str(foe_fin) + "\t" + foc.replace("million", "")
                                newline_2 = "#*\tAnnotatorNotes T*\t" + foc
                            if "billion" in foc:
                                line  = line.replace("billion", "")
                                newline_1 = "T*\tNumerals " + str(foe_start) + " " + str(foe_fin) + "\t" + foc.replace("billion", "")
                                newline_2 = "#*\tAnnotatorNotes T*\t" + foc
                            if "thousand" in foc:
                                line  = line.replace("thousand", "")
                                newline_1 = "T*\tNumerals " + str(foe_start) + " " + str(foe_fin) + "\t" + foc.replace("thousand", "")
                                newline_2 = "#*\tAnnotatorNotes T*\t" + foc
                            if "hundred" in foc:
                                newline_1 = "T*\tNumerals " + str(foe_start) + " " + str(foe_fin) + "\t" + foc.replace("hundred", "")
                                newline_2 = "#*\tAnnotatorNotes T*\t" + foc
                    if "." in foe and ". " in foc:
                        if sentence_array.index(working_sentence) == len(sentence_array)-1:
                            prev_line = prev_line.replace("disc", "Noerror")
                        if sentence_array.index(working_sentence) < len(sentence_array)-1:
                            prev_line = prev_line.replace("disc", "Linking devices")
                    if "." in foe and "SCONJ" in list_parser(foe, "pos") and "," in foc and "SCONJ" in list_parser(foc, "pos"): #R12_2
                        prev_line = prev_line.replace("disc", "Conjunctions")
                    if foe == "is" and foc == foe + " that":
                        prev_line = prev_line.replace("disc", "Conjunctions")
                    if (foe == "it" and foc == "they") or (foe == "this" and foc == "these") or (foe == "that" and foc == "those"): #
                        prev_line = prev_line.replace("disc", "Agreement")
                    if (foe == "It" and foc == "They") or (foe == "This" and foc == "These") or (foe == "That" and foc == "Those"):
                        prev_line = prev_line.replace("disc", "Ref_device")
                    if (foe == "it" and (foc == "these" or foc == "those")) or (foe == "this" and (foc == "they" or foc == "those")) or (foe == "that" and (foc == "they" or foc == "these")):
                        prev_line = prev_line.replace("disc", "Ref_device")
                    if (foe == "it" and (foc == "that" or foc == "this")) or (foe == "this" and (foc == "it" or foc == "this")) or (foe == "that" and (foc == "it" or foc == "this")):
                        prev_line = prev_line.replace("disc", "Ref_device")
                    if (foe == "it" and foc == "them") or (foe == "them" and foc == "it"):
                        prev_line = prev_line.replace("disc", "Agreement")
                    if foe == "am" and foc == "Delete":
                        prev_line = prev_line.replace("disc", "Redundant_comp")
                    if foe == "it" and foc == "that":
                        prev_line = prev_line.replace("disc", "Ref_device")
                    if foe == "It" and foc == "That":
                        prev_line = prev_line.replace("disc", "Ref_device")
                    if "?" in foe and "," in foc:
                        prev_line = prev_line.replace("disc", "Inappropriate_register")
                    if (foe == "is" or foe == "was" or foe == "are" or foe == "were") and foc == "Delete": 
                        if "," in working_sentence:
                            for pieces in working_sentence.split(","):
                                if essay[foe_start-3:foe_fin+3] in pieces:
                                    if "auxpass" in list_parser(working_sentence, "dep") and "VBN" in list_parser(working_sentence[working_sentence.find(foe):], "tag"):
                                        prev_line = prev_line.replace("disc", "Voice")
                                        for token_3 in nlp(working_sentence):
                                            if token_3.tag_ == "VBN" and working_sentence.find(token_3.text)+essay.find(working_sentence) > foe_fin:
                                                check_1 = 0
                                                if len(essay[foe_start:(essay.find(token_3.text)+len(token_3.text))]) < 30:
                                                    if essay.find(token_3.text) > foe_start:
                                                        prev_line = prev_line.replace(str(foe_fin), str(essay.find(token_3.text)+len(token_3.text)))
                                                        prev_line = prev_line.replace(foe, essay[foe_start:(essay.find(token_3.text)+len(token_3.text))])
                                                        check_1 = 1
                                                    if essay.count(token_3.text) > 1 and check_1 == 0:
                                                        index = essay.find(token_3.text)
                                                        replace_str = token_3.text[:1] + "*" + token_3.text[2:]
                                                        while index < foe_start:
                                                            essay = essay.replace(token_3.text, replace_str, 1)
                                                            index = essay.find(token_3.text)
                                                        if len(essay[foe_start:(index+len(token_3.text))]) < 30:
                                                            prev_line = prev_line.replace(str(foe_fin), str(index+len(token_3.text)))
                                                            prev_line = prev_line.replace(foe, essay[foe_start:(index+len(token_3.text))])
                                                        line = ""
                                                        new_foc = essay[foe_start:(essay.find(token_3.text)+len(token_3.text))].replace(foe, "")
                                                        fix_t = prev_line.split("\t")[0]
                                                        addlist.append("\n#№  \t" + "AnnotatorNotes " + fix_t + "\t" + new_foc + "\n")
                                                if len(essay[foe_start:(essay.find(token_3.text)+len(token_3.text))]) >= 30:
                                                    prev_line = prev_line.replace("Voice", "disc")
                                    if "auxpass" not in list_parser(working_sentence, "dep"):
                                        prev_line = prev_line.replace("disc", "Redundant_comp")
                        if "," not in working_sentence:
                            if "auxpass" in list_parser(working_sentence, "dep") and "VBN" in list_parser(working_sentence[working_sentence.find(foe):], "tag"):
                                prev_line = prev_line.replace("disc", "Voice")
                                for token_3 in nlp(working_sentence):
                                    if token_3.tag_ == "VBN" and working_sentence.find(token_3.text)+essay.find(working_sentence) > foe_fin:
                                        if len(essay[foe_start:(essay.find(token_3.text)+len(token_3.text))]) < 30:
                                            prev_line = prev_line.replace(str(foe_fin), str(essay.find(token_3.text)+len(token_3.text)))
                                            prev_line = prev_line.replace(foe, essay[foe_start:(essay.find(token_3.text)+len(token_3.text))])
                                            line = ""
                                            new_foc = essay[foe_start:(essay.find(token_3.text)+len(token_3.text))].replace(foe, "")
                                            fix_t = prev_line.split("\t")[0]
                                            addlist.append("\n#№  \t" + "AnnotatorNotes " + fix_t + "\t" + new_foc + "\n")
                                        if len(essay[foe_start:(essay.find(token_3.text)+len(token_3.text))]) > 30:
                                            prev_line = prev_line.replace("Voice", "disc")
                            if "auxpass" not in list_parser(working_sentence, "dep"):
                                prev_line = prev_line.replace("disc", "Redundant_comp")
                    if "is" in foe and "are" in foc:
                        if "disc" not in prev_line:
                            addlist.append("\nT&  Agreement " + str(foe_start) + " " + str(foe_fin) + "   " + foe + "\n#№  \t" + "AnnotatorNotes " + "T&" + "\t" + foc + "\n")
                        if "disc" in prev_line:
                            prev_line = prev_line.replace("disc", "Agreement")
                    if "was" in foe and "were" in foc:
                        if "disc" not in prev_line:
                            addlist.append("\nT&  Agreement " + str(foe_start) + " " + str(foe_fin) + "   " + foe + "\n#№  \t" + "AnnotatorNotes " + "T&" + "\t" + foc + "\n")
                        if "disc" in prev_line:
                            prev_line = prev_line.replace("disc", "Agreement")
                    if foe == "be" and foc == "Delete":
                        prev_line = prev_line.replace("disc", "Redundant_comp")
                    if ")" in foc:
                        if "(" in working_sentence and ")" in working_sentence:
                            prev_line = prev_line.replace("disc", "Noerror")
                        else:
                            prev_line = prev_line.replace("disc", "Punctuation")
                    if "(" in foc:
                        if ")" in working_sentence and "(" in working_sentence:
                            prev_line = prev_line.replace("disc", "Noerror")
                        else:
                            prev_line = prev_line.replace("disc", "Punctuation")
                    if re.sub(r"[^\w\s]","", foe) == re.sub(r"[^\w\s]","", foc):
                        prev_line = prev_line.replace("disc", "Punctuation")
                        addlist.append("\nT&  punct " + str(foe_start) + " " + str(foe_fin) + "   " + foe + "\n#№  \t" + "AnnotatorNotes " + "T&" + "  " + foc + "\n")
                    if re.sub(r"[^\w\s]","", foe) == "" and foc == "Delete":
                        prev_line = prev_line.replace("disc", "Punctuation")
                    match = re.findall(r"[0-9]+", foe)
                    if match:
                        if foe == match and match in foc and "NOUN" in list_parser(foc, "pos"):
                            prev_line = prev_line.replace("disc", "Absence_explanation")
                    if "." in foc and "." not in foe:
                        addlist.append("\nT&  punct " + str(foe_start) + " " + str(foe_fin) + "   " + foe + "\n#№  \t" + "AnnotatorNotes " + "T&" + "  " + foc + "\n")
                    if foc == "Delete" and re.sub(r"[^\w\s]","", foe) != foe and "'s" not in foe:
                        addlist.append("\nT&  punct " + str(foe_start) + " " + str(foe_fin) + "   " + foe + "\nA~  \t" + "Delete " + "T&" + "\n")
                    if "Noerror" not in prev_line:
                        writefile.write(prev_line)
                    if "Noerror" in prev_line and "break" not in prev_line:
                        line = "Noerror break" + line
                    prev_line = line
            if prev_line == "":
                prev_line = line
        writefile.write(line)
        if len(addlist) > 0:
            corr_addlist = []
            for strings in addlist:
                max_T += 1
                max_n += 1
                max_a += 1
                strings = strings.replace("&", str(max_T))
                strings = strings.replace("№", str(max_n))
                strings = strings.replace("~", str(max_a))
                corr_addlist.append(strings)
        file.close()
        writefile.close()
        if len(addlist) > 0:
            writestrings = []
            checker = 0
            writefile_add = open(adres1 + files, "r")
            for lines in writefile_add:
                if "lemma" not in lines:
                    writestrings.append(lines)
                if "lemma" in lines and checker == 1:
                    writestrings.append(lines)
                if len(corr_addlist) != 0:
                    if lines.split("\t")[0] == corr_addlist[0].split("\t")[1].replace("AnnotatorNotes ", ""):
                        writestrings.append(corr_addlist[0])
                        corr_addlist.pop(0)
                if "lemma" in lines and checker == 0:
                    for strings_1 in corr_addlist:
                        writestrings.append(strings_1)
                    checker = 1
                    writestrings.append("\n")
                    writestrings.append(lines)
            writefile_add.close()
            writefile_rewrite = open(adres1 + files, "w")
            for things in writestrings:
                writefile_rewrite.write(things)
            writefile_rewrite.close()
        writefile_check = open(adres1 + files, "r")
        check_text = writefile_check.read()
        check_text = check_text.replace("\n\n", "\n")
        writefile_check.close()
        writefile_fix = open(adres1 + files, "w")
        writefile_fix.write(check_text)
        writefile_fix.close()
        file_essay.close()
