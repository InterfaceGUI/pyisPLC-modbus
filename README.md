# py-isPLC
一個isPLC的Python模組(modbus版本)

目前可用方法:

```python
Read_coil()
```
目前能夠讀取 M 、 Y 、X 、T

用法
```python
import isPLC
plc = isPLC.isPLC.ClassCGS_isPLC()

#指定設備ID
#plc = isPLC.ClassCGS_isPLC(0x02)


plc.open('COM3')

print(plc.Version)

print(plc.Read_coil('M0'))
print(plc.Read_coil('Y1'))
print(plc.Read_coil('X3'))
print(plc.Read_coil('T10'))

plc.close()
