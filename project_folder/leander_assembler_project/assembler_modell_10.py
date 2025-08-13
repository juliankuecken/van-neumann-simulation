import math

class Modell:
    def __init__(self, datei):
        self.datei = datei
        self.zeilen = lesen(datei)
        self.pc = 0
        self.akku = 0
        self.alu=[0,0]
        self.ende = False
        self.es_modus=False
    
    def alles_ausfuehren(self):
        self.datei.seek(0)
        self.zeilen = lesen(self.datei)
        while not self.ende:
            if self.zeilen[self.pc].befehl is None:
                raise Exception("Execution, line %s has no instruction" % self.pc)
            self.zeilen[self.pc].befehle(self)
            self.pc+=1
            if self.es_modus:
                break
        self.datei.seek(0)
        self.datei.truncate(0)
        schreiben(self.datei, self.zeilen)
        self.datei.flush()

class Wert:
    def __init__(self, referenz, value):
        self.referenz = referenz
        self.value = value

    def get(self, modell):
        x = self.value
        for i in range(0, self.referenz):
            zeile = modell.zeilen[x]
            if zeile.befehl != None:
                raise Exception("Execution, value references line %s, which doesn't have data" % x)
            x = zeile.wert.value
        return x

    def set(self, modell):
        if self.referenz == 0:
            raise Exception("Syntax, guck nochmal wie Sta funktioniert bro")
        x = self.value
        for i in range(0, self.referenz):
            if x in modell.zeilen:
                zeile = modell.zeilen[x]
            else: 
                if i != self.referenz-1:
                    raise Exception("kein wert bei verwies")
                w = Wert(0,modell.akku)
                z = Zeile(None, w)
                modell.zeilen[x] = z
                break
            if zeile.befehl != None:
                raise Exception("Syntax")
            w = Wert(0,modell.akku)
            modell.zeilen[x] = Zeile(None, w)
            x = zeile.wert.value
    

class Zeile:
    def __init__(self, befehl, wert):
        self.befehl = befehl
        self.wert = wert
            
            
    def j_befehle(self, modell):
        if self.befehl == "JMP":
            modell.pc = self.wert.get(modell)-1
        elif self.befehl == "JNZ":
            if modell.akku > 0 or modell.akku < 0:
                modell.pc = self.wert.get(modell)-1
        elif self.befehl == "JZE":
            if modell.akku == 0:
                modell.pc = self.wert.get(modell)-1
        elif self.befehl == "JLE":
            if modell.akku <= 0:
                modell.pc = self.wert.get(modell)-1
        elif self.befehl == "JGE":
            if modell.akku >= 0:
                modell.pc = self.wert.get(modell) -1
        

    def befehle(self, modell):
        if modell.zeilen[modell.pc].befehl[0]== "J":
            self.j_befehle(modell)
        elif (self.befehl == "LDA"):
            modell.akku = self.wert.get(modell)
        elif (self.befehl == "STA"):
            self.wert.set(modell)
        elif self.befehl == "STP":
            modell.ende = True
        elif self.befehl == "MUL":
            modell.alu[0] = int(modell.akku)
            modell.alu[1] = int(self.wert.get(modell))
            modell.akku = modell.alu[0]*modell.alu[1]
        elif self.befehl == "DIV":
            modell.alu[0] = int(modell.akku)
            modell.alu[1] = int(self.wert.get(modell))
            modell.akku = round(modell.alu[0]/modell.alu[1])  
        elif self.befehl == "ADD":
            modell.alu[0] = int(modell.akku)
            modell.alu[1] = int(self.wert.get(modell))
            modell.akku = modell.alu[0]+modell.alu[1]
        elif self.befehl == "SUB":
            modell.alu[0] = int(modell.akku)
            modell.alu[1] = int(self.wert.get(modell))
            modell.akku = modell.alu[0]-modell.alu[1]
        

def lesen_wert_mit_hashtag(string):
    referenz = 0
    for i in range(0, len(string)):
        if not string[i] == "#":
            if not string[i:].isdigit():
                raise Exception("Syntax")
            return Wert(referenz, int(string[i:]))
        referenz += 1

def lesen_wert(string):
    referenz = 1
    for i in range(0, len(string)):
        if string[i]=="#":
            if not string[i + 1:].isdigit():
                raise Exception("Syntax, wert enthält keine zahlen nach #")
            return Wert(0, int(string[i + 1:]))
        elif string[i] == "(":
            referenz += 1
        else:
            s = string[i:]
            return Wert(referenz, int(s[:len(s) - (referenz - 1)]))
        
def lesen(dt):
        d = {}
        lines = dt.readlines()
        for line in lines:
            line = line.split()
            if len(line) < 2:
                continue
            if not line[0].isdigit():
                raise Exception("Syntax")
            addresse = int(line[0])
            if line[1].isdigit():
                befehl = None
                wert = lesen_wert(line[1])
            else:
                befehl=line[1].upper()
                if len(line) == 3:
                    wert = lesen_wert(line[2])
                else:
                    wert = None
            if befehl != None and befehl.startswith("J"):
                wert.referenz -=1
                                 
            z = Zeile(befehl, wert)
            d[addresse] = z
        
        return d
def lesen_gut(dt):
        d = {}
        lines = dt.readlines()
        for line in lines:
            line = line.split()
            if len(line) < 2:
                continue
            if not line[0].isdigit():
                raise Exception("Syntax")
            addresse = int(line[0])
            if line[1].isdigit():
                befehl = None
                wert = lesen_wert(line[1])
            else:
                befehl=line[1].upper()
                if len(line) == 3:
                    wert = lesen_wert(line[2])
                else:
                    wert = None
            z = Zeile(befehl, wert)
            d[addresse] = z
        return d
    
def schreiben_wert(file, wert):
    if wert.referenz == 0:
        return "#" + str(wert.value)
    else:
        s = ""
        for i in range(0, wert.referenz - 1):
            s += "("
        s += str(wert.value)
        for i in range(0, wert.referenz - 1):
            s += ")"
        return s

    
def schreiben_wert_mit_hashtag(file, wert):
    s = ""
    for i in range(0, wert.referenz):
        s += "#"
    s += str(wert.value)
    return s
    

def schreiben(file, zeilen):
    zeilen = dict(sorted(zeilen.items()))
    for addresse, zeile in zeilen.items():
        s = str(addresse) + " "
        if zeile.befehl == None:
            s += str(zeile.wert.value)
        else:
            
            s += zeile.befehl + " "
            if not zeile.befehl == "STP":
                if zeile.befehl.startswith("J"):
                    zeile.wert.referenz +=1
                s += schreiben_wert(file, zeile.wert)
        file.write(s + "\n")

# f = open("test.txt", "r+")
# m = Modell(f)
# m.alles_ausfuehren()
