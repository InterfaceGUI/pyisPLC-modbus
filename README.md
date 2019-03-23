# py-isPLC
一個isPLC的Python模組(modbus版本)

目前可用方法:

```python
Read_coil()
```
目前能夠讀取 M 、 Y 、X 、T

用法:
```python
import isPLC_Package.isPLC
plc = isPLC_Package.isPLC.ClassCGS_isPLC()

#指定設備ID
#plc = isPLC.ClassCGS_isPLC(0x02)


plc.open('COM3')

print(plc.Version)

#讀取元件
print(plc.Read_coil('M0'))
print(plc.Read_coil('Y1'))
print(plc.Read_coil('X3'))
print(plc.Read_coil('T10'))

#讀取元件陣列
print(plc.Read_coils(['M','0','1','2','3','4','5','6','7','8','9','10','11','12']))
print(plc.Read_coils(['Y','0','1','2','3','4','5']))
plc.close()
```
