import tkinter as tk
from tkinter import ttk
from tkinter import Text, Scrollbar, messagebox
from assembler_modell_9 import *


class Textf(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.textfeld_rechts = tk.Text(self, wrap=tk.WORD, width=40, height=10)
        self.textfeld_rechts.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.textfeld_scrollbar1 = tk.Scrollbar(self, command=self.sync_scroll)
        self.textfeld_scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

        self.zeilennummer_text = tk.Text(self, wrap=tk.NONE, width=4, height=10, state=tk.DISABLED, bg='#E0E0E0')
        self.zeilennummer_text.grid(row=0, column=0, sticky="nsew")

    def sync_scroll(self, *args):
        yview = self.textfeld.yview()
        self.zeilennummer_text.yview_moveto(yview[0])
        self.textfeld_scrollbar.set(*yview)

    def aktualisiere_zeilennummern(self, event=None):
        self.zeilennummer_text.config(state=tk.NORMAL)
        self.zeilennummer_text.delete("1.0", tk.END)
        zeilen = self.textfeld.get("1.0", tk.END).count('\n')
        for i in range(0, zeilen + 1):
            self.zeilennummer_text.insert(tk.END, f"{i}\n")
        self.zeilennummer_text.config(state=tk.DISABLED)


class GUI(Textf):
    def __init__(self, model):
        self.m = model
        self.window = tk.Tk()
        self.window.title('Widgets and returns')

        self.textfeld_frame = tk.Frame(self.window)
        self.textfeld_frame.grid(row=0, column=1, rowspan=6, sticky="nsew")

        self.textfeld = Text(self.textfeld_frame, wrap=tk.WORD, width=40, height=10)
        self.textfeld.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.textfeld_scrollbar = Scrollbar(self.textfeld_frame, command=self.sync_scroll)
        self.textfeld_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.textfeld['yscrollcommand'] = self.textfeld_scrollbar.set

        self.textfeld.bind("<Key>", lambda event: (self.aktualisiere_zeilennummern(), self.sync_scroll()))
        self.textfeld.bind("<MouseWheel>", lambda event: (self.aktualisiere_zeilennummern(), self.sync_scroll()))

        self.zeilennummer_text = tk.Text(self.window, wrap=tk.NONE, width=4, height=10, state=tk.DISABLED, bg='#E0E0E0')
        self.zeilennummer_text.grid(row=0, column=0, sticky="nsew")

        self.aktualisiere_zeilennummern()

        self.speichern_button = tk.Button(self.window, text="Speichern & Korrigieren", command=self.korrigieren_u_speichern)
        self.speichern_button.grid(row=6, column=2, sticky="ew", padx=20, pady=20)

        self.ausführen_button = tk.Button(self.window, text="Ausführen", command=self.ausführen)
        self.ausführen_button.grid(row=6, column=1, sticky="ew", padx=20, pady=20)

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        self.button_load = tk.Button(self.window, text='Laden', command=self.laden)
        self.button_load.grid(column=2, row=4, padx=5, pady=5)

        self.pc_label = tk.Label(self.window, text='Program_Counter')  # Might have to change text to text_variable
        self.pc_label.grid(column=2, row=0, padx=20, pady=5)

        self.akku_label = tk.Label(self.window, text='Akkumulator')  # Same as PC_label with the text
        self.akku_label.grid(column=2, row=1, padx=20, pady=5)

        self.alu_label = tk.Label(self.window, text='Alu')
        self.alu_label.grid(column=2, row=2, padx=20, pady=5)

        self.check_var = tk.IntVar()

        self.single_step_checkbox = tk.Checkbutton(self.window, text="Einzelschritt", variable=self.check_var)
        self.single_step_checkbox.grid(column=2, row=5, padx=20, pady=20)

        self.window.mainloop()

    def ausführen(self):
        self.combined_functions_save()
        self.m.datei = open("Assembler_Program.txt", "r+")  # Neu ins Modell geladen
        if self.check_var.get():
            self.m.es_modus = True
            print("Single Step in ausführen")
            self.m.alles_ausfuehren()
        else:
            self.m.es_modus = False
            self.m.pc = 0
            self.m.akku = 0
            self.m.alu = [0, 0]
            self.m.ende = False
            self.m.alles_ausfuehren()
            self.m.pc = 0
            self.m.akku = 0
            self.m.alu = [0, 0]
            self.m.ende = False
        self.laden()

    def sync_scroll(self, *args):
        yview = self.textfeld.yview()
        print(self.textfeld_scrollbar.get())
        self.zeilennummer_text.yview_moveto(yview[0])
        self.textfeld_scrollbar.set(*yview)

    def label_update(self):
        self.pc_label.configure(text=f"")
        self.akku_label.configure(text=f"")
        self.alu_label.configure(text=f"")

    def aktualisiere_zeilennummern(self, event=None):
        self.zeilennummer_text.config(state=tk.NORMAL)
        self.zeilennummer_text.delete("1.0", tk.END)

        # Nummern für Zeilennummern einfügen
        # zeilen = self.textfeld.get("1.0", tk.END).count('\n') + 1  # Plus eins weg für Start bei 0 & 1 statt 0 & 1 & 2
        zeilen = self.textfeld.get("1.0", tk.END).count('\n')
        for i in range(0, zeilen + 1):      # Wenn plus eins weg: Start bei 0, "falsches" Nummerieren
            self.zeilennummer_text.insert(tk.END, f"{i}\n")
        self.zeilennummer_text.config(state=tk.DISABLED)

    def korrigieren_u_speichern(self):
        self.combined_functions_save()
        self.laden()

    def laden(self):
        with open("Assembler_Program.txt", "r") as file:
            gespeicherter_text = file.readlines()

        self.textfeld.delete("1.0", tk.END)

        zeilen_dict = {}
        for line in gespeicherter_text:
            parts = line.split(" ", 1)
            if len(parts) >= 2 and parts[   # Überspringe leere Zeilen wie 06 ohne weitere Zeichen
                0].strip().isdigit():  # Überprüfe, ob genügend Teile vorhanden und erster Teil eine Ganzzahl ist
                zeilennummer = int(parts[0]) + 1
                text = parts[1].strip()
                zeilen_dict[zeilennummer] = text

        max_zeilennummer = max(zeilen_dict.keys(), default=0)
        for i in range(1, max_zeilennummer + 1):
            text = zeilen_dict.get(i, "")  # Falls i nicht vorhanden, leeren Text einfügen
            self.textfeld.insert(tk.END, f"{text}\n")

        self.aktualisiere_zeilennummern()

    def string_to_dict(self, input_string):
        input_string = input_string.upper()
        lines = input_string.split('\n')
        result_dict = {}
        count_newlines = 0

        for line in lines:
            if line.strip():  # Überprüfen, ob die Zeile nicht leer ist (nach Entfernen von Leerzeichen)
                result_dict[count_newlines] = line
                count_newlines += 1
            else:
                result_dict[count_newlines] = None
                count_newlines += 1
        return result_dict

    def check_instruction_syntax(self, instruction):
        if instruction.startswith(' ') or instruction.endswith(' '):
            return False
        if instruction.startswith("LDA #") and instruction[6:].isdigit():
            # AKKU := xx
            return True
        elif instruction[:].isdigit():
            # only number
            return True
        elif instruction.startswith("LDA ") and instruction[4:].isdigit():
            # AKKU := RAM[xx]
            return True
        elif instruction.startswith("LDA (") and instruction[5:-1].isdigit() and instruction.endswith(')'):
            # AKKU := RAM[RAM[xx]]
            return True
        elif instruction.startswith("STA ") and instruction[4:].isdigit():
            # RAM[xx] := AKKU
            return True
        elif instruction.startswith("STA (") and instruction[5:-1].isdigit() and instruction.endswith(')'):
            # RAM[RAM[xx]] := AKKU
            return True
        elif any(instruction.startswith(op) and instruction[len(op):].isdigit() for op in ["ADD ", "SUB ", "MUL ", "DIV "]):
            # AKKU := AKKU+RAM[xx], AKKU := AKKU-RAM[xx], AKKU := AKKU*RAM[xx], AKKU := AKKU DIV RAM[xx]
            return True
        elif any(instruction.startswith(op) and instruction[len(op):].isdigit() for op in ["JMP ", "JNZ ", "JZE ", "JLE "]):
            # PZ := xx, PZ := RAM[xx], PZ := xx, wenn AKKU <> 0, PZ := RAM[xx], wenn AKKU <> 0, ...
            return True
        elif any(instruction.startswith(op) and (instruction[len(op):].startswith("(") and instruction[len(op):].endswith(")")) for op in ["JMP ", "JNZ ", "JZE ", "JLE "]):
            # PZ := xx, PZ := RAM[xx], PZ := xx, wenn AKKU <> 0, PZ := RAM[xx], wenn AKKU <> 0, ...
            return True
        elif any(instruction.startswith(op) and (instruction[len(op):].startswith("#")) for op in ["JMP ", "JNZ ", "JZE ", "JLE "]):
            # PZ := xx, PZ := RAM[xx], PZ := xx, wenn AKKU <> 0, PZ := RAM[xx], wenn AKKU <> 0, ...
            return True
        elif instruction == "STP":
            # STOP
            return True
        else:
            return False

    def check_program_syntax(self, program_dict):
        for key in sorted(program_dict.keys()):
            instruction = program_dict[key]
            if instruction is None:
                pass
            elif not self.check_instruction_syntax(instruction.strip()):
                string1 = f"Syntax error: ' {instruction} ' in line {key} !"
                messagebox.showerror('Syntax Error', string1)
                return False
        return True

    def write_to_text_file(self, program_dict, filename):
        with open(filename, 'w') as file:
            for key in sorted(program_dict.keys()):
                content = program_dict[key]
                line_number = str(key).zfill(2)  # Füge ggf. führende Nullen hinzu
                if content is not None:
                    file.write(f"{line_number} {content.strip()}\n")
                else:
                    file.write(f"{line_number}\n")

    # methode die ausliest --> in dictunray --> Syntax --> in Datei schreiben
    def combined_functions_save(self):
        dict_temp = self.string_to_dict(self.textfeld.get("1.0", tk.END))
        if not self.check_program_syntax(dict_temp):
            # print("syntax error")
            return False #Label ändern
        self.write_to_text_file(dict_temp, "Assembler_Program.txt")


f = open("Assembler_Program.txt", "r+")
gui = GUI(Modell(f))
# dt = open("Assembler_Program.txt", "r")

# model = model.Modell({})


'''Verbinden Gui und Modell:
model..es_modus=False
m.alles_ausfuehren()

bei einzelstep jedes mal alles ausführen'''