from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
from pathlib import Path
import zipfile
import webbrowser
import json

root = Tk()

root.title("")
root.resizable(False, False)
root.geometry("600x400")

weblinks = os.path.dirname(os.path.realpath(__file__)) + "/weblinks.json"
weblinks = json.load(open(weblinks, "r"))

def openlink(link):
    webbrowser.open(link)

ttk.Label(root, text="Asset Importer - Rained", font=("Georgia", 25, "bold")).pack(pady=10, anchor=W, padx=15)
ttk.Label(root, text="Useful Links", font=("Georgia", 10)).pack(pady=10, anchor=W, padx=15)

for label, link in weblinks.items():
    ttk.Button(root, text=label, underline=0, width=35, command=lambda l=link: openlink(l)).pack(pady=0, anchor=W, padx=15)

def importtiles():
    importtile.config(state=DISABLED)
    tiles = filedialog.askopenfilename(title="Please select your tiles.", filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")], initialdir=Path.home() / "Downloads")

    if tiles:
        zip = zipfile.ZipFile(tiles) 

        copy_to_init = zip.open("Copy_To_Init.txt")
        if not copy_to_init: 
            messagebox.showerror("Error", "Couldn't find 'Copy_To_Init.txt' in the selected zip file.")
            importtile.config(state=NORMAL)
            return
        else:
            loadingbar = ttk.Progressbar(root, mode="determinate", length=550)
            loadingbar.pack(side=BOTTOM, pady=10)
            loadingbar.start()

            copy_to_init = copy_to_init.read().decode("utf-8")
            init_content = ""
            with open(init, "r") as initfile:
                init_content = initfile.read()
            with open(init, "w") as initfile:
                initfile.write(copy_to_init + "\n" + init_content)


            for file in zip.namelist():
                if file.lower().endswith(".png"):
                   zip.extract(file, path=graphics)
            
            loadingbar.stop()
            loadingbar.destroy()
            messagebox.showinfo("Success", "'" + os.path.basename(tiles) + "' imported successfully as tiles!")
            importtile.config(state=NORMAL)
    else:
        importtile.config(state=NORMAL)



importtile = ttk.Button(root, text="Import Tiles (.zip)", width=50, underline=0, command=importtiles)
importtile.pack(pady=20)
importtile.config(state=DISABLED)

rained = filedialog.askdirectory(title="Please Select 'Rained'", mustexist=True, initialdir=Path.home() / "Documents")
graphics = rained + "/Data/Graphics"
init = graphics + "/Init.txt"

if not rained:
    root.destroy()
else:
    if os.path.exists(graphics) and os.path.exists(init):
        importtile.config(state=NORMAL)
    else:    
        messagebox.showerror("Error", "Rained Graphics not found! Please relaunch and select the correct directory.")
        root.destroy()

root.mainloop()