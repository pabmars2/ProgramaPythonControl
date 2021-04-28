import serial

ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

print(ser.isOpen())

with open('data.txt', 'rb') as f:
    for l in f:
        l = l[:-2]
        for i in range(9, -1, -2):
            cod = l[i-1:i+1]
            cod = cod.decode()
            cod = bytearray.fromhex(cod)
            ser.write(cod)

#ser.write()
#thestring = b'\x7E\xFF\x03\x00\x01\x00\x02\x0A\x01\xC8\x04\xD0\x01\x02\x80\x00\x00\x00\x00\x8E\xE7\x7E'
#ser.write(thestring)

# s = ser.read(1)
# print(s)
ser.close()
