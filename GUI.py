from tkinter import *
from PIL import ImageTk, Image
import os

# Conexao com servidor
from xmlrpc.client import ServerProxy
proxy = ServerProxy('http://localhost:3001')

# Tela
screen=Tk()
screen.geometry("800x600")
screen.title('Urna eletrônica')

#Fundo
brazil = ImageTk.PhotoImage(Image.open("Candidatos/brazil.png"))
background = Label(screen, image = brazil)
background.grid(row=1, column=1, padx=0, pady=0)
background.place(x=0, y=0)

#Confirma
def confirmVote():
    print(proxy.vote(caixaCPF.get("1.0","end-1c"), dropdownDefault.get()))

confirm = Button(screen, text = 'Confirma', command = confirmVote, padx = 40, pady = 20, justify = "right", bg= '#1E8449', activebackground='#58D68D')
confirm.grid(row=2, column=2, padx= 10, pady=10)
confirm.place(x=600,y=500)


# Dropdown
Candidatos = [
    "Bruno da mola", 
    "Zuckerberg", 
    "Rodolfo Ipolito",
    "Branco",
    "Nulo"
]

dropdownDefault = StringVar(screen)
dropdownDefault.set("Candidato") # default value

#Resize the Image using resize method
img = Image.open("Candidatos/default.png")
img= img.resize((400,350), Image.ANTIALIAS)

# Imagem candidato
img = ImageTk.PhotoImage(img)
panel = Label(screen, image = img)
panel.grid(row=1, column=2, padx=10, pady=10)
panel.place(x=300, y=20)

def selectImagem(candidato):
    img = Image.open("Candidatos/" + candidato.replace(" ", "") + ".png")
    img = img.resize((450,350), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel.configure(image=img)
    panel.image = img
    

# Dropdown
dropdown = OptionMenu(screen, dropdownDefault, *Candidatos, command = selectImagem)
dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
dropdown.place(x = 50, y = 50)
dropdown.config(width=15, height=3) 

caixaCPF = Text(screen, height=2, width=10)
caixaCPF.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
caixaCPF.place(x = 50, y = 500)

# Roda
screen.mainloop()
