import copy
class Wordlist:
    def __init__(self, words, title ):
        # A List of words
        self.words = words
        # Title for list
        self.title = title
        # Letter statistics - occurance
        self.letterstat = {}
        # Letter statistics - based on position
        self.letterlocstat = {}
        # Score for each word based on statistics
        self.score = {}


    def readwordfile(self, filename):
        try:
            with open(filename, "r") as fh:
                self.words = fh.read().splitlines()
                fh.close()
            return 1
        except IOError:
            print("IOError: ",filename," File does not seem to exist.")
            return fh

    def writewordfile(self, filename):
        try:
            with open(filename, "w") as fh:
                fh.writelines('\n'.join(self.words))
                fh.close()
                print("Writing File:",filename)
        except:
            print("Error on open file for write")


    def makelowercase(self):
        wordlist = []
        for w in self.words:
            wordlist.append(w.lower())
        return wordlist

    def wordsunion(self, wordlist):
        commonlist = []
        for w in self.words:
            for x in wordlist:
                if w == x:
                    commonlist.append(w)
        return commonlist

    def wordssubtract(self, wordlist):
        uniquelist = []
        for w in self.words:
            common = False
            for x in wordlist:
                if w == x:
                    common = True
            if common == False:
                uniquelist.append(w)
        return uniquelist

    def wordsmerge(self, wordlist):
        mergelist = self.words.copy()
        for x in wordlist:
            common = False
            for w in self.words:
                if w == x:
                    common = True
            if common == False:
                mergelist.append(x)
        return mergelist

    def trimwords(self, trimlength):
        trimlist = []
        for w in self.words:
            if len(w) == trimlength:
                trimlist.append(w)
        return trimlist

    def getWordcount(self):
        return len(self.words)

    def getWord(self, index):
        return self.words[index]

    def checkWord(self, word):
        if word in self.words:
            return True
        else:
            return False

    def addword(self, word):
        self.words.append(word)

    def removeword(self, word):
        self.words.remove(word)

    def formatwords(self, numcols, maxwords):
        rtn = '\n'
        rtn += "-------- " + str(self.title)+" "+str(len(self.words))+" words --------"
        if len(self.words)>maxwords:
            rtn += " showing "+str(maxwords)+" words -----"+'\n'
        else:
            rtn += '\n'
        col = 0
        cnt = 0
        for w in self.words:
            cnt = cnt + 1
            rtn += str(w) + " "
            col = col + 1
            if col % numcols == 0:
                rtn += '\n'
            if cnt >= maxwords:
                break
        return rtn

    def letterfrequency(self, cols):
        letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        for letter in letters:
            self.letterlocstat[letter]={}
            self.letterstat[letter] = 0
            for loc in range(cols):
                self.letterlocstat[letter][loc] = 0

        for word in self.words:
            for loc in range(cols):
                for letter in letters:
                    if word[loc] == letter:
                        self.letterstat[letter] += 1
                        self.letterlocstat[letter][loc] +=1

        sorted_letters = sorted(self.letterstat, key=self.letterstat.get, reverse=True)

        rtn = 'LETTER FREQUENCY:\nLetter Total  Postion 1 thru '+str(cols)+'......\n'
        for letter in sorted_letters:
            rtn += "  "+letter.upper()+" "+"{:5.0f}".format(self.letterstat[letter])+"   "
            for loc in range(cols):
                rtn += "{:4.0f}".format(self.letterlocstat[letter][loc]) + " "
            rtn += "\n"
        rtn += "\n"
        return rtn

    def wordscore(self, cols):
        rtn = 'WORD SCORE:\n'
        self.score = {}
        for word in self.words:
            self.score[word] = 0
            for loc in range(cols):
                self.score[word] += self.letterlocstat[word[loc]][loc]

        sorted_score = sorted(self.score, key=self.score.get, reverse=True)

        for word in sorted_score:
            rtn += word + " " + str(self.score[word]) + '\n'
            # print(word, self.score[word])
        rtn += '\n'
        return rtn

    def scorewords_noG(self, noGlist, cols):
        # Uses the self score, but apply to another wordlist (all the words)
        rtn = 'NO GREEN SCORE:\n'

        for word in self.words:
            for loc in range(col):
                letter = word[loc]
                if letter in noGlist:
                    pass
                else:
                    score[word] +=self.letterstat[letter]

        print(self.score)

        sorted_noGreen = sorted(self.words, key=self.score.get, reverse=True)

        for word in sorted_noGreen:
            rtn += word + " " + str(self.score[word]) + '\n'
            # print(word, self.score[word])
        rtn += '\n'
        return rtn


    def elimGscore(self, wordscore, cols):
        rtn = 'ELIM GREEN:\n'
        self.elimG = {}
        for word in self.words:
            self.elimG[word] = 0
            for letter in word:
                self.elimG[word] += wordscore.letterstat[letter]

        sorted_noGreen = sorted(self.elimG, key=self.elimG.get, reverse=True)

        for wordkey in sorted_noGreen:
            rtn += wordkey + " " + str(self.elimG[wordkey]) + '\n'
            # print(word, self.score[word])
        rtn += '\n'
        return rtn

        print(self.elimG)

    def noColorscore(self, wordscore, cols):
        rtn ='ELIM G:/n'
        self.noColor = {}
        return rtn


    def searchresults(self, letterlist, letterdict):

        # Search five letter Common Word List for Words meeting criteria
        # Deprecated: used in console version
        validwords = []
        wordcount = 0
        for w in self.words:
            wordtest = True
            for letter in letterlist:
                # print("letter:", letter)
                loclist = letterdict[letter]

                if loclist[0] == 0:
                    positiontest = True
                    for position in range(5):
                        # print("  position:", position)
                        if w[position - 1] == letter:
                            positiontest = False

                else:
                    positiontest = False
                    for position in loclist:
                        if w[position - 1] == letter:
                            positiontest = True

                if positiontest == False:
                    wordtest = False

            if wordtest == True:
                validwords.append(w)
                wordcount = wordcount + 1

        return validwords

    def criteriaresults(self, inputwordlist, criteria, cols):
        self.words = []
        for w in inputwordlist:
            # print('word:',w, end='')
            wordtest = True
            for letter in criteria:
                lettercount = 0
                crit = criteria[letter]
                hitloc = crit['hit']

                # HITS ( Green )
                # print('hitloc:',hitloc, end='')
                for loc in hitloc:
                    # print(' hit ',loc,' ',end='')
                    if w[loc] != letter.lower():
                        wordtest = False
                        # print('False', end='')
                missloc = crit['miss']

                # MISSES ( Yellow, Black )
                # print('missloc',missloc, end='')
                positiontest = True
                for loc in missloc:
                    # print(' miss ',loc,' ',end='')
                    if w[loc] == letter.lower():
                        positiontest = False
                        # print(' False ', end='')
                if positiontest == False:
                    wordtest = False

                # LETTER COUNT
                for loc in range(cols):
                    if w[loc] == letter.lower():
                        lettercount += 1
                # print('lettercount:',w,' ',letter,": ",lettercount)
                if crit['exact'] == 'Y':
                    if lettercount != crit['tot']:
                        wordtest = False
                        # print('POP exact',crit['tot'])
                else:         # NOT EXACT
                    if lettercount < crit['tot']:
                        wordtest = False
                        # print('POP not exact',crit['tot'])

                # ANY ( RED )
                if crit['any'] == 'Y':
                    if crit['exact'] == " Y":
                        if lettercount != crit['tot']:
                            wordtest = False
                            # print('POP Any exact')
                    else:  # not exact
                        if lettercount < crit['tot']:
                            wordtest = False
                            # print('POP Any')


            if wordtest == True:
                # print("MATCH:",w, lettercount)
                self.words.append(w)
            # print('')


