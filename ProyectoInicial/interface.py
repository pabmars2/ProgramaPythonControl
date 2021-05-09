import tkinter
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

newWindow = miFrame
flagNewWindow = False
serialCOM = None
current_value = StringVar()
current_value_addr = StringVar()
nSteps = StringVar()
debug = IntVar()
step = IntVar()
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

seleccionLecturaPC = Radiobutton(miFrame, text="PC actual y próximo:", state=DISABLED, variable=opcionLectEscr,
                                 value=5, bg='grey', font=('Sans Serif', 13))

debugCheck = Checkbutton(miFrame, text="Activar modo debug del sistema", variable=debug, state=DISABLED,
                         onvalue=1, offvalue=0, bg='grey', font=('Sans Serif', 13))

steps = Checkbutton(miFrame, text="Activar modo ejecución por pasos", variable=step, state=DISABLED,
                    onvalue=1, offvalue=0, bg='grey', font=('Sans Serif', 13))

botonAbrirPuerto = Button(miFrame, text='Abrir', state=NORMAL, width=8, font=('Sans Serif', 13))

addressExt = Entry(miFrame, font=('Sans Serif', 13), width=13, justify=RIGHT)

dataExt = Entry(miFrame, font=('Sans Serif', 13), width=13, justify=RIGHT)

botonEnvioExt = Button(miFrame, text='Enviar', state=DISABLED,
                       width=5, font=('Sans Serif', 13))

initialAddress = Entry(miFrame, font=('Sans Serif', 13), width=13, justify=RIGHT)

numAdresses = Spinbox(miFrame, from_=1, to=10, textvariable=current_value_addr, justify=RIGHT, font=('Sans Serif', 13))

numSteps = Spinbox(miFrame, from_=1, to=10, textvariable=nSteps, justify=RIGHT, width=5, font=('Sans Serif', 13))

botonRx = Button(miFrame, text='Recibir datos', state=DISABLED,
                 font=('Sans Serif', 13))


def _cerrarPuerto():
    logicaEnvio.cerrarPuerto(serialCOM)
    controlControles(False)


def controlControles(booleanControl):
    accion = DISABLED
    accionExtra = NORMAL
    if booleanControl:
        accion = NORMAL
        accionExtra = DISABLED

    botonEnvio.config(state=DISABLED)
    botonAbrirPuerto.config(state=accionExtra)
    puerto.config(state=accionExtra)
    botonCerrarPuerto.config(state=accion)
    debugCheck.config(state=accion)
    steps.config(state=accion)

    seleccionEscritura1.config(state=DISABLED)
    seleccionEscritura2.config(state=DISABLED)
    seleccionLectura1.config(state=DISABLED)
    seleccionLectura2.config(state=DISABLED)
    seleccionLecturaPC.config(state=DISABLED)
    botonEnvioExt.config(state=DISABLED)
    botonRx.config(state=DISABLED)

    debugCheck.deselect()
    steps.deselect()


def logica():
    global serialCOM
    serialCOM = logicaEnvio.abrirPuerto(current_value.get())
    if serialCOM is None:
        controlControles(False)
    else:
        controlControles(True)


def _enviaDatos():
    datos = cuadroTexto.get(1.0, END)
    datos_aux = ''
    datos_salida = list()
    for i in range(len(datos)):
        cod = datos[i:i + 1]

        if cod != '\n':
            datos_aux = datos_aux + cod
        else:
            datos_salida.append(datos_aux)
            datos_aux = ''

    logicaEnvio.enviarDatosInstr(serialCOM, datos_salida)


def _wrInstr():
    botonEnvio.config(state=NORMAL)
    botonEnvioExt.config(state=DISABLED)
    botonRx.config(state=DISABLED)


def _wrExt():
    botonEnvio.config(state=DISABLED)
    botonEnvioExt.config(state=NORMAL)
    botonRx.config(state=DISABLED)


def _newWindow():
    global newWindow
    newWindow = tkinter.Toplevel(raiz)
    newWindow.title('Datos recibidos')
    newWindow.resizable(0, 0)  # niega el redimensionamiento
    newWindow.iconbitmap('icono.ico')  # determinamos el icono
    newWindow.geometry('400x400')  # ancho x alto
    newWindow.config(bg='grey')  # color de fondo
    Label(newWindow, text='Numero de direcciones:', bg='grey', font=('Sans Serif', 13)).place(x=100, y=100)



def _rdInstr():
    botonEnvio.config(state=DISABLED)
    botonEnvioExt.config(state=DISABLED)
    botonRx.config(state=NORMAL)


