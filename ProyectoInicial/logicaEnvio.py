from tkinter import messagebox
import serial
from serial.serialutil import SerialException


def enviarDatos(serialCOM, datos, registro):
    for i in range(7, -1, -2):
        cod = datos[i - 1:i + 1]
        cod = bytearray.fromhex(cod)
        serialCOM.write(cod)

    if registro == 0:
        thestring = b'\x00'
        serialCOM.write(thestring)

    if registro == 1:
        thestring = b'\x01'
        serialCOM.write(thestring)

    if registro == 2:
        thestring = b'\x02'
        serialCOM.write(thestring)


def abrirPuerto(indice):
    try:
        ser = serial.Serial(
            port=indice,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=2
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


def enviarExt(serialCOM, addressExt, dataExt):
    if (len(addressExt) != 8) | (len(dataExt) != 8):
        messagebox.showerror('ERROR', 'Longitud incorrecta, solo permitido 8 bytes.')
    else:
        enviarDatos(serialCOM, addressExt, 1)
        enviarDatos(serialCOM, dataExt, 2)

        thestring = b'\x31\x00\x00\x00\x00'
        serialCOM.write(thestring)
        thestring = b'\x01\x00\x00\x00\x00'
        serialCOM.write(thestring)

        messagebox.showinfo('Información', 'Datos enviados correctamente!')



def debugMode(serialCOM, debug):
    if debug:
        thestring = b'\x01\x00\x00\x00\x00'
        serialCOM.write(thestring)
    else:
        thestring = b'\x00\x00\x00\x00\x00'
        serialCOM.write(thestring)


def ejecSteps(serialCOM, stateSteps, numSteps):
    if stateSteps:
        if numSteps == 1:
            thestring = b'\x0d\x00\x00\x01\x00'
            serialCOM.write(thestring)

        if numSteps == 2:
            thestring = b'\x0d\x00\x00\x02\x00'
            serialCOM.write(thestring)

        if numSteps == 3:
            thestring = b'\x0d\x00\x00\x03\x00'
            serialCOM.write(thestring)

        if numSteps == 4:
            thestring = b'\x0d\x00\x00\x04\x00'
            serialCOM.write(thestring)

        if numSteps == 5:
            thestring = b'\x0d\x00\x00\x05\x00'
            serialCOM.write(thestring)

        if numSteps == 6:
            thestring = b'\x0d\x00\x00\x06\x00'
            serialCOM.write(thestring)

        if numSteps == 7:
            thestring = b'\x0d\x00\x00\x07\x00'
            serialCOM.write(thestring)

        if numSteps == 8:
            thestring = b'\x0d\x00\x00\x08\x00'
            serialCOM.write(thestring)

        if numSteps == 9:
            thestring = b'\x0d\x00\x00\x09\x00'
            serialCOM.write(thestring)

        if numSteps == 10:
            thestring = b'\x0d\x00\x00\x0a\x00'
            serialCOM.write(thestring)

        messagebox.showinfo('Información', 'Ejecutando ' + numSteps + ' pasos en el sistema!')
    #else:
     #   thestring = b'\x01\x00\x00\x00\x00'
      #  serialCOM.write(thestring)


def recibirDatos(serialCOM, address, nData, tipo):
    datos = ''
    if len(address) != 8 :
        messagebox.showerror('ERROR', 'Longitud incorrecta, solo permitido 8 bytes.')
    else:
        addressToSend = address

        for i in range(int(nData)):
            enviarDatos(serialCOM, addressToSend, 1)
            addressToSend = int(addressToSend, 16)
            addressToSend = addressToSend + 4
            addressToSend = hex(addressToSend)
            addressToSend = addressToSend[2:]

            if tipo == 0:
                thestring = b'\x21\x00\x00\x00\x00'
                serialCOM.write(thestring)
                thestring = b'\x01\x00\x00\x00\x00'
                serialCOM.write(thestring)
            if tipo == 1:
                thestring = b'\x11\x00\x00\x00\x00'
                serialCOM.write(thestring)
                thestring = b'\x01\x00\x00\x00\x00'
                serialCOM.write(thestring)

            recepcion = serialCOM.read(4)

            if recepcion == b'' :
                messagebox.showerror('ERROR', 'Error al recibir datos.')
            else:
                datos = recepcion

        return datos

def readPC(serialCOM, tipo):
    datos = ''

    if tipo == 0:
        thestring = b'\x51\x00\x00\x00\x00'
        serialCOM.write(thestring)
        thestring = b'\x01\x00\x00\x00\x00'
        serialCOM.write(thestring)
    if tipo == 1:
        thestring = b'\x61\x00\x00\x00\x00'
        serialCOM.write(thestring)
        thestring = b'\x01\x00\x00\x00\x00'
        serialCOM.write(thestring)

    recepcion = serialCOM.read(4)

    if recepcion == b'':
        messagebox.showerror('ERROR', 'Error al recibir datos.')
    else:
        datos = recepcion


    return datos

def enviarDatosInstr(serialCOM, data):
    address = '00000000'
    addressToSend = address
    error = False

    for datos in data:

        if len(datos) != 8 :
            messagebox.showerror('ERROR', 'Longitud incorrecta, solo permitido 8 bytes.')
            error = True
        else:
            enviarDatos(serialCOM, datos, 2)
            enviarDatos(serialCOM, addressToSend, 1)

            addressToSend = int(addressToSend, 16)
            addressToSend = addressToSend + 4
            addressToSend = hex(addressToSend)
            addressToSend = addressToSend[2:]

            if len(addressToSend) < 8 :
                for i in range(8-len(addressToSend)):
                    addressToSend = '0' + addressToSend

            thestring = b'\x41\x00\x00\x00\x00'
            serialCOM.write(thestring)
            thestring = b'\x01\x00\x00\x00\x00'
            serialCOM.write(thestring)
            thestring = b'\x01\x01\x00\x00\x00'
            serialCOM.write(thestring)
            thestring = b'\x01\x00\x00\x00\x00'
            serialCOM.write(thestring)


    if not error:
        messagebox.showinfo('Información', 'Datos enviados correctamente!')


