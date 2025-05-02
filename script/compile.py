import os
import shutil

PROGAM_NAME = "game"

cur_dir = os.path.dirname(__file__)

# essayer de supprimer les anciens program
try:
    os.remove(f"{cur_dir}\\..\\build\\pyxapp\\{PROGAM_NAME}.pyxapp")
except FileNotFoundError:
    pass
try:
    os.remove(f"{cur_dir}\\..\\build\\html\\{PROGAM_NAME}.html")
except FileNotFoundError:
    pass
try:
    os.remove(f"{cur_dir}\\..\\build\\exe\\{PROGAM_NAME}.exe")
except FileNotFoundError:
    pass

# créé le fichier pyxapp
os.system(f"pyxel package {cur_dir}\\..\\src {cur_dir}\\..\\src\\game.py")
os.rename(f"src.pyxapp", f"{cur_dir}\\..\\build\\pyxapp\\{PROGAM_NAME}.pyxapp")

# créé le fichier html
print(f"pyxel app2html {cur_dir}\\..\\build\\pyxapp\\{PROGAM_NAME}.pyxapp")
os.system(f"pyxel app2html {cur_dir}\\..\\build\\pyxapp\\{PROGAM_NAME}.pyxapp")
os.rename(f"{PROGAM_NAME}.html", f"{cur_dir}\\..\\build\\html\\{PROGAM_NAME}.html")

# créé le fichier exe
os.system(f"pyxel app2exe {cur_dir}\\..\\build\\pyxapp\\{PROGAM_NAME}.pyxapp")
os.rename(f"{PROGAM_NAME}.exe", f"{cur_dir}\\..\\build\\exe\\{PROGAM_NAME}.exe")

# suprimée les fichier par créé par Pyinstaller
os.remove(f"{PROGAM_NAME}.spec")
shutil.rmtree(f"build\\{PROGAM_NAME}")
try:
    os.rmdir("build")
except OSError:
    pass
