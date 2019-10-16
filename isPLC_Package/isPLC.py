try:
    import pip
except ImportError:
    raise ImportError('請安裝pip模組')


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

import time,sys,math,asyncio



def Bin(x):
    ''' dec to bin list'''
    return [int(d) for d in str(bin(x))[2:].zfill(8)]


def crc(byte):
    ''' 
    [ (H) , (L) ] \n
    crc(bytes([0x1,0x11])) == 192,44
    '''
    # ['modbus','CrcModbus',0x18005,REVERSE,0xFFFF,0x0000,0x4B37]
    cr = crc16(byte)
    crhex = str(hex(cr))[2:].zfill(4).upper()
    re = crhex[:2]
    re2 = crhex[2:]
    if re2 =='':
        re2 = '0'
    return [ int(re2, base=16) , int(re, base=16) ]


class ClassCGS_isPLC():
    '''ID 為設備ID'''

    def __init__(self, ID=0x01):
        self.Version = '請使用isPLC核心，或重新更新韌體。'
        global ID0
        global crc16
        ID0 = ID
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)

    def open(self, Port):
        '''開啟新的序列埠連線。'''
        global ser
        mes = str()
        ser = serial.Serial(Port, baudrate=38400,
                            stopbits=1, timeout=0.5, bytesize=8, parity='N')
        for i in range(1, 30):
            time.sleep(0.5)
            ser.write(bytes([ID0, 17, 192, 44]))
            time.sleep(0.05)


            if not ser.readable():
                continue

            try:
                
                r = ser.read_all()
        
                if r == b'':
                    continue
                
                for i in r[:-2]:
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
            raise RuntimeError(Port + ' 無法連接')

    def close(self):
        '''關閉連線。'''
        try:
            ser.close()
        except:
            pass


    def Read_coil(self, Element):
        '''
        `Element` 為元件，
        回傳 bool (`0` or `1`)\n
        { Y、X、M、T、S、C }\n\n
        用法；\n
        取得 `Y5`狀態\n
        `Read_coil('Y5')`
        '''

        if Element[:1] == 'Y':

            ra = Read_ALL_coil().readY()
            n = int(Element[1:])
            return bool(int(ra[n]))

        elif Element[:1] == 'X':

            ra = Read_ALL_coil().readX()
            n = int(Element[1:])
            return bool(int(ra[n]))

        elif Element[:1] == 'M':
            n = int(Element[1:])
            ra = Read_ALL_coil().readM(n)
            n = n %8

            return bool(int(ra[n]))

        elif Element[:1] == 'T':

            ra = Read_ALL_coil().readT()
            n = int(Element[1:])
            return bool(int(ra[n]))

    def Read_coils(self, Elements):
        '''
        `Element` 為元件，
        回傳格式為 bool [0,1,0,1]\n
        元件線圈{ Y、X、M、T、S、C }\n\n
        用法；\n
        取得 `Y0`、`Y1`、`Y2`狀態\n
        `Read_coil('Y',['0','1','2'])`
        '''

        if Elements == 'Y':
            ra = Read_ALL_coil().readY()
            return [bool(d) for d in ra[:-2]]

        if Elements == 'X':
            ra = Read_ALL_coil().readX()
            return [bool(d) for d in ra[:-2]]

        elif Elements[0] == 'M':
            if Elements == 'M0':
                ra = Read_ALL_coil().readM(0)
            elif Elements == 'M1':
                ra = Read_ALL_coil().readM(8)
            elif Elements == 'M2':
                ra = Read_ALL_coil().readM(16)
            elif Elements == 'M3':
                ra = Read_ALL_coil().readM(24)
            elif Elements == 'M4':
                ra = Read_ALL_coil().readM(32)
            elif Elements == 'M5':
                ra = Read_ALL_coil().readM(40)
            elif Elements == 'M6':
                ra = Read_ALL_coil().readM(48)
            return [bool(d) for d in ra]


        elif Elements == 'T':
            ra = Read_ALL_coil().readT()
            return [bool(d) for d in ra]

    def ReadRegister(Self,ID):
        ''' 讀取指定暫存器 \n
            用法：
                讀取D0 → ReadRegister(0)
            結果：
                0 ~ 1023
        '''
        ra = Registers().ReadSingle(ID)
        return ra
    
    def Write_Register(self,ID , Vaule ):
        ''' 寫入指定暫存器 \n
            用法：
                D1 寫入 500 → Write_Register(1,500)
        '''

        Registers().WriteSingle(ID,Vaule)

    def Write_coil(self,Element,ID,Bool):
        '''
        若要進行大量傳送 請用 Write_coils\n\n
        `Element` 為元件，
        元件線圈{ Y、M、T、S、C }\n\n
        用法；\n
        設定 Y0 為 HIGH
        `Write_coil('Y',0,True)`
        '''
        if Element == 'Y':
            Write_All_coils().WriteY(ID,Bool)

        elif Element == 'S':
            Write_All_coils().WriteS(ID,Bool)

        elif Element == 'M':
            Write_All_coils().WriteM(ID,Bool)

        elif Element == 'T':
            Write_All_coils().WriteT(ID,Bool)

        elif Element == 'C':
            Write_All_coils().WriteC(ID,Bool)
    
    def Write_coils(self,Element,ID,amount,Bools):
        '''
        `Element` 為元件線圈{ Y、M、T、S、C }，\n
        `ID` 為起始元件 (int)
        `amoun` 為數量 (int)\n
        `Bools` 為寫入線圈狀態(int) 
        用法；\n
        設定 Y0~Y5 為 HIGH
        `Write_coil('Y',0,6,)`
        '''
        if Element == 'Y':
            re = str(bin(Bools)).replace('0b','').zfill(4)[::-1]
            Write_All_coils().WriteList_Y(ID,amount,Bools)

        elif Element == 'S':
            re = str(bin(Bools)).replace('0b','').zfill(4)[::-1]
            Write_All_coils().WriteList_S(ID,amount,Bools)

        elif Element == 'M':
            pass
            raise RuntimeError('功能尚未完成')

        elif Element == 'T':
            pass
            raise RuntimeError('功能尚未完成')

        elif Element == 'C':
            pass
            raise RuntimeError('功能尚未完成')


