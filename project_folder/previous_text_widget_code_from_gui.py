## This file is not supposed to work
## The following code is cut out of the GUI class's __init__()
## It is the previous implementation of the Textframe without a seperate class
        # Previously used Textf (now commented out)
        # # Textfeld erstellen (rechte Seite)
        # self.textfeld_frame = tk.Frame(self.window)
        # self.textfeld_frame.grid(row=0, column=1, rowspan=6, sticky="nsew")
        #
        # self.textfeld = Text(self.textfeld_frame, wrap=tk.WORD, width=40, height=10)
        # self.textfeld.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #
        # self.textfeld_scrollbar = Scrollbar(self.textfeld_frame, command=self.sync_scroll)
        # self.textfeld_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # self.textfeld['yscrollcommand'] = self.textfeld_scrollbar.set
        #
        # self.textfeld.bind("<Key>", lambda event: (self.aktualisiere_zeilennummern(), self.sync_scroll()))
        # self.textfeld.bind("<MouseWheel>", lambda event: (self.aktualisiere_zeilennummern(), self.sync_scroll()))
        #
        # # Textfeld für Zeilennummern (linke Seite)
        # self.zeilennummer_text = tk.Text(self.window, wrap=tk.NONE, width=4, height=10, state=tk.DISABLED, bg='#E0E0E0')
        # self.zeilennummer_text.grid(row=0, column=0, sticky="nsew")
        #
        # # Nummern für Zeilennummern einfügen
        # self.aktualisiere_zeilennummern()
        # Previously used Textf (comment end)

        # Objekt Textf TEST START
        #self.textf_test = Textf(self.window)
        #self.textf_test.grid(row=3, column=6, sticky="nsew")
        # Objekt Textf TEST ENDE

        # def sync_scroll(self, *args):
            #     yview = self.textfeld.yview()
            #     # print(yview)
            #     self.zeilennummer_text.yview_moveto(yview[0])
            #     # print(yview[0])
            #     # print(*yview)
            #     self.textfeld_scrollbar.set(*yview)     # First and Last of yview are percentages of the max scrollbar
            #
            # # Funktion zum Aktualisieren der Zeilennummern
            # def aktualisiere_zeilennummern(self, event=None):
            #     self.zeilennummer_text.config(state=tk.NORMAL)
            #     self.zeilennummer_text.delete("1.0", tk.END)
            #
            #     # Nummern für Zeilennummern einfügen
            #     # zeilen = self.textfeld.get("1.0", tk.END).count('\n') + 1  # Plus eins weg für Start bei 0 & 1 statt 0 & 1 & 2
            #     zeilen = self.textfeld.get("1.0", tk.END).count('\n')
            #     for i in range(0, zeilen + 1):      # Wenn plus eins weg: Start bei 0, "falsches" Nummerieren
            #         self.zeilennummer_text.insert(tk.END, f"{i}\n")
            #     self.zeilennummer_text.config(state=tk.DISABLED)