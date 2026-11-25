import serial

baud = 9600
ser = serial.Serial("COM10", baud) 

while True:
    ser.write('0')
