# 用缓存来定义并滚动
from machine import Pin, SoftSPI
import time
from micropython import const
import ntptime
import network

font = (  #8x8矩阵中的字符集5x8
  0x0e, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0e, 0x00,   # 0x30, 0
  0x04, 0x0c, 0x04, 0x04, 0x04, 0x04, 0x0e, 0x00,   # 0x31, 1
  0x0e, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1f, 0x00,   # 0x32, 2
  0x0e, 0x11, 0x01, 0x06, 0x01, 0x11, 0x0e, 0x00,   # 0x33, 3
  0x02, 0x06, 0x0a, 0x12, 0x1f, 0x02, 0x02, 0x00,   # 0x34, 4
  0x1f, 0x10, 0x1e, 0x01, 0x01, 0x11, 0x0e, 0x00,   # 0x35, 5
  0x06, 0x08, 0x10, 0x1e, 0x11, 0x11, 0x0e, 0x00,   # 0x36, 6
  0x1f, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08, 0x00,   # 0x37, 7
  0x0e, 0x11, 0x11, 0x0e, 0x11, 0x11, 0x0e, 0x00,   # 0x38, 8
  0x0e, 0x11, 0x11, 0x0f, 0x01, 0x02, 0x0c, 0x00,   # 0x39, 9  
)

_NOOP = const(0)
_DIGIT0 = const(1)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)

class Matrix8x8:
    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.cs.init(mode=Pin.OUT, value=1)
        self.buff = [0]*8*4 #缓存list ，4个7219
        self.init()

    def _write(self, command, data):
        self.cs(0)
        for m in range(4):  #4个7219都要写
            self.spi.write(bytearray([command, data]))
        self.cs(1)

    def init(self):
        for command, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
            (_INTENSITY, 0) #默认亮度0
        ):
            self._write(command, data)
            
    def show(self):
        pass
    
    
    def brightness(self, value):
        if not 0 <= value <= 15:
            raise ValueError("Brightness out of range")
        self._write(_INTENSITY, value)
    
    def set_nub(self,nub,psion): # 数字，位置        
        for j in range(8):
            self.buff[j*4+psion] = font[nub*8+j]

    def up_roll(self,nub,psion): # 数字，位置        
        for i in range(8):
            for j in range(7):
                self.buff[4*j+psion] =self.buff[4*(j+1)+psion]
            self.buff[4*7+psion] = font[nub*8+i]
            self.show()
            time.sleep_ms(80)

    def down_roll(self,nub,psion): # 数字，位置        
        for i in range(7,-1,-1):
            for j in range(7,0,-1):
                self.buff[4*j+psion] =self.buff[4*(j-1)+psion]
            self.buff[0+psion] = font[nub*8+i]
            self.show()            
            time.sleep_ms(80)

#spi = SoftSPI(sck=Pin(0), mosi=Pin(2), miso=Pin(12), baudrate=10000000)  #10Mhz 串口
spi = SoftSPI(sck=Pin(0), mosi=Pin(2),  miso=Pin(4), baudrate=1000000)  #1Mhz
display = Matrix8x8(spi, Pin(15))

def  digt(nub):
    _l = []
    _s = '{0:0>4d}'.format(nub)
    for i in range(len(_s)):
        _l.append(int(_s[i]))
    return(_l)

while True:
    for i in range(10):
        display.up_roll(i,0)
        display.down_roll(9-i,1)
        display.up_roll(i,2)
        display.down_roll(9-i,3)
        time.sleep_ms(500)

    for i in range(10):
        display.up_roll(i,1)
        display.up_roll(i,3)
        time.sleep_ms(500)

    #display.down_4_roll((0,0,0,0),(9,9,9,9))    
    for i in range(9999,9980,-1):
        display.down_4_roll(digt(i),digt(i-1))
        time.sleep_ms(300)
      
    for i in range(9980,9999):
        display.up_4_roll(digt(i),digt(i+1))
        time.sleep_ms(300)

