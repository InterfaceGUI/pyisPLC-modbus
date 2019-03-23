try:

    import serial

except ImportError:

    from pip._internal import main as pip
    pip(['install', '--user', 'pyserial'])
    import serial

try:

    import crcmod

except ImportError:

    from pip._internal import main as pip
    pip(['install', '--user', 'crcmod'])
    import crcmod

import time
import sys
import math


def crc(byte):
    ''' 
    crc(bytes([0x1,0x11])) == 192,44
    '''
    # ['modbus','CrcModbus',0x18005,REVERSE,0xFFFF,0x0000,0x4B37]
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    cr = crc16(byte)
    re = str(hex(cr)).replace("0x", '').upper()[:2]
    re2 = str(hex(cr)).replace("0x", '').upper()[2:]
    return str(int(re2, base=16))+','+str(int(re, base=16))


def byteTObin(n):
    return str(bin(int(n))).replace('0b', '').zfill(8)


def reverse(s):
    '''反轉字串'''
    out = ''
    for i in s:
        out = i + out
    return out


class ClassCGS_isPLC():
    '''ID 為設備ID'''

    def __init__(self, ID=0x01):
        self.Version = '請使用isPLC核心，或重新更新韌體。'
        global ID0
        ID0 = ID

    def open(self, Port):
        '''開啟新的序列埠連線。'''
        global ser

        ser = serial.Serial(Port, baudrate=38400,
                            stopbits=1, timeout=1, bytesize=8, parity='N')
        time.sleep(0)
        for i in range(1, 30):

            time.sleep(1)
            ser.write(bytes([ID0, 17, 192, 44]))
            time.sleep(0.05)

            if not ser.readable():
                continue

            try:
                mes = str()
                r = ser.read(8)
                if r == b'':
                    continue

                for i in r:
                    mes = mes + str(i) + ','
                mes = mes.split(',')
                if mes[3] == '255':
                    self.Version = ''
                    msg = ''
                    for i in mes[4:-1]:
                        msg = msg + i + '.'
                    self.Version = msg[:-1]
                    break
                ser.read_all()
            except Exception as e:
                print(str(e))
        else:
            raise RuntimeError('無法連接')

    def close(self):
        '''關閉連線。'''
        try:
            ser.close()
        except:
            pass

    def Read_coil(self, Element):
        '''
        `Element` 為元件，
        回傳 int (`0` or `1`)\n
        { Y、X、M、T、S、C }\n\n
        用法；\n
        取得 `Y5`狀態\n
        `Read_coil('Y5')`
        '''

        if Element[:1] == 'Y':
            ra = Read_ALL_coil().readY()
            return int(ra[int(Element[1:])])
        if Element[:1] == 'X':
            ra = Read_ALL_coil().readX()
            return int(ra[int(Element[1:])])
        if Element[:1] == 'M':
            ra = Read_ALL_coil().readM(int(Element[1:]))
            return int(ra[int(Element[1:])%8])
        if Element[:1] == 'T':
            ra = Read_ALL_coil().readT()
            return int(ra[int(Element[1:])])

    def Read_coils(self, Elements):
        '''
        `Element` 為元件，
        回傳 int [0,1,0,1]\n
        { Y、X、M、T、S、C }\n\n
        用法；\n
        取得 `Y0`、`Y1`、`Y2`狀態\n
        `Read_coil(['Y','0','1','2'])`
        '''

        if Elements[0] == 'Y':
            ra = Read_ALL_coil().readY()
            listitem = []
            for i in Elements[1:]:
                listitem.append(int(ra[int(i)]))
            return listitem

        if Elements[0] == 'M':
            listitem = []
            
            for i in Elements[1:]:
                ra = Read_ALL_coil().readM(int(i))
                listitem.append(int(ra[int(i)%8]))
            return listitem

# 內部傳送 讀取線圈區塊


class Read_ALL_coil():
    # bytes(ID , Func_code , E, E, E, E, CRC {H} , CRC {L} ])
    ##########################################################################
    def readY(self):
        crcs = crc(bytes([ID0, 1, 5, 0, 0, 6])).split(',')  # 取得CRC16
        ser.write(
            bytes([ID0, 1, 5, 0, 0, 6, int(crcs[0]), int(crcs[1])]))  # 傳送資料
        time.sleep(0.0005)  # 等0.5ms 等到isplc回應

        r = ser.read(6)  # 讀取後6個byte
        data = ''

        for i in r:
            data = data + str(i) + ','
        res = data[:-1].split(',')
        ret = ''
        # 顛倒排序
        for i in str(bin(int(res[3]))).replace('0b', '').zfill(6):
            ret = i + ret
        return ret
    ##########################################################################

    def readX(self):
        crcs = crc(bytes([ID0, 2, 4, 0, 0, 6])).split(',')
        ser.write(bytes([ID0, 2, 4, 0, 0, 6, int(crcs[0]), int(crcs[1])]))
        time.sleep(0.05)

        r = ser.read(6)
        data = ''

        for i in r:
            data = data + str(i) + ','
        res = data[:-1].split(',')
        ret = ''
        # 顛倒排序
        for i in str(bin(int(res[3]))).replace('0b', '').zfill(6):
            ret = i + ret
        return ret
    ##########################################################################