class LetterCell:
    def __init__(self, row, col, letter):
        self.row = row
        self.col = col
        self.letter = letter
        self.color = 'B'

    def nextcolor(self):
        if self.color == 'B':
            self.color = 'Y'
        elif self.color == 'Y':
            self.color = 'G'
        elif self.color == 'G':
            self.color = 'R'
        elif self.color == 'R':
            self.color = 'V'
        else:
            self.color = 'B'

        return self.color

    def setletter(self, letter):
        self.letter = letter


class Criteria:
    def __init__(self, cols):
        # rowlist is representation of the wordle graphical visual fields (i.e. yellow letters, green letters, etc)
        self.rowlist = []         # list(rows) of dict(key=letter) of dict(key=location,value=cell color
        # rowlist gets converted to rowcrit. A more functional coded representation of the rows of visual letters
        self.rowcrit = []         # list(rows) of dict(key=letter) of dict(key=hit,miss,etc.(2 dict and 1 int and 2 chars)
        # rowcrit (list of row criteria) gets merged into a single criteria representing all the rows (mergecrit)
        self.mergecrit = {}       # dict(key=letter) of dict(key=hit,miss,etc.(2 dict and 1 int and 2 chars)
        # example
        # a:[G:[1],Y:[3],total:2,exact:N}
        # b:[G:[],Y:[2,5],total: 1, exact: ######WIP
        # c:[null], 0 only
        self.strcrit = ''   # for printing the criteria
        self.strerror = ''  # error messages from the merged criteria
        self.cols = cols    # number of columns (letters in word, legacy = 5)
        self.greenletters = []  # list of all letters that are green

    def scanwords(self, rows, cols, cell):
        # scans the GUI cells and makes the list of row (rowlist)
        self.rowlist = []

        for r in range(rows):
            # Row data is dict-dict example:
            # { A : { 0:G , 2:Y } , B : { 1:B } }
            # A in pos 0 is green and in pos 2 is yellow. B in pos 1 is black
            letterdict = {}
            for c in range(cols):
                letter = cell[r][c].letter
                color = cell[r][c].color
                if letter in letterdict:
                    letterdict[letter].update({c:color})
                elif letter == " ":
                    pass
                else:
                    letterdict[letter] = {c:color}
            if len(letterdict) > 0:
                self.rowlist.append(letterdict.copy())
            letterdict.clear()
        #print(self.rowlist)



    def printrowlist(self):
        for rowdata in self.rowlist:
            print("ROW:",end='')
            for letterkey in rowdata:
                print("<",letterkey,">  ",end='',sep='')
                tempdict = rowdata[letterkey]
                for loc in tempdict:

                    print(loc,":",tempdict[loc]," ",end='',sep='')
            print()
        print()


    def printrow(self,rowindex):
        print("ROW:",end='')
        rowdata = self.rowlist[rowindex]
        for letterkey in rowdata:
            print("<",letterkey,">  ",end='',sep='')
            tempdict = rowdata[letterkey]
            for loc in tempdict:
                print(loc,":",tempdict[loc]," ",end='',sep='')
        print()



    def makecriteria(self):
        # Make coded list of criteria per row from rowlist
        self.rowcrit = []
        for index, rowdata in enumerate(self.rowlist):

            lettercrit={}   # {'A': {'hit': [0], 'miss': [2], 'tot': 2, 'exact': 'N'}
            # A: { hit:[1] miss:[3] tot:2 exact:N }
            # B: { hit:[]  miss:[25] tot:1 exact:Y }
            # C: { hit:[]  miss:[4]  tot:1 exact:N }
            #print("### Rowdata:",rowdata)
            for letterkey in rowdata:
                if letterkey == " ":
                    lettercrit[letterkey]={}
                else:
                    letterdict = rowdata[letterkey]
                    # letterdict i.e: { 0:G , 1:B, 4:Y }
                    letterhit = []     # list of in this location(lockey) GREEN cell
                    lettermiss = []     # list of miss in this location YELLOW/BLACK
                    lettertot = 0      # total of GREEN and YELLOW cells
                    letterexact = "N"  # exactly total (true) or equal to or more than letter total (false)
                    letterany = "N"    # letter could be in any location
                    for lockey in letterdict:
                        if letterdict[lockey] == "G":
                            letterhit.append(lockey)
                            lettertot += 1
                        elif letterdict[lockey] == "Y":
                            lettermiss.append(lockey)
                            lettertot += 1
                        elif letterdict[lockey] == "B":
                            lettermiss.append(lockey)
                            letterexact = "Y"
                        elif letterdict[lockey] == "R":
                            lettermiss.append(lockey)
                            letterany = "Y"
                        elif letterdict[lockey] == "V":
                            lettermiss.append(lockey)
                        else:   # letterkey[lockey] == (space)
                            pass
                    tempdict={}
                    tempdict['hit']=letterhit
                    tempdict['miss']=lettermiss
                    tempdict['tot']=lettertot
                    tempdict['exact']=letterexact
                    tempdict['any']=letterany
                    lettercrit[letterkey]=tempdict.copy()
            self.rowcrit.append(lettercrit.copy())

    def mergecriteria(self):
        # Merge rowlist criteria (each row in list) into a single criteria (mergecrit)
        self.mergecrit={}
        self.strerror=''
        for rowidx, row in enumerate(self.rowcrit, start=1):
            mergeletters = list(set(list(self.mergecrit)+list(row)))
            # print("merge letters:",mergeletters)
            for letterkey in mergeletters:
                mcrit = d2d(letterkey, self.mergecrit)
                rcrit = d2d(letterkey, row)

                # merge row with existing criteria
                mhit = list(set(list(d2l('hit',mcrit)+d2l('hit',rcrit))))
                mmiss = list(set(list(d2l('miss', mcrit)+d2l('miss', rcrit))))
                mtot = max(d2i('tot',mcrit),d2i('tot',rcrit))
                if d2s('exact',mcrit) == "Y" or d2s('exact',rcrit) == "Y":
                    mexact = 'Y'
                else:
                    mexact = 'N'
                if d2s('any',mcrit) == "Y" or d2s('any',rcrit) == "Y":
                    many = 'Y'
                else:
                    many = 'N'

                # ##### Error checking merge ######
                if ((d2s('exact',mcrit) == "Y" and d2i('tot',rcrit)>d2i('tot',mcrit)) or
                    (d2s('exact',rcrit) == "Y" and d2i('tot',mcrit)>d2i('tot',rcrit))):
                    self.errorcriteria(rowidx,letterkey,"Inconsistent yellow or green cell count with black cell")

                if len( set(d2l('hit',mcrit)) & set(d2l('miss',rcrit)) ) > 0:
                    self.errorcriteria(rowidx, letterkey, "Inconsistent yellow/black versus green cell")
                if len( set(d2l('hit', rcrit)) & set(d2l('miss', mcrit)) ) > 0:
                    self.errorcriteria(rowidx, letterkey, "Inconsistent yellow/black versus green cell")

                # Error check: total misses plus total is greater than number of available cells
                if d2i('tot',rcrit)+len(d2l('miss',rcrit)) > self.cols:
                    self.errorcriteria(rowidx, letterkey, "Not enough cells for condition")

                # write back new merged criteria
                mcrit = {'hit':mhit, 'miss':mmiss, 'tot':mtot, 'exact':mexact, 'any':many}
                self.mergecrit[letterkey] = mcrit
                # print(' Merged:>>>' + str(self.mergecrit))

    def greenletter(self):
        self.greenletters = []
        # a:{hit:[1],miss:[3],total:2,exact:N}
        # b: .....
        for letterkey in self.mergecrit:
            singlelettercrit = self.mergecrit[letterkey]
            hitlist = singlelettercrit["hit"]
            if len(hitlist) != 0:
                # letter is green
                self.greenletters.append(letterkey)
                print("###>> ",self.greenletters)



    def elimGcriteria(self, criteria):
        self.mergecrit = {}
        # a:[hit:[1],miss:[3],total:2,exact:N}
        # b:.....
        # change all Green Letters to Black
        for letterkey in criteria:
            letterdict = copy.deepcopy(criteria[letterkey])
            hitlist = letterdict["hit"]
            letterdict['hit']=[]
            # letterdict['tot'] # no change
            letterdict['miss'] = letterdict['miss'] + hitlist
            self.mergecrit[letterkey]=letterdict


    # ##### WIP ######
    def noColorcriteria(self, criteria):
        self.mergecrit = {}
        # make criteria eliminating all yellow and black
        for letterkey in criteria:
            letterdict = copy.deepcopy(criteria[letterkey])
            hitlist = letterdict["hit"]
            misslist = letterdict['miss']
            letterdict['hit'] = []
            letterdict['tot'] = 0
            letterdict['miss'] = []
            self.mergecrit[letterkey] = letterdict
    # ######## WIP ###########


    def printcriteria(self):
        print("CRITERIA: ",self.mergecrit)
        '''
        for letterkey in self.mergecrit:
            letterdict = self.mergecrit[letterkey]
            # print("   ", letterkey," --> ",end="")
            for category in letterdict:
                print("  ", category, ":", letterdict[category], end="")
            print()
        '''


    def textcriteria(self):
        templabel=""
        '''
        for row in self.rowcrit:
            for letterkey in row:
                templabel += letterkey + "  "
                thingdict = row[letterkey]
                for thingkey in thingdict:
                    templabel += thingkey +":"+ str(thingdict[thingkey]) + "\t"
                templabel += "\n"
        templabel += "\n\n"
        '''
        for letterkey in self.mergecrit:
            templabel += letterkey + "  "
            thingdict = self.mergecrit[letterkey]
            for thingkey in thingdict:
                templabel += thingkey + ":" + str(thingdict[thingkey]) + "\t"
            templabel += "\n"
        self.strcrit = templabel

    def errorcriteria(self,row,letter,message):
        self.strerror += 'ERROR: Row:'+str(row)+" Letter:"+str(letter)+" "+message + "\n"