#---------傳輸資料與接收----------------------------------------------------

def SendD(DataList):
    ''' [ID , Func_code , d0 , d1 , ... , d4 ,d5 ] '''
    #DataList = list(DataList)
    ##CRC計算
    crcs = crc(bytes(DataList))
    DataList +=  crcs

    
    ser.write(
        bytes(DataList)
    )

    while not ser.in_waiting:
        pass
    r = list(ser.read_all())

    ##傳送錯誤
    #if r == [1, 135, 1, 130, 48]:
    #    print('Error:',DataList)
    #    return

    
    crcs = crc(bytes(r[:-2]))
    if crcs != r[-2:]:
        print('Error:',DataList)
        return None
    

    return r[:-2]

    #--------------------------------------------------------------------------



# 內部傳送 讀取線圈區塊


class Read_ALL_coil():

    # bytes(ID , Func_code , E, E, E, E, CRC {H} , CRC {L} ])
    # func_code 0x01 取輸出元件線圈狀態
    #   Read Y0 ~ Y6
    #####################################################################
    #           #   ID  #  funcCode #    addr   #  element  #   CRC     #
    # Commands  #--------#----------#-----------#-----------#-----------#
    #           #        #   0x01   # (5) # (0) # (0) # (6) # (H) # (L) #
    #####################################################################

    def readY(self):

        rec = SendD([ID0,1,5,0,0,6])
        #[1,1,1,0] = ID , FuncCode , ByteNum ,status → 8進位

        ret = list()
        
        ret = Bin(rec[3])
        if not rec[3] == 0:
            ret.reverse()
            return ret

        return ret
    ##########################################################################
    # bytes(ID , Func_code , E, E, E, E, CRC {H} , CRC {L} ])
    # func_code 0x01 取輸出元件線圈狀態
    #   Read x0 ~ X6
    #####################################################################
    #           #   ID  #  funcCode #    addr   #  element  #   CRC     #
    # Commands  #--------#----------#-----------#-----------#-----------#
    #           #        #   0x02   # (4) # (0) # (0) # (6) # (H) # (L) #
    #####################################################################
    def readX(self):
        rec = SendD([ID0,2,4,0,0,6])
        #[1,1,1,0] = ID , FuncCode , ByteNum ,status → 8進位

        ret = list()
        
        ret = Bin(rec[3])
        if not rec[3] == 0:
            ret.reverse()
            return ret

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

        if num <=7:
            r = SendD([ID0, 1, 8, 0, 0, 8])

        elif num >= 8 and num <= 15:
            r = SendD([ID0, 1, 8, 8, 0, 8])

        elif num >= 16 and num <=23 :
            r = SendD([ID0, 1, 8, 16, 0, 8])

        elif num >= 24 and num <=31 :
            r = SendD([ID0, 1, 8, 24, 0, 8])

        elif num >=32 and num <=39 :
            r = SendD([ID0, 1, 8, 32, 0, 8])

        elif num >=40 and num <= 47:
            r = SendD([ID0, 1, 8, 40, 0, 8])

        elif num >=48 and num <= 49:
            r = SendD([ID0, 1, 8, 48, 0, 8])


        ret = list()
        
        ret = Bin(r[3])
        if not r[3] == 0:
            ret.reverse()
            return ret

        return ret

    #####################################################################
    # bytes(ID , Func_code , E, E, E, E, CRC {H} , CRC {L} ])           #
    # func_code 0x01 取輸出元件線圈狀態
    #   Read T ~ T9                                                     #
    #####################################################################
    #           #   ID  #  funcCode #    addr   #  element  #   CRC     #
    # Commands  #--------#----------#-----------#-----------#-----------#
    #           #        #   0x01   # (6) # (0) # (0) # (0) # (H) # (L) #
    #####################################################################
    def readT(self):
        re = []
        Em = [0, 10]
        for ci in range(2):

            r = SendD([ID0, 1, 6, Em[ci], 0, 10])

            ret = list()
            ret = Bin(r[3])
            ret2 = [int(d) for d in str(bin(r[4]))[2:].zfill(2)]
            rrr = ret2 + ret
            rrr.reverse()
            re =  re + rrr

        return re

    ##########################################################################

