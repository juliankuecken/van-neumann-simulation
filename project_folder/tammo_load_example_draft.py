import tkinter as tk
from tkinter import Text, Scrollbar

def speichern():
    text = textfeld.get("1.0", tk.END)
    print(text)
    with open("gespeicherter_text.txt", "w") as file:
        file.write(text)

def laden():
    with open("gespeicherter_text.txt", "r") as file:
        gespeicherter_text = file.readlines()
        
    textfeld.delete("1.0", tk.END)
        
    for line in gespeicherter_text:
        parts = line.split(" ", 1)
        if len(parts) == 2:
            zeilennummer, text = parts
            textfeld.insert(f"{zeilennummer}.0", text)
        else:
            textfeld.insert(tk.END, line)

    aktualisiere_zeilennummern()


def sync_scroll(*args):
    yview = textfeld.yview()
    zeilennummer_text.yview_moveto(yview[0])
    textfeld_scrollbar.set(*yview)

# Funktion zum Aktualisieren der Zeilennummern
def aktualisiere_zeilennummern(event=None):
    zeilennummer_text.config(state=tk.NORMAL)
    zeilennummer_text.delete("1.0", tk.END)

    # Nummern für Zeilennummern einfügen
    zeilen = textfeld.get("1.0", tk.END).count('\n') + 1
    for i in range(1, zeilen + 1):
        zeilennummer_text.insert(tk.END, f"{i}\n")

    zeilennummer_text.config(state=tk.DISABLED)

# GUI erstellen
root = tk.Tk()
root.title("Texteditor")

# Textfeld erstellen (rechte Seite)
textfeld_frame = tk.Frame(root)
textfeld_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

textfeld = Text(textfeld_frame, wrap=tk.WORD, width=40, height=10)
textfeld.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

textfeld_scrollbar = Scrollbar(textfeld_frame, command=sync_scroll)
textfeld_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
textfeld['yscrollcommand'] = textfeld_scrollbar.set

textfeld.bind("<Key>", lambda event: (aktualisiere_zeilennummern(), sync_scroll()))
textfeld.bind("<MouseWheel>", lambda event: (aktualisiere_zeilennummern(), sync_scroll()))

# Textfeld für Zeilennummern (linke Seite)
zeilennummer_text = tk.Text(root, wrap=tk.NONE, width=4, height=10, state=tk.DISABLED, bg='#E0E0E0')
zeilennummer_text.grid(row=0, column=0, sticky="nsew")

# Nummern für Zeilennummern einfügen
aktualisiere_zeilennummern()

# Button zum Speichern hinzufügen
speichern_button = tk.Button(root, text="Speichern", command=speichern)
speichern_button.grid(row=1, column=0, columnspan=2, sticky="ew")

# Button zum Laden hinzufügen
laden_button = tk.Button(root, text="Laden", command=laden)
laden_button.grid(row=2, column=0, columnspan=2, sticky="ew")

# Konfiguration für das Grid-Layout
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# GUI starten
root.mainloop()
