import time

from isPLC_Package import isPLC

plc = isPLC.ClassCGS_isPLC()

plc.open('COM7')

print(plc.Version)
time.sleep(2)


print(plc.Read_coil('T0'))
print(plc.Read_coil('T19'))





while 0:
    print(plc.Read_coils('X'))

while 0:
    x = 0
    for i in range(0,6):

        plc.Write_coils('Y',0,6,2**i)

    for i in range(6,0,-1):

        plc.Write_coils('Y',0,6,2**i)





