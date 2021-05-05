from tkinter import messagebox
import serial
from serial.serialutil import SerialException


def enviarDatos(serialCOM,pepe):
    print(pepe[:-1])
    print('eviar')


def abrirPuerto(indice):
    try:
        ser = serial.Serial(
            port=indice,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        messagebox.showinfo('Información', 'Puerto ' + indice + ' abierto correctamente!')
        return ser
    except SerialException:
        messagebox.showerror('ERROR', 'Error al abrir el puerto ' + indice + ' !')


def cerrarPuerto(serial):
    try:
        serial.close()
        messagebox.showinfo('Información', 'Puerto cerrado correctamente!')
    except AttributeError:
        messagebox.showerror('ERROR', 'Error al cerrar el puerto!')


def selec(opcion):
    print(opcion.get())


def debugMode(serialCOM, debug):
    if debug:
        thestring = b'\x00\x00\x00\x00\x00'
        serialCOM.write(thestring)
    else:
        thestring = b'\x01\x00\x00\x00\x00'
        serialCOM.write(thestring)
