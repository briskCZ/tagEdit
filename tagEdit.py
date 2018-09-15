#Marek Nesvadba, 2018, briskcz@gmail.com

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from appJar import gui
import re

audio = None

def changeTags(btn):
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
		audio = EasyID3(path)
		
		
		if audio["title"][0] != "":
			app.setEntry("skladba", audio["title"][0], callFunction=False)
		if audio["album"][0] != "":
			app.setEntry("album", audio["album"][0], callFunction=False)
		if audio["artist"][0] != "":
			app.setEntry("interpret", audio["artist"][0], callFunction=False)
		if audio["date"][0] != "":
			app.setEntry("rok", audio["date"][0], callFunction=False)
		if audio["genre"][0] != "":
			app.setEntry("zanr", audio["genre"][0], callFunction=False)
		if audio["tracknumber"][0] != "":
			app.setEntry("stopa", audio["tracknumber"][0], callFunction=False)
		
		
		

	
app = gui("Tag editor")

app.addLabel("l1", "Skladba:",0,0)
app.addEntry("skladba",0,1,2)

app.addLabel("l2", "Album:",1,0)
app.addEntry("album",1,1,2)

app.addLabel("l3", "Interpret:",2,0)
app.addEntry("interpret",2,1,2)

app.addLabel("l4", "Rok:",3,0)
app.addNumericEntry("rok",3,1,2)

app.addLabel("l5", "Žánr:",4,0)
app.addEntry("zanr",4,1,2)

app.addLabel("l6", "Stopa:",5,0)
app.addEntry("stopa",5,1,2)

#app.addLabel("l7", "Obrázek:",6,0)
#app.addFileEntry("fCover",6,1,2)

app.addLabel("l8", "Soubor:",7,0)
app.addLabel("labelDisplay", "placeholder.mp3",7,1,2)

app.addHorizontalSeparator(8,0,3, colour="black")

app.addFileEntry("f1",9,0,3)
app.addButton("Uložit", changeTags,10,1)
app.addButton("Načíst", load,10,2)

app.go()