class Write_All_coils():
    
    def __init__(self):
        global TrueFalse
        TrueFalse = [[0,255],[255,0]]

    #####################################################################
    # bytes(ID , Func_code , E, E, E, E, CRC {H} , CRC {L} ])           #
    # func_code 0x01 取輸出元件線圈狀態
    #   Write Multiple coil                                             #
    #############################################################################################
    #           #   ID  #  funcCode #    addr   #  num      #    Byte   #  status   #   CRC     #
    # Commands  #--------#----------#-----------#-----------#-----------#-----------#-----------#
    #           #        #   0x01   # (6) # (0) # (0) # (0) #     N     #           # (H) # (L) #
    #############################################################################################

    def WriteList_Y(self,ID,num,B):

        re = SendD([ ID0 , 15 , 5 , ID , 0 , num , 1 , B ])
        

    def WriteList_S(self,ID,num,B):

        re = SendD([ ID0 , 15 , 0 , ID , 0 , num , 1 , B ])


    def WriteS(self,Element,Bool):
        SendD([ID0, 5, 0, Element] + TrueFalse[int(Bool)])
    
    def WriteY(self,Element,Bool):
        SendD([ID0, 5, 5, Element] + TrueFalse[int(Bool)])

    def WriteM(self,Element,Bool):
        SendD([ID0, 5, 8, Element] + TrueFalse[int(Bool)])

    def WriteT(self,Element,Bool):
        SendD([ID0, 5, 6, Element] + TrueFalse[int(Bool)])
                
    def WriteC(self,Element,Bool):
        SendD([ID0, 5, 0xE, Element] + TrueFalse[int(Bool)])
        


#----------------------------------------------------------------------


class Registers():


    #####################################################################
    # bytes(ID , Func_code , E, E, E, E, CRC {H} , CRC {L} ])           #
    # func_code 0x01 取輸出元件線圈狀態
    #   Read D                                                     #
    #####################################################################
    #           #   ID  #  funcCode #    addr   #    num    #   CRC     #
    # Commands  #--------#----------#-----------#-----------#-----------#
    #           #        #   0x04   # (16) # (0)# (0) # (1) # (H) # (L) #
    #####################################################################
    def ReadSingle(self,d):

        r = SendD([ID0, 4, 16, d, 0, 1])

        r1 = str(bin(r[3]))[2:]
        r2 = str(bin(r[4]))[2:].zfill(8)
        rrr = r1+r2

        return int(rrr,base=2)



    def WriteSingle(self,d , vaule):
        date = str(bin(vaule)[2:].zfill(16))
        L = int(date[8:],base = 2)
        H = int(date[6:8],base = 2)
        r = SendD([ID0, 6, 16, d, H, L])

