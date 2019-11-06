# py-isPLC
一個 [isPLC](https://blog.xuite.net/plcduino/blog) 的Python模組(modbus版本)

![](https://img.shields.io/github/issues/InterfaceGUI/pyisPLC-modbus?style=for-the-badge)&nbsp;&nbsp;
![](https://img.shields.io/badge/Python-v3.7-blue?style=for-the-badge)&nbsp;&nbsp;
![](https://img.shields.io/badge/Version-v1.0-green?style=for-the-badge)&nbsp;&nbsp;
![](https://img.shields.io/github/license/InterfaceGUI/pyisPLC-modbus?style=for-the-badge)

## 安裝方法

#### 使用pip安裝：
```pip install git+https://github.com/InterfaceGUI/pyisPLC-modbus.git```

## 用法

```python
open()
close()
Read_coil()
Read_coils()
ReadRegister()
Write_coil()
Write_coils()
Write_Register()

```

範例:
```python
import isPLC_Package.isPLC
plc = isPLC_Package.isPLC.ClassCGS_isPLC()

#指定設備ID
plc = isPLC.ClassCGS_isPLC(0x01)


plc.open('COM3')

print(plc.Version) #顯示版本

#讀取元件
print(plc.Read_coil('M0'))
print(plc.Read_coil('Y1'))
print(plc.Read_coil('X3'))
print(plc.Read_coil('T10'))

#讀取元件陣列
print(plc.Read_coils('M0')) # M0 ~ M7
print(plc.Read_coils('M1')) # M8 ~ M15
print(plc.Read_coils('Y'))  # Y0 ~ Y6


#寫入元件
plc.Write_coil('Y',0,True)
plc.Write_coil('Y',1,True)
plc.Write_coil('Y',2,False)
plc.Write_coil('M',1,True)

#讀取暫存器
print(plc.ReadRegister(0)) # 讀取D0

#寫入暫存器
plc.Write_Register(0,1024) #將 1024 寫入 D0
plc.Write_Register(1,50)   #將 50 寫入 D1


plc.close() #關閉連線

```
