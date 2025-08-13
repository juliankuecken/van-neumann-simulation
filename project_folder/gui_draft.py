import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Text, Scrollbar

# Verbesserungsvorschläge:
# Beim Einfügen von Zeilen dazwischen die indirekten Verweise der Befehle verändern
# Syntax Checking Fehler Highlighten
# Extra-Klasse für
# Alles in Großbuchstaben in der Datei speichern, Kleinschreibung der Befehle akzeptieren
# Für Syntax: Button zum "Glätten" der Eingaben in Datei schreiben, Großschreiben und korrigieren und wieder rein laden
# Button zum Syntax checken der Datei, doppel Leerzeichen durch einfach leerzeichen ersetzen


class GUI():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Widgets and returns')
        # Textfeld erstellen (rechte Seite)

        self.textfeld_frame = tk.Frame(self.window)
        self.textfeld_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        self.textfeld = Text(self.textfeld_frame, wrap=tk.WORD, width=40, height=10)
        self.textfeld.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.textfeld_scrollbar = Scrollbar(self.textfeld_frame, command=self.sync_scroll)
        self.textfeld_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.textfeld['yscrollcommand'] = self.textfeld_scrollbar.set

        self.textfeld.bind("<Key>", lambda event: (self.aktualisiere_zeilennummern(), self.sync_scroll()))
        self.textfeld.bind("<MouseWheel>", lambda event: (self.aktualisiere_zeilennummern(), self.sync_scroll()))

        # Textfeld für Zeilennummern (linke Seite)
        self.zeilennummer_text = tk.Text(self.window, wrap=tk.NONE, width=4, height=10, state=tk.DISABLED, bg='#E0E0E0')
        self.zeilennummer_text.grid(row=0, column=0, sticky="nsew")

        # Nummern für Zeilennummern einfügen
        self.aktualisiere_zeilennummern()

        # Button zum Speichern hinzufügen
        self.speichern_button = tk.Button(self.window, text="Speichern", command=self.speichern)
        self.speichern_button.grid(row=3, column=0, columnspan=2, sticky="ew")

        # Konfiguration für das Grid-Layout
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        # TEXTFELD IMPORT ENDE

        button_save = tk.Button(self.window, text='Laden', command=self.laden)
        button_save.grid(column=2, row=4, padx=5, pady=5)

        # Program Counter Label in Column 1 ...
        pc_label = tk.Label(self.window, text='Program_Counter')  # Might have to change text to text_variable
        pc_label.grid(column=2, row=1, padx=20, pady=5)

        akku_label = tk.Label(self.window, text='Akkumulator')  # Same as PC_label with the text
        akku_label.grid(column=2, row=2, padx=20, pady=5)

        alu_label = tk.Label(self.window, text='Alu')
        alu_label.grid(column=2, row=3, padx=20, pady=5)

        # GUI starten
        self.window.mainloop()

    def syntax_checking(self):
        pass


    def laden(self):
        with open("gespeicherter_text.txt", "r") as file:
            gespeicherter_text = file.readlines()
            self.textfeld.delete("1.0", tk.END)

        for line in gespeicherter_text:
            parts = line.split(" ", 1)
            if len(parts) == 2:
                zeilennummer, text = parts
                self.textfeld.insert(f"{zeilennummer}.0", text)
            else:
                self.textfeld.insert(tk.END, line)

        self.aktualisiere_zeilennummern()


    def speichern(self):
        text = self.textfeld.get("1.0", tk.END)
        print(text)
        with open("assembler.txt", "w") as file:
            file.write(text)


    def sync_scroll(self, *args):
        yview = self.textfeld.yview()
        self.zeilennummer_text.yview_moveto(yview[0])
        self.textfeld_scrollbar.set(*yview)


    # Funktion zum Aktualisieren der Zeilennummern
    def aktualisiere_zeilennummern(self, event=None):
        self.zeilennummer_text.config(state=tk.NORMAL)
        self.zeilennummer_text.delete("1.0", tk.END)

        # Nummern für Zeilennummern einfügen
        zeilen = self.textfeld.get("1.0", tk.END).count('\n') + 1
        for i in range(0, zeilen + 1):
            self.zeilennummer_text.insert(tk.END, f"{i}\n")

        self.zeilennummer_text.config(state=tk.DISABLED)


gui = GUI()
