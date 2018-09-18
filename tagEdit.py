#Marek Nesvadba, 2018, briskcz@gmail.com

from mutagen.id3 import ID3, APIC, TIT2, TALB, TPE1, TDRC, TCON,TRCK
from appJar import gui
import re

audio = None

def changeTags(btn):
    input = app.getAllEntries()

    if audio is not None:
        if input.get("skladba","") != "":#TIT2
            audio["TIT2"] = TIT2(encoding=3, text=input.get("skladba",""))
        if input.get("album","") != "":#TALB
            audio["TALB"] = TALB(encoding=3, text=input.get("album",""))
        if input.get("interpret","") != "":#TPE1
            audio["TPE1"] = TPE1(encoding=3, text=input.get("interpret",""))
        if input.get("rok","") != "":#TDRC
            num = input.get("rok")
            if len(num) == 4 and num.isnumeric():
                audio["TDRC"] = TDRC(encoding=3, text=num)
            else:
                print("Wrong date format!")
        if input.get("zanr","") != "":#TCON
            audio["TCON"] = TCON(encoding=3, text=input.get("zanr",""))
        if input.get("stopa","") != "":#TRCK
            audio["TRCK"] = TRCK(encoding=3, text=input.get("stopa",""))
        if input.get("fCover","") != "":#APIC
            imagedata = open(input.get("fCover",""), 'rb').read()
            audio.add(APIC(3, 'image/jpeg', 3, 'Front cover', imagedata))
            
        audio.save(v2_version=3)
        print("Tags for: " + str(app.getLabel("labelDisplay")) + " succesfully saved.")
            

    
def load(btn):
    global audio
    path = app.getEntry("f1")
    if path != "":
        filename = re.search('^.*[/](.+$)',path).group(1) #regex returns the filename
        app.setLabel("labelDisplay",filename) #set the filename to the label that should display it
        print("Loaded: " + str(path))
        audio = ID3(path)
        
        
        if 'TIT2' in audio:
            app.setEntry("skladba", audio["TIT2"][0], callFunction=False)
        if 'TALB' in audio:
            app.setEntry("album", audio["TALB"][0], callFunction=False)
        if 'TPE1' in audio:
            app.setEntry("interpret", audio["TPE1"][0], callFunction=False)
        if 'TDRC' in audio:
            app.setEntry("rok", audio["TDRC"][0], callFunction=False)
        if 'TCON' in audio:
            app.setEntry("zanr", audio["TCON"][0], callFunction=False)
        if 'TRCK' in audio:
            app.setEntry("stopa", audio["TRCK"][0], callFunction=False)
        
        
        

    
app = gui("Tag editor")

app.addLabel("l1", "Skladba:",0,0)
app.addEntry("skladba",0,1,2)

app.addLabel("l2", "Album:",1,0)
app.addEntry("album",1,1,2)

app.addLabel("l3", "Interpret:",2,0)
app.addEntry("interpret",2,1,2)

app.addLabel("l4", "Rok:",3,0)
app.addEntry("rok",3,1,2)

app.addLabel("l5", "Žánr:",4,0)
app.addEntry("zanr",4,1,2)

app.addLabel("l6", "Stopa:",5,0)
app.addEntry("stopa",5,1,2)

app.addLabel("l7", "Obrázek:",6,0)
app.addFileEntry("fCover",6,1,2)

app.addLabel("l8", "Soubor:",7,0)
app.addLabel("labelDisplay", "",7,1,2)

app.addHorizontalSeparator(8,0,3, colour="black")

app.addFileEntry("f1",9,0,3)
app.addButton("Uložit", changeTags,10,1)
app.addButton("Načíst", load,10,2)

app.go()