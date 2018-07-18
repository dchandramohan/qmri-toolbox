from JSONParsing import load_json
import tkinter as tk
from tkinter import *
from tkinter import filedialog

def load():
        filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file"
        ,filetypes = (("json files","*.json"),("all files","*.*")))
        textBox.insert(0.0, load_json(filename))
def save():
    newjson = textBox.get(1.0, END)
    f = filedialog.asksaveasfile(initialdir = "/",title = "Select file"
        ,filetypes = (("json files","*.json"),("all files","*.*")), defaultextension = "*.json" )
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    f.write(newjson)
    f.close()
    
def erase():
    textBox.delete(1.0, END)
        
root = tk.Tk()
root.geometry("650x650")

json = StringVar()

loadJson = tk.Button()
loadJson["text"] = "Load JSON"
loadJson["command"] = load
loadJson.pack(side="top")
loadJson.place(x = 0, y = 0)

saveJson = tk.Button()
saveJson["text"] = "Save JSON"
saveJson["command"] = save
saveJson.pack(side="top")
saveJson.place(x = 110, y = 0)

quit = tk.Button(root, text = "QUIT", fg="red",
                              command=root.destroy)
quit.pack(side="top")

erase = tk.Button(root, text = "ERASE", command  = erase)
erase.pack(side = "top")
erase.place(x = 220, y = 0)

textBox = Text(root, height=32, width=55, wrap = WORD)
textBox.pack(fill=BOTH, expand=1)
textBox.place()

            
mainloop()
