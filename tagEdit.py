#Marek Nesvadba, 2018, briskcz@gmail.com

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from appJar import gui
import re


def test(fpath):
	audio = MP3(fpath,ID3=EasyID3)
	print(audio.pprint())

def save(btn):
    print(btn)
	
def load(btn):
	path = app.getEntry("f1")
	if path != "":
		filename = re.search('^.*[/](.+$)',path).group(1) #regex returns the filename
		app.setLabel("l8",filename)
		print("Loaded: " + str(path))
		test(path)
		
		
		

	
app = gui("Tag editor")

app.addLabel("l1", "Skladba:",0,0)
app.addEntry("skladba",0,1)

app.addLabel("l2", "Album:",1,0)
app.addEntry("album",1,1)

app.addLabel("l3", "Interpret:",2,0)
app.addEntry("interpret",2,1)

app.addLabel("l4", "Rok:",3,0)
app.addEntry("rok",3,1)

app.addLabel("l5", "Žánr:",4,0)
app.addEntry("zanr",4,1)

app.addLabel("l6", "Stopa:",5,0)
app.addEntry("stopa",5,1)

app.addLabel("l7", "Soubor:",6,0)
app.addLabel("l8", "placeholder.mp3",6,1)

app.addButton("Uložit", save,7,0)
app.addButton("Načíst", load,7,1)
app.addFileEntry("f1",8,0,2)

app.go()