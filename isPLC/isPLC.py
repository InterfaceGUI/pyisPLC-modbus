import serial
import time
import crcmod
import sys


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
                            stopbits=1, bytesize=8, parity='N')

        time.sleep(10)
        ser.write(bytes([ID0, 17, 192, 44]))
        time.sleep(0.05)
        mes = str()
        try:
            r = ser.read(8)
            for i in r:
                mes = mes + str(i) + ','
            mes = mes.split(',')
            if mes[3] == '255':
                self.Version = ''
                msg = ''
                for i in mes[4:-1]:
                    msg = msg + i + '.'
                self.Version = msg[:-1]
            ser.read_all()
        except Exception as e:
            pass

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
            ra = Read_ALL_coil().readM()
            return int(ra[int(Element[1:])])
        if Element[:1] == 'T':
            ra = Read_ALL_coil().readT()
            return int(ra[int(Element[1:])])

# 內部傳送 讀取線圈區塊


class Read_ALL_coil():
    # bytes(ID , Func_code , E, E, E, E, CRC {H} , CRC {L} ])
    ##########################################################################
    def readY(self):
        crcs = crc(bytes([ID0, 1, 5, 0, 0, 6])).split(',')  # 取得CRC16
        ser.write(
            bytes([ID0, 1, 5, 0, 0, 6, int(crcs[0]), int(crcs[1])]))  # 傳送資料
        time.sleep(0.05)  # 等50ms 等到isplc回應

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

    def readM(self):
        # 0~15
        ret = ''
        OutCoil = ''
        ReturnOutCoil = ''

        # ---------------------------------
        Em = [0, 10, 20, 30, 40]
        for ci in range(5):
            # 計算CR
            crcs = crc(bytes([ID0, 1, 8, Em[ci], 0, 10])).split(',')
            # 傳送資料 格式為bytes([ID, func, 元件,位置, 讀取元,件數量, CRC`H`, CRC`L`)])
            ser.write(
                bytes([ID0, 1, 8, Em[ci], 0, 10, int(crcs[0]), int(crcs[1])]))

            time.sleep(0.05)
            r = ser.read(7)
            rrr = ser.read_all()
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
