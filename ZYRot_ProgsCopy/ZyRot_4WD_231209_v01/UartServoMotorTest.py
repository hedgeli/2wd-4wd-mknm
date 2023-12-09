from machine import UART
import time
from machine import Pin
# GPIO16->RX2  GPIO17->TX2
uart2 = UART(2,tx=17,rx=16)
uart2.init(115200, bits=8, parity=None, stop=1) 
time.sleep_ms(1)

print("Blue LED in Pin-2")
blueLed = Pin(2,Pin.OUT)

ang_000_cmd = bytearray([0xFA,0xAF,0x00,0x01,0x00,0x20,0x00,0x20,0x41,0xED])
ang_120_cmd = bytearray([0xFA,0xAF,0x00,0x01,0x78,0x20,0x00,0x20,0xB9,0xED])
ang_240_cmd = bytearray([0xFA,0xAF,0x00,0x01,0xF0,0x20,0x00,0x20,0x31,0xED])

send_us = 1200

print("Uart2 Servo Motor Test...")
time.sleep_ms(500)
for i in range(10):
    print('Test cnt:',i)
    blueLed.value(1)
#     uart2 = UART(2, 115200,tx=17,rx=16)
#     time.sleep_us(send_us)
    uart2 = UART(2,tx=17,rx=16)
    uart2.init(115200, bits=8, parity=None, stop=1) 
    time.sleep_ms(1)
    uart2.write(ang_000_cmd)
    time.sleep_us(send_us)
    uart2 = UART(2, 115200,tx=16,rx=17)
    uart2.init(115200, bits=8, parity=None, stop=1) 
    time.sleep_ms(10)
    rxdata = uart2.read(10)
    print(rxdata)
    time.sleep_ms(1000)
    
    blueLed.value(0)
#     uart2 = UART(2, 115200,tx=17,rx=16)
    uart2 = UART(2,tx=17,rx=16)
    uart2.init(115200, bits=8, parity=None, stop=1) 
    time.sleep_ms(1)
    time.sleep_us(100)    
    uart2.write(ang_120_cmd)
    time.sleep_us(send_us)
    uart2 = UART(2, 115200,tx=16,rx=17)
    uart2.init(115200, bits=8, parity=None, stop=1) 
    time.sleep_ms(10)
    rxdata = uart2.read(10)
    print(rxdata)
    time.sleep_ms(1000)
    
    
    blueLed.value(1)
#     uart2 = UART(2, 115200,tx=17,rx=16)
    uart2 = UART(2,tx=17,rx=16)
    uart2.init(115200, bits=8, parity=None, stop=1) 
    time.sleep_ms(1)
    time.sleep_us(100) 
    uart2.write(ang_240_cmd)
    time.sleep_us(send_us)
    uart2 = UART(2, 115200,tx=16,rx=17)
    uart2.init(115200, bits=8, parity=None, stop=1) 
    time.sleep_ms(10)
    rxdata = uart2.read(10)
    print(rxdata)
    time.sleep_ms(1000)
    
    
#     blueLed.value(0)
#     uart2.write(ang_120_cmd)
#     time.sleep_ms(1000)
#     uart2.write(ang_000_cmd)
#     blueLed.value(1)
#     time.sleep_ms(1000)
print("End of uart2 Servo Motor Test")
while 1:
    blueLed.value(0)
    time.sleep_ms(400)
    blueLed.value(1)
    time.sleep_ms(100)

