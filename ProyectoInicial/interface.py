from tkinter import *
import logicaEnvio

raiz = Tk()

raiz.title('Controlador debug RISC-V')
raiz.resizable(0,0)     #niega el redimensionamiento
raiz.iconbitmap('icono.ico')    #determinamos el icono
raiz.geometry('850x650')    #ancho x alto
raiz.config(bg='grey')  #color de fondo

miFrame = Frame()
miFrame.pack(fill='both', expand='True')
miFrame.config(bg='grey')
miFrame.config(width='850', height='650')

logo = PhotoImage(file='logo.gif').subsample(4)
Label(miFrame, image=logo, bg='grey').place(x=750, y=550)

Label(miFrame, text='Inserta el código en hexadecimal', bg='grey', font=('Sans Serif', 13)).place(x=50, y=20)

cuadroTexto = Text(miFrame, font=('Sans Serif', 13), width=27, height=25)
cuadroTexto.place(x=50, y=50)

botonEnvio = Button(miFrame, text='Enviar', command=logicaEnvio.enviarDatos, width=18, font=('Sans Serif', 13)).place(x=90, y=550)



raiz.mainloop()