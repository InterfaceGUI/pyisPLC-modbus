# py-isPLC
一個 [isPLC](https://blog.xuite.net/plcduino/blog) 的Python模組(modbus版本)

目前可用方法:

```python
Read_coil()
Read_coils()
Write_coil()
Write_coils()
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

#寫入元件
plc.Write_coil('Y',0,True)
plc.Write_coil('Y',1,True)
plc.Write_coil('Y',2,False)

#寫入元件陣列
plc.Write_coils('Y',0,4,7)
	#也就是 Y0開始 共 4 個 ；"7" 轉 2進位之後 為 0111 
	#也就是
	#Y0	Y1	Y2	Y3 
	#LOW	HIGH	HIGH	HIGH
	# 0	 1	 1	 1
	#
#例2: 
	#plc.Write_coils('Y',2,4,5)
	#也就是 Y2開始 共 4 個 ；5 轉 2進位之後 為 0110
	#也就是
	#Y0	Y1	Y2	Y3 
	#LOW	HIGH	HIGH	LOW
	# 0	 1	 1 	 0


## 七段顯示器 0~9 9~0 重複

while 1:
  for i in range(0,9):
    plc.Write_coils('Y',0,4,i)
    time.sleep(0.5)

  for i in range(9,0,-1):
    plc.Write_coils('Y',0,4,i)
    time.sleep(0.5)
	
## 7447 接腳 -> 
### Y	0	1	2	3
###	A	B	C	D
	


```
