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

    def bedingtes_jump(self, modell):
        if self.Zeile.befehl == "JNZ":
            if self.modell.akku > 0 or self.modell.akku < 0:
                self.modell.pc = self.get(modell)
        if self.Zeile.befehl == "JZE":
            if self.modell.akku = 0:
                self.modell.pc = self.get(modell)
        if self.Zeile.befehl == "JLE":
            if self.modell.akku <= 0:
                self.modell.pc = self.get(modell)
        if self.Zeile.befehl = "JGE":
            if self.modell.akku >= 0:
                self.modell.pc = self.get(modell)
        else:
            self.modell.pc += 1   

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
        elif self.befehl == "MUL":
            modell.akku *= self.wert.get(modell)
        elif self.befehl == "DIV":
            modell.akku /= self.wert.get(modell)
        elif self.befehl == "ADD":
            modell.akku += self.wert.get(modell)
        elif self.befehl == "SUB":
            modell.akku -= self.wert.get(modell)
        elif self.befehl == "JNZ" or self.befehl == "JZE" or self.befehl == "JLE" or self.befehl=="JGE":
            self.wert.bedingtes_jump(modell)