class Search:
    def __init__(self):
        self.rowlist = []

def printcells(rows,cols,cell):
    for rindex in range(rows):
        word = ">>>"
        color = ">>>"
        for cindex in range(cols):
            word += cell[rindex][cindex].letter
            color += cell[rindex][cindex].color
        word += "<<<"
        color += "<<<"
        print(word, color)

def d2d(thekey,thedict):
    rtn = {}
    if thekey in thedict:
        rtn = thedict[thekey]
    return rtn

def d2l(thekey, thedict):
    rtn = []
    if thekey in thedict:
        rtn = thedict[thekey]
    return rtn

def d2i(thekey, thedict):
    rtn = 0
    if thekey in thedict:
        rtn = thedict[thekey]
    return rtn

def d2s(thekey, thedict):
    rtn = 'N'
    if thekey in thedict:
        rtn = thedict[thekey]
    return rtn



# COLOR MAPPING
def cmap(colorcode):
   if colorcode == 'B':
       c = '#000000'
   elif colorcode == 'Y':
       c = '#CDAD00'
   elif colorcode == 'G':
       c = '#228B22'
   elif colorcode == 'R':
       c = '#B22222'
   elif colorcode == 'V':
       c = '#8470FF'  #LightSlateBlue
   else:
       c = '#FF1493'
   return c



















