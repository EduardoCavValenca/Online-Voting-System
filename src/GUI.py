from tkinter import *
from tkinter import font as tkFont
from PIL import ImageTk, Image
import os
from playsound import playsound


# Conexao com servidor
from xmlrpc.client import ServerProxy
proxy = ServerProxy('http://localhost:3333')

# Tela
screen=Tk()
screen.geometry("800x600")
screen.title('Urna eletrônica')
screen.wm_attributes('-alpha')

# Background
backgroundCanvas = Canvas(screen, bg = 'red', width=800, height=600, border=0)
backgroundCanvas.grid(row=1, column=1, padx=0, pady=0)
backgroundCanvas.place(x=0, y=0)
brazil = ImageTk.PhotoImage(file = "Fundo/Background.png")
brazil_on_canvas = backgroundCanvas.create_image(0, 0, image=brazil, anchor=NW)

# Carrega as imagens de candidatos
candidatoImages = {}
for filename in os.listdir('Candidatos'):
    candidatoImages[filename.rstrip(".png")] = ImageTk.PhotoImage(Image.open('Candidatos/' + filename).resize((250, 350)))

# Imagem dos candidatos
candidatoCanvas = Canvas(screen, width=240, height=320, border=0)
candidatoCanvas.grid(row=1, column=2, padx=0, pady=0)
candidatoCanvas.place(x=488, y=30)
Misc.lift(candidatoCanvas)
image_on_canvas = candidatoCanvas.create_image(0, 0, image=candidatoImages['Default'], anchor=NW)

def selectImagem(candidato):
    candidatoCanvas.itemconfig(image_on_canvas, image=candidatoImages[candidato])

# Dropdown
Candidatos = [
    "Alessandro", 
    "Bruno", 
    "Che",
    "Eduardo",
    "Branco",
    "Nulo"
]
dropdownDefault = StringVar(screen)
dropdownDefault.set("Candidato")
dropdown = OptionMenu(screen, dropdownDefault, *Candidatos, command = selectImagem)
dropdown.grid(row=1, column=1, sticky="ew")
dropdown.place(x = 55, y = 26)
dropdown.config(width=10, height=2, font=('Arial',18)) 
helv20 = tkFont.Font(family='Arial', size=21)
menu = screen.nametowidget(dropdown.menuname)
menu.config(font=helv20)  # Set the dropdown menu's font

# Caixa para CPF
caixaCPF = Text(screen, height=1, width=11, font=('Arial',20), padx=10, pady=12)
caixaCPF.grid(row=2, column=1, padx=0, pady=0, sticky="ew")
caixaCPF.place(x = 50, y = 497)

# Botao de confirma
def confirmVote():
    str = proxy.vote(caixaCPF.get("1.0","end-1c"), dropdownDefault.get())
    print(str)
    if(str == 'Vote added'):
        playsound('SoundEffects/SomUrna.mp3')

confirm = Button(screen, text = 'Confirma', command = confirmVote, width=16, height=3, fg='white', border=5, padx = 0, pady = 0, justify = "right", bg= '#1E8449', activebackground='#58D68D', font=('Arial',18))
confirm.grid(row=2, column=2, padx= 10, pady=10)
confirm.place(x=485,y=455)



# Roda
screen.mainloop()
