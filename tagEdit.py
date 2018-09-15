#Marek Nesvadba, 2018, briskcz@gmail.com

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from appJar import gui
import re

audio = None

def test(fpath):#debug
	print(audio.pprint())

def save(btn):
	input = app.getAllEntries()
	print(input)
	if audio is not None:
		if input.get("skladba","") != "":
			audio["title"] = input.get("skladba","")
		if input.get("album","") != "":
			audio["album"] = input.get("album","")
		if input.get("interpret","") != "":
			audio["artist"] = input.get("interpret","")
		if input.get("rok","") != "":#cekovat jestli jsou to 4 cisla
			audio["date"] = input.get("rok","")
		if input.get("zanr","") != "":
			audio["genre"] = input.get("zanr","")
		if input.get("stopa","") != "":
			audio["tracknumber"] = input.get("stopa","")	
		
		
		
		
		audio.save()
	
def load(btn):
	global audio
	path = app.getEntry("f1")
	if path != "":
		filename = re.search('^.*[/](.+$)',path).group(1) #regex returns the filename
		app.setLabel("labelDisplay",filename) #set the filename to the label that should display it
		print("Loaded: " + str(path))
		audio = MP3(path,ID3=EasyID3)
		test(path) #debug
		
		
		

	
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
app.addLabel("labelDisplay", "placeholder.mp3",6,1)

app.addButton("Uložit", save,7,0)
app.addButton("Načíst", load,7,1)
app.addFileEntry("f1",8,0,2)

app.go()