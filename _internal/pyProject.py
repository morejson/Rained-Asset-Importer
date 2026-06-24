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
# ttk.Separator(root, orient=HORIZONTAL).pack(fill=X, padx=15, pady=5)
# ttk.Label(root, text="Useful Links", font=("Georgia", 10)).pack(pady=10, anchor=W, padx=15)

for label, link in weblinks.items():
    ttk.Button(root, text=label, underline=0, width=35, command=lambda l=link: openlink(l)).pack(pady=0, anchor=W, padx=15)

def importtiles():
    importtile.config(state=DISABLED)
    importprop.config(state=DISABLED)
    tiles = filedialog.askopenfilename(title="Please select your tiles.", filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")], initialdir=Path.home() / "Downloads")

    if tiles:
        zip = zipfile.ZipFile(tiles) 

        copy_to_init = zip.open("Copy_To_Init.txt")
        if not copy_to_init: 
            messagebox.showerror("Error", "Couldn't find 'Copy_To_Init.txt' in the selected zip file.")
            importtile.config(state=NORMAL)
            importprop.config(state=NORMAL)
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
            importprop.config(state=NORMAL)
    else:
        importtile.config(state=NORMAL)
        importprop.config(state=NORMAL)







def importprops():
    importtile.config(state=DISABLED)
    importprop.config(state=DISABLED)
    props = filedialog.askopenfilename(title="Please select your props.", filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")], initialdir=Path.home() / "Downloads")

    if props:
        zip = zipfile.ZipFile(props) 

        copy_to_init = zip.open("Copy_To_Init.txt")
        if not copy_to_init: 
            messagebox.showerror("Error", "Couldn't find 'Copy_To_Init.txt' in the selected zip file.")
            importtile.config(state=NORMAL)
            importprop.config(state=NORMAL)
            return
        else:
            loadingbar = ttk.Progressbar(root, mode="determinate", length=550)
            loadingbar.pack(side=BOTTOM, pady=10)
            loadingbar.start()

            copy_to_init = copy_to_init.read().decode("utf-8")
            init_content = ""
            with open(propsinit, "r") as initfile:
                init_content = initfile.read()
            with open(propsinit, "w") as initfile:
                initfile.write(copy_to_init + "\n" + init_content)


            for file in zip.namelist():
                if file.lower().endswith(".png"):
                   zip.extract(file, path=propsfolder)
            
            loadingbar.stop()
            loadingbar.destroy()
            messagebox.showinfo("Success", "'" + os.path.basename(props) + "' imported successfully as props!")
            importtile.config(state=NORMAL)
            importprop.config(state=NORMAL)
    else:
        importtile.config(state=NORMAL)
        importprop.config(state=NORMAL)


ttk.Separator(root, orient=HORIZONTAL).pack(fill=X, padx=15, pady=5)

importtile = ttk.Button(root, text="Import Tiles (.zip)", width=50, underline=0, command=importtiles)
importtile.pack(pady=0)
importtile.config(state=DISABLED)

importprop = ttk.Button(root, text="Import Props (.zip)", width=50, underline=0, command=importprops)
importprop.pack(pady=0)
importprop.config(state=DISABLED)

rained = filedialog.askdirectory(title="Please Select 'Rained'", mustexist=True, initialdir=Path.home() / "Documents")
graphics = rained + "/Data/Graphics"
propsfolder = rained + "/Data/Props"
propsinit = propsfolder + "/Init.txt" 
init = graphics + "/Init.txt"


if not rained:
    root.destroy()
else:
    if os.path.exists(graphics) and os.path.exists(init) and os.path.exists(propsfolder) and os.path.exists(propsinit):
        importtile.config(state=NORMAL)
        importprop.config(state=NORMAL)
    else:    
        messagebox.showerror("Error", "Rained Graphics not found! Please relaunch and select the correct directory.")
        root.destroy()

root.mainloop()