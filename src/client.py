from tkinter import *
from tkinter import font as tkFont
from PIL import ImageTk, Image
import os
from playsound import playsound
from tkinter.messagebox import showinfo

# Server connection
from xmlrpc.client import ServerProxy
proxy = ServerProxy('http://localhost:3333')

# Main screen
screen=Tk()
screenRes = 200
screenResX, screenResY = screenRes*4, screenRes*3
screen.geometry(str(screenResX) + 'x' + str(screenResY))
screen.title('Eletronic ballot box')
screen.resizable = (False, False)

# Background
backgroundCanvas = Canvas(screen, width=screenResX, height=screenResY, border=0)
backgroundCanvas.grid(row=1, column=1, padx=0, pady=0)
backgroundCanvas.place(x=0, y=0)
background = ImageTk.PhotoImage(Image.open("Background/Background.png").resize((screenResX, screenResY)))
background_on_canvas = backgroundCanvas.create_image(0, 0, image=background, anchor=NW)

# Load candidates images
candidates = proxy.getCandidates()
candidateImages = {}
candidateImages['Default'] = ImageTk.PhotoImage(Image.open('Candidates/Default.png').resize((int(screenResX*5/16), int(screenResX*5/16 * 4/3))))
for candidate in candidates:
    try:
        candidateImages[candidate] = ImageTk.PhotoImage(Image.open('Candidates/' + candidate + '.png').resize((int(screenResX*5/16), int(screenResX*5/16 * 4/3))))
    except FileNotFoundError:
        candidateImages[candidate] = None

# Display candidates images
candidateCanvas = Canvas(screen, width=screenResX*3/10, height=screenResY*8/15, border=0)
candidateCanvas.grid(row=1, column=2, padx=0, pady=0)
candidateCanvas.place(x=screenResX*3/5, y=screenResY/20)
Misc.lift(candidateCanvas)
curCandidateImage = candidateCanvas.create_image(0, 0, image=candidateImages['Default'], anchor=NW)

def selectImagem(candidate):
    candidateCanvas.itemconfig(curCandidateImage, image=candidateImages[candidate])

# Dropdown
dropdownCurOption = StringVar(screen)
dropdownCurOption.set("Candidate")
dropdown = OptionMenu(screen, dropdownCurOption, *candidates, command = selectImagem)
dropdown.grid(row=1, column=1, sticky="ew")
dropdown.place(x = screenResX/16, y = screenResY/24)
dropdown.config(width=11, height=2, font=('Helvetica', int(20*screenRes/200)))  
menu = screen.nametowidget(dropdown.menuname)
menu.config(font=tkFont.Font(family='Helvetica', size=int(26*screenRes/200)))

# Input box to get the voter's ID
inputBoxID = Text(screen, height=1, width=11, font=('Helvetica', int(20*screenRes/200)), padx=10, pady=12)
inputBoxID.grid(row=2, column=1, padx=0, pady=0, sticky="ew")
inputBoxID.place(x = screenResX/16, y = screenResY*5/6)

# confirm button
def confirmVote():
    str = proxy.vote(inputBoxID.get("1.0","end-1c"), dropdownCurOption.get())
    if(str == 'Vote added'):
        playsound('SoundEffects/SomUrna.mp3')
    showinfo("Info", str)
    dropdownCurOption.set("Candidate")
    selectImagem("Default")
    inputBoxID.delete('1.0', END)

confirm = Button(screen, text = 'Confirm', command = confirmVote, width=16, height=3, fg='white', border=5, padx = 0, pady = 0, justify = "right", bg= '#1E8449', activebackground='#58D68D', font=('Helvetica', int(18*screenRes/200)))
confirm.grid(row=2, column=2, padx= 10, pady=10)
confirm.place(x=screenResX*3/5, y=screenResY*4/5)

def on_closing():
    result = proxy.getResult()
    resultStr = ""
    for candidate in result:
        resultStr += candidate['name'] + ":        \t" + str(candidate['votes']) + '\n'
    showinfo("Resultado", resultStr)
    screen.destroy()

screen.protocol("WM_DELETE_WINDOW", on_closing)

# run
screen.mainloop()
