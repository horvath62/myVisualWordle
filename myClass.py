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


