def _rdExt():
    botonEnvio.config(state=DISABLED)
    botonEnvioExt.config(state=DISABLED)
    botonRx.config(state=NORMAL)


def _debugIntrucc():
    logicaEnvio.debugMode(serialCOM, debug.get())
    if debug.get() == 1:
        seleccionEscritura1.config(state=NORMAL)
        seleccionEscritura2.config(state=NORMAL)
        seleccionLectura1.config(state=NORMAL)
        seleccionLectura2.config(state=NORMAL)
        seleccionLecturaPC.config(state=NORMAL)
    else:
        seleccionEscritura1.config(state=DISABLED)
        seleccionEscritura2.config(state=DISABLED)
        seleccionLectura1.config(state=DISABLED)
        seleccionLectura2.config(state=DISABLED)
        seleccionLecturaPC.config(state=DISABLED)


def _sendExt():
    logicaEnvio.enviarExt(serialCOM, addressExt.get(), dataExt.get())


def _rdPC():
    global flagNewWindow

    if flagNewWindow:
        newWindow.destroy()
        flagNewWindow = False

    if not flagNewWindow:
        _newWindow()
        flagNewWindow = True

    botonEnvio.config(state=DISABLED)
    botonEnvioExt.config(state=DISABLED)
    botonRx.config(state=DISABLED)

    PCActual = logicaEnvio.readPC(serialCOM, 0)

    PCSiguiente = logicaEnvio.readPC(serialCOM, 1)


def _rx():
    global flagNewWindow

    datos = logicaEnvio.recibirDatos(serialCOM, initialAddress.get(), current_value_addr.get(),
                                     opcionLectEscr.get() - 3)

    if flagNewWindow:
        newWindow.destroy()
        flagNewWindow = False

    if not flagNewWindow:
        _newWindow()
        flagNewWindow = True


def _steps():
    logicaEnvio.ejecSteps(serialCOM, step.get(), nSteps.get())
    steps.deselect()


botonAbrirPuerto.config(command=logica)
botonCerrarPuerto.config(command=_cerrarPuerto)
botonEnvio.config(command=_enviaDatos)
seleccionEscritura1.config(command=_wrInstr)
seleccionEscritura2.config(command=_wrExt)
debugCheck.config(command=_debugIntrucc)
botonEnvioExt.config(command=_sendExt)
seleccionLectura1.config(command=_rdInstr)
seleccionLectura2.config(command=_rdExt)
seleccionLecturaPC.config(command=_rdPC)
botonRx.config(command=_rx)
steps.config(command=_steps)

logo = PhotoImage(file='logo.gif').subsample(4)
Label(miFrame, image=logo, bg='grey').place(x=750, y=550)
Label(miFrame, text='Inserta el código en hexadecimal', bg='grey', font=('Sans Serif', 13)).place(x=50, y=20)
Label(miFrame, text='Configuración del puerto serie', bg='grey', font=('Sans Serif', 13)).place(x=400, y=20)
Label(miFrame, text='Selecciona el destino a escribir:', bg='grey', font=('Sans Serif', 13)).place(x=400, y=150)
Label(miFrame, text='Dirección:', bg='grey', font=('Sans Serif', 13)).place(x=550, y=250)
Label(miFrame, text='Datos:', bg='grey', font=('Sans Serif', 13)).place(x=550, y=280)
Label(miFrame, text='Selecciona el destino a leer:', bg='grey', font=('Sans Serif', 13)).place(x=400, y=340)
Label(miFrame, text='Dirección inicial:', bg='grey', font=('Sans Serif', 13)).place(x=550, y=440)
Label(miFrame, text='Numero de direcciones:', bg='grey', font=('Sans Serif', 13)).place(x=550, y=470)

cuadroTexto.place(x=50, y=50)
botonEnvio.place(x=90, y=550)
puerto.place(x=420, y=65)
botonAbrirPuerto.place(x=650, y=60)
botonCerrarPuerto.place(x=750, y=60)
seleccionEscritura1.place(x=450, y=180)
seleccionEscritura2.place(x=450, y=210)
debugCheck.place(x=350, y=110)
steps.place(x=350, y=590)
addressExt.place(x=610, y=250)
dataExt.place(x=610, y=280)
botonEnvioExt.place(x=760, y=260)
seleccionLectura1.place(x=450, y=370)
seleccionLectura2.place(x=450, y=400)
seleccionLecturaPC.place(x=450, y=550)
initialAddress.place(x=675, y=440)
numAdresses.place(x=600, y=470)
botonRx.place(x=690, y=510)
numSteps.place(x=650, y=595)

raiz.mainloop()
