import tkinter as tk
from tkinter import ttk
from tkinter import Text, Scrollbar, messagebox


class Textframe(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, border=10)

        # # Create a ttk.Style instance
        # self.style = ttk.Style()
        #
        # # Configure the background color of the frame
        # self.style.configure("Blue.TFrame", background="blue")
        #
        # # Apply the style to the frame
        # self.configure(style="Blue.TFrame")

        # grid layout (unnecessary?)
        # self.rowconfigure(0, weight=1)
        # self.columnconfigure((0, 1, 2), weight=1, uniform='a')

        # self.grid_columnconfigure(1, weight=1)      # If window resized Textfeld object takes up space

        self.zeilennummer_text = tk.Text(self, wrap=tk.NONE, width=4, height=10, state=tk.DISABLED, bg='#E0E0E0')
        self.zeilennummer_text.grid(row=0, column=0, sticky="nsew")

        self.textfeld_rechts = tk.Text(self, wrap=tk.WORD, width=40, height=10)
        self.textfeld_rechts.grid(row=0, column=1, sticky="nsew")

        self.textfeld_scrollbar1 = tk.Scrollbar(self, command=self.sync_scroll)
        self.textfeld_scrollbar1.grid(row=0, column=2, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 1, 2), weight=1)

    def sync_scroll(self, *args):
        yview = self.textfeld_rechts.yview()
        self.zeilennummer_text.yview_moveto(yview[0])
        self.textfeld_scrollbar1.set(*yview)

    def aktualisiere_zeilennummern(self, event=None):
        self.zeilennummer_text.config(state=tk.NORMAL)
        self.zeilennummer_text.delete("1.0", tk.END)

        # Nummern für Zeilennummern einfügen
        # zeilen = self.textfeld.get("1.0", tk.END).count('\n') + 1  # Plus eins weg für Start bei 0 & 1 statt 0 & 1 & 2
        zeilen = self.textfeld_rechts.get("1.0", tk.END).count('\n')
        print(zeilen)
        for i in range(0, zeilen + 1):  # Wenn plus eins weg: Start bei 0, "falsches", versetztes Nummerieren
            self.zeilennummer_text.insert(tk.END, f"{i}\n")
        self.zeilennummer_text.config(state=tk.DISABLED)


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('pAssembler Python 3.9')

        # self.window.rowconfigure((0,1,2,3,4,5,6), weight=0)
        # self.window.columnconfigure((0,1), weight=0)

        self.textf = Textframe(self.window)
        self.textf.grid(row=0, column=0, rowspan=7, sticky="nsew")

        self.textf.textfeld_rechts.bind("<Key>", lambda event: (self.textf.aktualisiere_zeilennummern(), self.textf.sync_scroll()))
        self.textf.textfeld_rechts.bind("<MouseWheel>", lambda event: (self.textf.aktualisiere_zeilennummern(), self.textf.sync_scroll()))

        self.textf.aktualisiere_zeilennummern()

        self.speichern_button = tk.Button(self.window, text="Speichern & Korrigieren", command=self.korrigieren_u_speichern)
        self.speichern_button.grid(row=6, column=2, sticky="ew", padx=20, pady=20)

        self.button_load = tk.Button(self.window, text='Laden', command=self.laden)
        self.button_load.grid(column=2, row=4, padx=5, pady=5)

        self.pc_label = tk.Label(self.window, text='Program Counter')  # Might have to change text to text_variable
        self.pc_label.grid(column=2, row=1, padx=20, pady=5)

        self.akku_label = tk.Label(self.window, text='Akkumulator')  # Same as PC_label with the text
        self.akku_label.grid(column=2, row=2, padx=20, pady=5)

        self.alu_label = tk.Label(self.window, text='Alu')
        self.alu_label.grid(column=2, row=3, padx=20, pady=5)

        self.single_step_checkbox = tk.Checkbutton(self.window, text="Einzelschritt")
        self.single_step_checkbox.grid(column=2, row=5, padx=20, pady=20)

        self.window.mainloop()

    def korrigieren_u_speichern(self):
        self.combined_functions_save()
        self.laden()

    def laden(self):
        with open("Assembler_Program.txt", "r") as file:
            gespeicherter_text = file.readlines()

        # Textfeld leeren
        self.textfeld.delete("1.0", tk.END)

        # Dictionary für die Zeilen erstellen
        zeilen_dict = {}
        for line in gespeicherter_text:
            parts = line.split(" ", 1)
            if len(parts) >= 2 and parts[   # Überspringe leere Zeilen wie 06 ohne weitere Zeichen
                0].strip().isdigit():  # Überprüfe, ob genügend Teile vorhanden und erster Teil eine Ganzzahl ist
                zeilennummer = int(parts[0]) + 1
                text = parts[1].strip()
                zeilen_dict[zeilennummer] = text

        # Gespeicherten Text in das Textfeld einfügen
        max_zeilennummer = max(zeilen_dict.keys(), default=0)
        for i in range(1, max_zeilennummer + 1):
            text = zeilen_dict.get(i, "")  # Falls i nicht vorhanden, leeren Text einfügen
            self.textfeld.insert(tk.END, f"{text}\n")

        self.aktualisiere_zeilennummern()

    # Import Leander Auslesen, Syntax, in Datei schreiben
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
        # Überprüfe, ob Leerzeichen am Anfang oder am Ende der Anweisung vorhanden sind
        if instruction.startswith(' ') or instruction.endswith(' '):
            return False

        if instruction.startswith("LDA #") and instruction[6:].isdigit():
            # AKKU := xx
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
        elif instruction == "STP":
            # STOP
            return True
        else:
            return False

    def check_program_syntax(self, program_dict):
        for key in sorted(program_dict.keys()):
            instruction = program_dict[key]
            # instruction = instruction.strip()   # Remove unneccessary blanks in front and in end
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

print("HEllo World")
gui = GUI()
# dt = open("Assembler_Program.txt", "r")

# model = model.Modell({})