# 0  1  2  3  4  5  6  7
# 8  9  10 11 12 13 14 15
# 16 17 18 19 20 21 22 23
# 24 25 26 27 28 29 30 31
# 32 33 34 35 36 37 38 39
# 40 41 42 43 44 45 46 47
# 48 49

    def readM(self,num):
        # 0~15
        OutCoil = ''
        ReturnOutCoil = ''

        # ---------------------------------
        Em = [0, 8, 16, 24, 32, 40, 48]
        rrr = ser.read_all()

        if num <=7:

            crcs = crc(bytes([ID0, 1, 8, 0, 0, 8])).split(',')
                # 傳送資料 格式為bytes([ID, func, 元件,位置, 讀取元,件數量, CRC`H`, CRC`L`)])
            ser.write(
                bytes([ID0, 1, 8, 0, 0, 8, int(crcs[0]), int(crcs[1])]))


        if num >= 8 and num <= 15:
            crcs = crc(bytes([ID0, 1, 8, 8, 0, 8])).split(',')
                # 傳送資料 格式為bytes([ID, func, 元件,位置, 讀取元,件數量, CRC`H`, CRC`L`)])
            ser.write(
                bytes([ID0, 1, 8,8, 0, 8, int(crcs[0]), int(crcs[1])]))

        if num >= 16 and num <=23 :
            crcs = crc(bytes([ID0, 1, 8, 16, 0, 8])).split(',')
                # 傳送資料 格式為bytes([ID, func, 元件,位置, 讀取元,件數量, CRC`H`, CRC`L`)])
            ser.write(
                bytes([ID0, 1, 8, 16, 0, 8, int(crcs[0]), int(crcs[1])]))

        if num >= 24 and num <=31 :
            crcs = crc(bytes([ID0, 1, 8, 24, 0, 8])).split(',')
                # 傳送資料 格式為bytes([ID, func, 元件,位置, 讀取元,件數量, CRC`H`, CRC`L`)])
            ser.write(
                bytes([ID0, 1, 8, 24, 0, 8, int(crcs[0]), int(crcs[1])]))

        if num >=32 and num <=39 :
            crcs = crc(bytes([ID0, 1, 8, 32, 0, 8])).split(',')
                # 傳送資料 格式為bytes([ID, func, 元件,位置, 讀取元,件數量, CRC`H`, CRC`L`)])
            ser.write(
                bytes([ID0, 1, 8, 32, 0, 8, int(crcs[0]), int(crcs[1])]))

        if num >=40 and num <= 47:
            crcs = crc(bytes([ID0, 1, 8, 40, 0, 8])).split(',')
                # 傳送資料 格式為bytes([ID, func, 元件,位置, 讀取元,件數量, CRC`H`, CRC`L`)])
            ser.write(
                bytes([ID0, 1, 8, 40, 0, 8, int(crcs[0]), int(crcs[1])]))

        if num >=48 and num <= 49:
                crcs = crc(bytes([ID0, 1, 8, 48, 0, 8])).split(',')
                # 傳送資料 格式為bytes([ID, func, 元件,位置, 讀取元,件數量, CRC`H`, CRC`L`)])
                ser.write(
                    bytes([ID0, 1, 8, 48, 0, 8, int(crcs[0]), int(crcs[1])]))

        r = ser.read(7)
        rrr = ser.read_all()
        data = ''
        for i in r:
            data = data + str(i) + ','
        res = data[:-1].split(',')

        if num >= 48:
            OutCoil += str(bin(int(res[3]))).replace('0b', '').zfill(2)[::-1]
        else:
            OutCoil += str(byteTObin(res[3]))[::-1]
        return OutCoil
    ##########################################################################

    def readT(self):
        ret = ''
        OutCoil = ''
        ReturnOutCoil = ''

        Em = [0, 10]
        for ci in range(2):
            # 計算CR
            crcs = crc(bytes([ID0, 1, 6, Em[ci], 0, 10])).split(',')
            # 傳送資料 格式為bytes([ID, func, 元件,位置, 讀取元,件數量, CRC`H`, CRC`L`)])
            ser.write(
                bytes([ID0, 1, 6, Em[ci], 0, 10, int(crcs[0]), int(crcs[1])]))

            time.sleep(0.05)
            r = ser.read(7)
            rrr = ser.read_all()
            c = 0
            data = ''
            for i in r:
                data = data + str(i) + ','
            res = data[:-1].split(',')

            ret = str(bin(int(res[4]))).replace('0b', '').zfill(2)
            if res[4] == '4':
                OutCoil = ret[1:]
            else:
                OutCoil = ret

            OutCoil = OutCoil + byteTObin(res[3])
            ReturnOutCoil = OutCoil + ReturnOutCoil

        pass
        return reverse(ReturnOutCoil)

    ##########################################################################
