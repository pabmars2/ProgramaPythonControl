from tkinter import *
import logicaEnvio

raiz = Tk()

raiz.title('Controlador debug RISC-V')
raiz.resizable(0, 0)  # niega el redimensionamiento
raiz.iconbitmap('icono.ico')  # determinamos el icono
raiz.geometry('850x650')  # ancho x alto
raiz.config(bg='grey')  # color de fondo

miFrame = Frame()
miFrame.pack(fill='both', expand='True')
miFrame.config(bg='grey')
miFrame.config(width='850', height='650')

serialCOM = None
current_value = StringVar()
debug = IntVar()
opcionLectEscr = IntVar()

ValoresComList = [f'COM{v + 1}' for v in range(256)]

cuadroTexto = Text(miFrame, font=('Sans Serif', 13), width=27, height=25)

botonEnvio = Button(miFrame, text='Enviar', state=DISABLED, width=18, font=('Sans Serif', 13))


puerto = Spinbox(miFrame, values=ValoresComList, textvariable=current_value, justify=RIGHT, font=('Sans Serif', 13))

botonCerrarPuerto = Button(miFrame, text='Cerrar', state=DISABLED, width=8, font=('Sans Serif', 13))


seleccionEscritura1 = Radiobutton(miFrame, text="Memoria instrucciones", state=DISABLED, variable=opcionLectEscr,
                                  value=1, bg='grey', font=('Sans Serif', 13))

seleccionEscritura2 = Radiobutton(miFrame, text="Memoria externa", state=DISABLED, variable=opcionLectEscr,
                                  value=2, bg='grey', font=('Sans Serif', 13))

seleccionLectura1 = Radiobutton(miFrame, text="Memoria instrucciones", state=DISABLED, variable=opcionLectEscr,
                                  value=3, bg='grey', font=('Sans Serif', 13))

seleccionLectura2 = Radiobutton(miFrame, text="Memoria externa", state=DISABLED, variable=opcionLectEscr,
                                  value=4, bg='grey', font=('Sans Serif', 13))


debugCheck = Checkbutton(miFrame, text="Activar modo debug del sistema", variable=debug, state=DISABLED,
                         onvalue=1, offvalue=0, bg='grey', font=('Sans Serif', 13))

botonAbrirPuerto = Button(miFrame, text='Abrir', state=NORMAL, width=8, font=('Sans Serif', 13))

addressExt = Entry(miFrame, font=('Sans Serif', 13), width=13, justify=RIGHT)

dataExt = Entry(miFrame, font=('Sans Serif', 13), width=13, justify=RIGHT)

botonEnvioExt = Button(miFrame, text='Enviar', state=DISABLED,
                    width=5, font=('Sans Serif', 13))

def _cerrarPuerto():
    logicaEnvio.cerrarPuerto(serialCOM)
    controlControles(False)


def controlControles(booleanControl):
    accion = DISABLED
    accionExtra = NORMAL
    if booleanControl:
        accion = NORMAL
        accionExtra = DISABLED

    botonEnvio.config(state=accion)
    botonAbrirPuerto.config(state=accionExtra)
    puerto.config(state=accionExtra)
    botonCerrarPuerto.config(state=accion)
    debugCheck.config(state=accion)

    seleccionEscritura1.config(state=DISABLED)
    seleccionEscritura2.config(state=DISABLED)
    seleccionLectura1.config(state=DISABLED)
    seleccionLectura2.config(state=DISABLED)
    botonEnvioExt.config(state=DISABLED)

    debugCheck.deselect()


def logica():
    global serialCOM
    serialCOM = logicaEnvio.abrirPuerto(current_value.get())
    if serialCOM is None:
        controlControles(False)
    else:
        controlControles(True)


def _enviaDatos():
    logicaEnvio.enviarDatos(serialCOM, cuadroTexto.get(1.0, END))


def _wrInstr():
    logicaEnvio.selec(opcionLectEscr)
    botonEnvio.config(state=NORMAL)
    botonEnvioExt.config(state=DISABLED)


def _wrExt():
    logicaEnvio.selec(opcionLectEscr)
    botonEnvio.config(state=DISABLED)
    botonEnvioExt.config(state=NORMAL)

def _rdInstr():
    botonEnvio.config(state=DISABLED)
    botonEnvioExt.config(state=DISABLED)

def _rdExt():
    botonEnvio.config(state=DISABLED)
    botonEnvioExt.config(state=DISABLED)


def _debugIntrucc():
    logicaEnvio.debugMode(serialCOM, debug)
    if debug.get() == 1:
        seleccionEscritura1.config(state=NORMAL)
        seleccionEscritura2.config(state=NORMAL)
        seleccionLectura1.config(state=NORMAL)
        seleccionLectura2.config(state=NORMAL)
    else:
        seleccionEscritura1.config(state=DISABLED)
        seleccionEscritura2.config(state=DISABLED)
        seleccionLectura1.config(state=DISABLED)
        seleccionLectura2.config(state=DISABLED)


def _sendExt():
    print('Print ext')


botonAbrirPuerto.config(command=logica)
botonCerrarPuerto.config(command=_cerrarPuerto)
botonEnvio.config(command=_enviaDatos)
seleccionEscritura1.config(command=_wrInstr)
seleccionEscritura2.config(command=_wrExt)
debugCheck.config(command=_debugIntrucc)
botonEnvioExt.config(command=_sendExt)
seleccionLectura1.config(command=_rdInstr)
seleccionLectura2.config(command=_rdExt)

logo = PhotoImage(file='logo.gif').subsample(4)
Label(miFrame, image=logo, bg='grey').place(x=750, y=550)
Label(miFrame, text='Inserta el código en hexadecimal', bg='grey', font=('Sans Serif', 13)).place(x=50, y=20)
Label(miFrame, text='Configuración del puerto serie', bg='grey', font=('Sans Serif', 13)).place(x=400, y=20)
Label(miFrame, text='Selecciona el destino a escribir:', bg='grey', font=('Sans Serif', 13)).place(x=400, y=150)
Label(miFrame, text='Dirección:', bg='grey', font=('Sans Serif', 13)).place(x=550, y=250)
Label(miFrame, text='Datos:', bg='grey', font=('Sans Serif', 13)).place(x=550, y=280)
Label(miFrame, text='Selecciona el destino a leer:', bg='grey', font=('Sans Serif', 13)).place(x=400, y=340)

cuadroTexto.place(x=50, y=50)
botonEnvio.place(x=90, y=550)
puerto.place(x=420, y=65)
botonAbrirPuerto.place(x=650, y=60)
botonCerrarPuerto.place(x=750, y=60)
seleccionEscritura1.place(x=450, y=180)
seleccionEscritura2.place(x=450, y=210)
debugCheck.place(x=350, y=110)
addressExt.place(x=610, y=250)
dataExt.place(x=610, y=280)
botonEnvioExt.place(x=760, y=260)
seleccionLectura1.place(x=450, y=370)
seleccionLectura2.place(x=450, y=400)

raiz.mainloop()
