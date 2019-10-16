import time

from isPLC_Package import isPLC


#import serial.tools.list_ports;
#print([comport.device for comport in serial.tools.list_ports.comports()])
#input()

plc = isPLC.ClassCGS_isPLC()

plc.open('COM3')

print(plc.Version)
time.sleep(4)
plc.
while 1:
    for i in range(513):
        plc.Write_Register(0,i*2)
        print(plc.ReadRegister(0))


while 0:
    print(plc.Read_coils('X'))

while 0:
    x = 0
    for i in range(0,6):
        print( plc.Write_coils('S',0,6,2**i) )
        plc.Write_coils('Y',0,6,2**i)

    for i in range(6,0,-1):

        plc.Write_coils('Y',0,6,2**i)





