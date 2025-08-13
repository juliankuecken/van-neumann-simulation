class Modell:
    def __init__(self, zeilen):
        self.zeilen = zeilen
        self.pc = 0
        self.akku = 0
        self.ende = False

class Wert:
    def __init__(self, referenz, value):
        self.referenz = referenz
        self.value = value

    def get(self, modell):
        x = self.value
        for i in range(0, referenz):
            zeile = modell.zeilen[x]
            if zeile.befehl != None:
                raise Exception("Syntax")
            x = zeile.wert
        return x

    def set(self, modell):
        if self.referenz == 0:
            raise Exception("Syntax, guck nochmal wie Sta funktioniert bro")
        x = self.value
        for i in range(0, referenz):
            zeile = modell.zeilen[x]
            if zeile.befehl != None:
                raise Exception("Syntax")
            x = zeile.wert
        zeile.wert = modell.akku
        
        
## lda()     

class Zeile:
    def __init__(self, befehl, wert):
        self.befehl = befehl
        self.wert = wert

    def ausführen(self, modell):
        if (self.befehl == "LDA"):
            modell.akku = self.wert.get(modell)
        elif (self.befehl == "STA"):
            self.wert.set(modell)
        elif self.befehl == "JMP":
            modell.pc = self.wert.get(modell)
        elif self.befehl == "STP":
            modell.ende = True

w1 = Wert(1, "05")
z1 = Zeile("LDA", w1)
w2 = Wert(1, "06")
z2 = Zeile("STA", w2)
z3 = Zeile("STP", None)


d = {
    "01": z1,
    "02": z2
}

m = Modell(d)
