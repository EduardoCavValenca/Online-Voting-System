from tkinter import *
from PIL import ImageTk, Image
import os
from playsound import playsound


# Conexao com servidor
from xmlrpc.client import ServerProxy
proxy = ServerProxy('http://localhost:3000')

##Toca som
def playConfirmSound():
   playsound('SomUrna.mp3')


# Tela
screen=Tk()
screen.geometry("800x600")
screen.title('Urna eletrônica')

# Canvas
backgroundCanvas = Canvas(screen, bg = 'red', width=800, height=600, border=0)
backgroundCanvas.grid(row=1, column=1, padx=0, pady=0)
backgroundCanvas.place(x=0, y=0)

#Fundo
brazil = ImageTk.PhotoImage(file = "Fundo/brazil.png")
brazil_on_canvas = backgroundCanvas.create_image(0, 0, image=brazil, anchor=NW)

background = Label(screen, image = brazil)
background.grid(row=1, column=1, padx=0, pady=0)
background.place(x=0, y=0)

#Confirma
def confirmVote():
    print(proxy.vote(caixaCPF.get("1.0","end-1c"), dropdownDefault.get()))
    playConfirmSound()

confirm = Button(screen, text = 'Confirma', command = confirmVote, padx = 40, pady = 20, justify = "right", bg= '#1E8449', activebackground='#58D68D')
confirm.grid(row=2, column=2, padx= 10, pady=10)
confirm.place(x=600,y=500)



# Carrega as imagens de candidatos
candidatoImages = {}
for filename in os.listdir('Candidatos'):
    candidatoImages[filename.rstrip(".png")] = ImageTk.PhotoImage(Image.open('Candidatos/' + filename).resize((250, 350)))

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
dropdownDefault.set("Candidato") # default value

# Canvas
candidatoCanvas = Canvas(screen, width=250, height=350, border=0)
candidatoCanvas.grid(row=1, column=1, padx=0, pady=0)
candidatoCanvas.place(x=500, y=25)
Misc.lift(candidatoCanvas)

image_on_canvas = candidatoCanvas.create_image(0, 0, image=candidatoImages['Default'], anchor=NW)

def selectImagem(candidato):
    candidatoCanvas.itemconfig(image_on_canvas, image=candidatoImages[candidato])

# Dropdown
dropdown = OptionMenu(screen, dropdownDefault, *Candidatos, command = selectImagem)
dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
dropdown.place(x = 50, y = 50)
dropdown.config(width=15, height=3) 

caixaCPF = Text(screen, height=1, width=11, font=('Arial',24))
caixaCPF.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
caixaCPF.place(x = 100, y = 500)

#canvas.create_text(50, 500, text="CPF: ", fill="white", font=('Arial',24))
#canvas.pack()

# Roda
screen.mainloop()
