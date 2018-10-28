# py-isPLC
一個isPLC的Python模組(modbus版本)

用法
```python
import isPLC
plc = isPLC.ClassCGS_isPLC()

#指定設備ID
#plc = isPLC.ClassCGS_isPLC(0x02)


plc.open('COM3')

print(plc.Version)

print(plc.Read_coil('M0'))
print(plc.Read_coil('Y1'))
print(plc.Read_coil('X3'))
print(plc.Read_coil('T10'))

plc.close()
