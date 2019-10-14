import time

from isPLC_Package import isPLC

plc = isPLC.ClassCGS_isPLC()

plc.open('COM3')

print(plc.Version)
time.sleep(1)
while True:
    print(plc.Read_coil('X0'),plc.Read_coil('X1'),plc.Read_coil('X2'),plc.Read_coil('X3'),plc.Read_coil('X4'),plc.Read_coil('X5'))





