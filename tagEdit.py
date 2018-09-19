#Marek Nesvadba, 2018, briskcz@gmail.com

#TODO: popup windows

from mutagen.id3 import ID3, APIC, TIT2, TALB, TPE1, TDRC, TCON,TRCK
from appJar import gui
import re

audio = None

fPaths = []

def clearFiles(btn):        # deletes all files from the listbox
    global fPaths
    app.clearListBox("seznam", callFunction=False)
    fPaths.clear()
    app.clearAllEntries(callFunction=False)
    app.setLabel("labelDisplay","Žádný soubor nevybrán.")  
       
def editTags(btn):      # tags of selected files can be edited
    global audio
    chosenList = []
    for x in app.getListBox("seznam"):      #for each selected item
        i = app.getAllListItems("seznam").index(x)      #get index from list all items
        chosenList.append(fPaths[i])        #appends paths to selected files to chosenList
    
    if len(chosenList) == 1:
        app.clearAllEntries(callFunction=False)
        audio = ID3(chosenList[0])
        
        filename = re.search('^.*[/](.+$)',chosenList[0]).group(1)       #regex returns the filename
        app.setLabel("labelDisplay",filename)       #set the filename to the label that should display it
        
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
            
    if len(chosenList) > 1:
        app.clearAllEntries(callFunction=False)
        loadedList = []
        for x in chosenList:
            loadedList.append(ID3(x))
        
        app.setLabel("labelDisplay","Více souborů vybráno.")
        
        sameSkladba = 0
        sameAlbum = 0
        sameInterpret = 0
        sameRok = 0
        sameZanr = 0
        sameStopa = 0
        
        for i in range(0,len(loadedList)):
            if loadedList[i]["TIT2"][0] == loadedList[0]["TIT2"][0]:
                sameSkladba += 1
            if loadedList[i]["TALB"][0] == loadedList[0]["TALB"][0]:
                sameAlbum += 1   
            if loadedList[i]["TPE1"][0] == loadedList[0]["TPE1"][0]:
                sameInterpret += 1      
            if loadedList[i]["TDRC"][0] == loadedList[0]["TDRC"][0]:
                sameRok += 1      
            if loadedList[i]["TCON"][0] == loadedList[0]["TCON"][0]:
                sameZanr += 1      
            if loadedList[i]["TRCK"][0] == loadedList[0]["TRCK"][0]:
                sameStopa += 1      
                
        if sameSkladba == len(loadedList):
            app.setEntry("skladba", audio["TIT2"][0], callFunction=False)
        else:
            app.setEntryDefault("skladba", "Různé hodnoty")
            
        if sameAlbum == len(loadedList):
            app.setEntry("album", audio["TALB"][0], callFunction=False)
        else:
            app.setEntryDefault("album", "Různé hodnoty")
            
        if sameInterpret == len(loadedList):
            app.setEntry("interpret", audio["TPE1"][0], callFunction=False)
        else:
            app.setEntryDefault("interpret", "Různé hodnoty")
        
        if sameRok == len(loadedList):
            app.setEntry("rok", audio["TDRC"][0], callFunction=False)
        else:
            app.setEntryDefault("rok", "Různé hodnoty")
            
        if sameZanr == len(loadedList):
            app.setEntry("zanr", audio["TCON"][0], callFunction=False)
        else:
            app.setEntryDefault("zanr", "Různé hodnoty")
            
        if sameStopa == len(loadedList):
            app.setEntry("stopa", audio["TRCK"][0], callFunction=False)
        else:
            app.setEntryDefault("stopa", "Různé hodnoty")
    
def addFile(btn):       # adds selected file/files to the listbox
    global fPaths
    if app.getEntry("f1")[-4:] == '.mp3': 
            fPath = app.getEntry("f1")
            fName = re.search('^.*[/](.+$)',fPath).group(1) #regex returns the filename
            if fName not in app.getListBox("seznam"):
                app.addListItem("seznam", fName)
                fPaths.append(fPath)
            app.clearEntry("f1", callFunction=False)
    else:
        print("Wrong file, must be an *.mp3")
        
def saveTags(btn):        # saves tags to the file/files
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

    if app.getEntry("f1")[-4:] == '.mp3': 
        path = app.getEntry("f1")
        filename = re.search('^.*[/](.+$)',path).group(1)       #regex returns the filename
        app.setLabel("labelDisplay",filename)       #set the filename to the label that should display it
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
    else:
        print("Wrong file, must be an *.mp3")

app = gui("Tag editor")

app.addLabel("l1", "Skladba:",0,0)
app.addEntry("skladba",0,1,3)

app.addLabel("l2", "Album:",1,0)
app.addEntry("album",1,1,3)

app.addLabel("l3", "Interpret:",2,0)
app.addEntry("interpret",2,1,3)

app.addLabel("l4", "Rok:",3,0)
app.addEntry("rok",3,1,3)

app.addLabel("l5", "Žánr:",4,0)
app.addEntry("zanr",4,1,3)

app.addLabel("l6", "Stopa:",5,0)
app.addEntry("stopa",5,1,3)

app.addLabel("l7", "Obrázek:",6,0)
app.addFileEntry("fCover",6,1,3)

app.addLabel("l8", "Soubor:",7,0)
app.addLabel("labelDisplay", "Žádný soubor nevybrán.",7,1,3)

app.addHorizontalSeparator(8,0,4, colour="black")

app.addFileEntry("f1",9,0,4)
app.addButton("Vymazat", clearFiles,10,0)
app.addButton("Uložit", saveTags,10,1)
app.addButton("Upravit", editTags,10,2)
app.addButton("Načíst", addFile,10,3)

app.addHorizontalSeparator(11,0,4, colour="black")

app.addListBox("seznam", [],12,0,4,4)
app.setListBoxMulti("seznam", multi=True)

app.go()