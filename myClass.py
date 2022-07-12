class Wordlist:
  def __init__(self, words, title ):
      self.words = words
      self.title = title

  def readwordfile(self, filename):
      try:
          with open(filename, "r") as fh:
              self.words = fh.read().splitlines()
              fh.close()
          return 1
      except IOError:
          print("IOError: ",filename," File does not appear to exist.")
          return 0

  def writewordfile(self, filename):
      try:
          with open(filename, "w") as fh:
              fh.writelines('\n'.join(self.words))
      except:
          print("Error on open file for write")


  def makelowercase(self):
      wordlist = []
      for w in self.words:
          wordlist.append(w.lower())
      return wordlist

  def commonwords(self, wordlist):
      commonlist = []
      for w in self.words:
          for x in wordlist:
              if w == x:
                  commonlist.append(w)
      return commonlist

  def uniquewords(self, wordlist):
      uniquelist = []
      for w in self.words:
          common = False
          for x in wordlist:
              if w == x:
                  common = True
          if common == False:
              uniquelist.append(w)
      return uniquelist

  def trimwords(self, trimlength):
      trimlist = []
      for w in self.words:
          if len(w) == trimlength:
              trimlist.append(w)
      return trimlist

  def getWordcount(self):
      return len(self.words)

  def addword(self, word):
      self.words.append(word)

  def printwords(self, numcols, maxwords):
      print("")
      print("-------- ", self.title, " ", len(self.words), " words", " --------", end="" )
      if len(self.words)>maxwords:
          print(" showing ", maxwords, " words -----")
      else:
          print("")

      col=0
      cnt = 0

      for w in self.words:
          cnt = cnt + 1
          print(w, " ", end="")
          col = col + 1
          if col % numcols == 0:
            print("")
          if cnt >= maxwords:
              break

  def searchresults(self, letterlist, letterdict):

      # Search five letter Common Word List for Words meeting criteria
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
        else:
            self.color = 'B'

        return self.color

    def setletter(self, letter):
        self.letter = letter







class Criteria:
    def __init__(self):
        self.letterdata = []  #list of dict of (2 dict and 1 int and 1 value)
        # a:[G:[1],Y:[3],total:2,exact:N}
        # b:[G:[],Y:[2,5],total: 1, exact: ######WIP
        # c:[null], 0 only
        self.rowlist = []   #list(rows) of dict(key=letter) of dict(key=location,value=cell color

    def scanwords(self, rows, cols, cell):
        # list of row data
        self.rowlist = []

        for r in range(rows):
            # Row data is dict-dict
            # { A : { 0:G , 2:Y } , B : { 1:B } }
            # A in pos 0 is green and in pos 2 is yellow. B in pos 1 is black
            letterdict = {}
            for c in range(cols):
                letter = cell[r][c].letter
                color = cell[r][c].color
                if letter in letterdict:
                    letterdict[letter].update({c:color})
                else:
                    tempdict = {c:color}
                    letterdict[letter] = {c:color}
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



    def makecriteria(self,rowindex):
        lettercrit={}
        # A: { hit:[1] not:[3] tot:2 exact:N }
        # B: { hit:[]  not:[25] tot:1 exact:Y }
        # C: { hit:[]  not:[4]  tot:1 exact:N }
        rowdata = self.rowlist[rowindex]
        print("### Rowdata:",rowdata)
        for letterkey in rowdata:
            if letterkey == " ":
                lettercrit[letterkey]={}
            else:
                print("# Letterkey:",letterkey)
                letterdict = rowdata[letterkey]
                # letterdict i.e: { 0:G , 1:B, 2:Y }
                letterhit = []     # list of in this location(lockey) GREEN cell
                letternot = []     # list of not in this location YELLOW/BLACK
                lettertot = 0      # total of GREEN and YELLOW cells
                letterexact = "N"  # exactly total or equal to or more than lettertotal
                for lockey in letterdict:
                    if letterdict[lockey] == "G":
                        letterhit.append(lockey)
                        lettertot += 1
                    elif letterdict[lockey] == "Y":
                        letternot.append(lockey)
                        lettertot += 1
                    else:  # == "B"
                        letternot.append(lockey)
                        letterexact = "Y"
                tempdict={}
                tempdict['hit']=letterhit
                tempdict['not']=letternot
                tempdict['tot']=lettertot
                tempdict['exact']=letterexact
                # print("tempdict",tempdict)
                lettercrit[letterkey]=tempdict.copy()
                print(lettercrit[letterkey])
        self.letterdata.append(lettercrit)


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
   else:
       c = '#FF1493'
   return c



















