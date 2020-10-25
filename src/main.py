import re
import glob

### Algoritma Knuth-Morris-Pratt
def kmpAlgorithm(text, pattern, fail):
    lenText = len(text)
    lenPat = len(pattern)

    i = 0
    j = 0

    while (i < lenText):
        if(pattern[j] == text[i]):
            if(j == lenPat - 1):
                return (i - lenPat + 1)
            i += 1
            j += 1
        elif(j > 0):
            j = fail[j-1]
        else:
            i += 1
    return -1


def matchFail(pattern):
    fail = [0]*len(pattern)
    fail[0]

    j = 0
    i = 1

    while (i < len(pattern)):
        if (pattern[i] == pattern[j]):
            fail[i] = j + 1
            j += 1
            i += 1
        elif (j > 0):
            j = fail[j-1]
        else:
            fail[i] = 0
            i += 1
    return fail
###

### Algoritma Booye-Moore
def bmAlgo(text, pattern, last):
    lenText = len(text)
    lenPat = len(pattern)
    i = lenPat-1

    if(i > lenText-1):
        return -1

    j = lenPat-1
    while(True):
        if(pattern[j] == text[i]):
            if(j == 0):
                return i
            else:
                i -= 1
                j -= 1
        else:
            lastOcc = last[ord(text[i])]
            i = i + lenPat - min(j, 1+lastOcc)
            j = lenPat - 1
        if(i > lenText-1):
            break
    return -1

def buildLast(pattern):
    last = [-1]*128

    for i in range(len(pattern)):
        last[ord(pattern[i])] = i
    
    return last

def readFile(file):
    f = open(file, "r")
    string = f.read()
    return string
###

def getSentence(string, pattern, algoMatch, algorithm):
    lowercaseText = string.lower()
    if(algorithm == "1"):
        idxFound = kmpAlgorithm(lowercaseText, pattern, algoMatch)
    elif(algorithm == "2"):
        idxFound = bmAlgo(lowercaseText, pattern, algoMatch)
    idxMin = idxFound
    idxMax = idxFound
    if(idxFound != -1):
        while(string[idxMin:idxMin+2] != ". " and string[idxMin] != "\n"):
            idxMin -= 1
            if(idxMin == 0):
                break
        
        while(string[idxMax-2:idxMax] != ". " and string[idxMax] != "\n"):
            idxMax += 1
            if(idxMax == len(string)-1):
                break
        if(idxMin == 0):
            sentence = string[idxMin:idxMax+1]
            next = string[idxMax:len(string)]
        else:
            sentence = string[idxMin+1:idxMax+1]
            next = string[idxMax:len(string)]
        return sentence, next
    else:
        return "", ""

def getArrSentence(text, pattern, algoMatch, algorithm):
    sentence, next = getSentence(text, pattern, algoMatch, algorithm)
    arrSentence = []
    while(next != "" and sentence != ""):
        arrSentence.append(sentence)
        sentence, next = getSentence(next, pattern, algoMatch, algorithm)
    return arrSentence

### Regular Expression
def regex(pattern, text):
    arrSentence = re.findall(re.compile(r'(?:^|[\.\n] )(.*?' + pattern + r'.*?)(?=[\.\n])', re.I), text)
    return arrSentence
###

def waktuTerjadi(sentence):
    waktu = re.findall(r'((Senin|Selasa|Rabu|Kamis|Jumat|Sabtu|Minggu)?\s?\(\d+[/-]\d+[/-]\d+\))', sentence)
    # waktu = re.findall(r'\d+/\d+/\d+',i)
    return waktu

def jumlahKorban(sentence):
    jumlah = re.findall(r'(^\d+ | \d+ | \d?\d?\d\.\d\d\d)',sentence)
    return jumlah

def printHasil(arrSentence, file):
    for i in arrSentence:
        jumlah = jumlahKorban(i)
        waktu = waktuTerjadi(i)
        waktu_art = waktuArtikel(file)
        if(jumlah != []):
            print("Jumlah: " + str(jumlah[0]), end=" ")
        if(waktu != []):
            print("Waktu: " + str(waktu[0][0]))
        elif(waktu == [] and waktu_art != []):
            print("Waktu: " + str(waktu_art[0][0]))
        else:
            print("Waktu:")
        print(" " + str(i) + "(" + str(file) + ")")
        print()

def waktuArtikel(text):
    waktu = re.findall(r'((Senin|Selasa|Rabu|Kamis|Jumat|Sabtu|Minggu)?\,?\s?[\d]{1,2}\s(Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)(\s\d{4})?)', text)
    return waktu

folderinput = input("Masukkan directory: ")
folder = glob.glob(folderinput + "/*.txt")
pattern = input("Masukkan pencarian: ")
pattern = pattern.lower()
while(True):
    print("Masukkan algoritma pencarian:")
    print("1. Knuth-Morris-Pratt")
    print("2. Boyer-Moore")
    print("3. Regular Expression")
    algorithm = input()
    if(algorithm != "1" and algorithm != "2" and algorithm != "3"):
        print("Masukan salah!")
        print()
    else:
        break

print("Hasil ekstraksi:")
if(algorithm == "1"):
    for file in folder:
        text = readFile(file)
        fail = matchFail(pattern)
        fullSentence = getArrSentence(text,pattern, fail, "1")
        printHasil(fullSentence, file)

elif(algorithm == "2"):
    for file in folder:
        text = readFile(file)
        last = buildLast(pattern)
        fullSentence = getArrSentence(text,pattern, last, "2")
        printHasil(fullSentence, file)

elif(algorithm == "3"):
    for file in folder:
        text = readFile(file)
        arrSentence = regex(pattern, text)
        printHasil(arrSentence, file)