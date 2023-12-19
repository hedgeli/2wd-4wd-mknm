from machine import Pin
import time

def init_7219_pin():
    pin_clk = Pin(0, Pin.OUT, value=1)
    pin_cs = Pin(15, Pin.OUT, value=1)
    pin_din = Pin(2, Pin.OUT, value=1)

def write_byte(data):
    pin_clk = Pin(0, Pin.OUT, value=1)
    pin_din = Pin(2, Pin.OUT, value=1)
    time.sleep_us(5)
    for i in range(8):
        pin_clk.off()
        pin_din.value(1 if ((data<<i) & 0x80) else 0)
        pin_clk.on()
        
def write_data(addr, data):
    pin_clk = Pin(0, Pin.OUT, value=1)
    pin_cs = Pin(15, Pin.OUT, value=1)
    pin_din = Pin(2, Pin.OUT, value=1)
    time.sleep_us(5)
    pin_cs.off()
    time.sleep_us(2)
    write_byte(addr)
    write_byte(data)
    time.sleep_us(2)
    pin_cs.on()
    
def init_max7219():
    write_data(0x0c, 0x00)    # 关闭
    write_data(0x0f, 0x00)
    write_data(0x0b, 0x07)
    write_data(0x0a, 0x00)    # 亮度
    write_data(0x09, 0x00)
    write_data(0x0c, 0x01)    # 显示
    
font = (  #8x8矩阵中的字符集5x8
0x00,0x0C,0x12,0x12,0x12,0x12,0x12,0x0C,    # /*"0",0*/
0x00,0x04,0x06,0x04,0x04,0x04,0x04,0x0E,    # /*"1",1*/
0x00,0x0C,0x12,0x10,0x18,0x0C,0x06,0x1E,    # /*"2",2*/
0x00,0x0e,0x10,0x10,0x0e,0x10,0x10,0x0E,    # /*"3",3*/
0x00,0x08,0x0C,0x0C,0x0A,0x1E,0x08,0x08,    # /*"4",4*/
0x00,0x1E,0x02,0x0E,0x10,0x10,0x10,0x0E,    # /*"5",5*/
0x00,0x1C,0x06,0x02,0x1E,0x12,0x12,0x0C,    # /*"6",6*/
0x00,0x1E,0x10,0x08,0x08,0x08,0x0C,0x04,    # /*"7",7*/
0x00,0x0C,0x12,0x12,0x0C,0x12,0x12,0x0C,    # /*"8",8*/
0x00,0x0C,0x12,0x12,0x1E,0x10,0x18,0x0E,    # /*"9",9*/
0x00,0x00,0x0c,0x10,0x1c,0x12,0x12,0x3c,    # /*"a",10*/
0x02,0x02,0x02,0x0E,0x12,0x12,0x12,0x0E,    # /*"b",11*/
0x00,0x00,0x0C,0x02,0x02,0x02,0x0C,0x00,    # /*"c",12*/
0x00,0x10,0x10,0x1C,0x12,0x12,0x12,0x1C,    # /*"d",13*/
0x00,0x00,0x00,0x0C,0x12,0x1E,0x02,0x1C,    # /*"e",14*/
0x18,0x04,0x04,0x1E,0x04,0x04,0x04,0x04,    # /*"f",15*/
0x00,0x1C,0x12,0x12,0x12,0x1C,0x10,0x0E,    # /*"g",16*/
0x02,0x02,0x02,0x1E,0x12,0x12,0x12,0x12,    # /*"h",17*/
0x04,0x00,0x00,0x06,0x04,0x04,0x04,0x0E,    # /*"i",18*/
0x04,0x00,0x06,0x04,0x04,0x04,0x04,0x07,    # /*"j",19*/
0x02,0x02,0x02,0x1A,0x0A,0x06,0x0A,0x12,    # /*"k",20*/
0x06,0x04,0x04,0x04,0x04,0x04,0x04,0x18,    # /*"l",21*/
0x00,0x00,0x00,0x1f,0x15,0x15,0x15,0x15,    # /*"m",22*/
0x00,0x00,0x00,0x0e,0x12,0x12,0x12,0x12,    # /*"n",23*/
0x00,0x00,0x00,0x0C,0x12,0x12,0x12,0x0C,    # /*"o",24*/
0x00,0x0E,0x12,0x12,0x12,0x0E,0x02,0x02,    # /*"p",25*/
0x00,0x1C,0x12,0x12,0x12,0x1C,0x10,0x10,    # /*"q",26*/
0x00,0x00,0x00,0x0E,0x02,0x02,0x02,0x02,    # /*"r",27*/
0x00,0x00,0x00,0x1E,0x02,0x1C,0x10,0x1E,    # /*"s",28*/
0x00,0x04,0x04,0x1E,0x04,0x04,0x04,0x1C,    # /*"t",29*/
0x00,0x00,0x00,0x12,0x12,0x12,0x12,0x0C,    # /*"u",30*/
0x00,0x00,0x00,0x12,0x12,0x0a,0x0C,0x04,    # /*"v",31*/
0x00,0x00,0x00,0x11,0x15,0x0A,0x0A,0x0A,    # /*"w",32*/
0x00,0x00,0x00,0x12,0x0C,0x04,0x0C,0x12,    # /*"x",33*/
0x00,0x12,0x0A,0x0C,0x0C,0x04,0x04,0x06,    # /*"y",34*/
0x00,0x00,0x00,0x1E,0x08,0x04,0x04,0x1E,    # /*"z",35*/
0x00,0xff,0x00,0x00,0x00,0x00,0x00,0x00,    # /*"-",36*/
0x00,0x00,0x00,0x00,0x00,0x00,0xff,0x00,    # /*"_",37*/
0x00,0xff,0x00,0xff,0x00,0x00,0xff,0x00,    # /*"_",38*/
)


font_capital = (
    0x3C,0x42,0x42,0x42,0x42,0x42,0x3C,0x00,    #  0, 0
    0x0C,0x0B,0x08,0x08,0x08,0x08,0x7F,0x00,    #  1, 1
    0x1E,0x20,0x20,0x10,0x0C,0x02,0x3E,0x00,    #  2, 2
    0x1E,0x20,0x20,0x1C,0x20,0x20,0x1E,0x00,    #  3, 3
    0x10,0x18,0x14,0x12,0x3F,0x10,0x10,0x00,    #  4, 4
    0x3C,0x04,0x04,0x1C,0x20,0x20,0x1C,0x00,    #  5, 5
    0x3C,0x04,0x02,0x3A,0x46,0x42,0x3C,0x00,    #  6, 6
    0x7E,0x20,0x20,0x10,0x08,0x08,0x04,0x00,    #  7, 7
    0x3C,0x42,0x26,0x3C,0x62,0x42,0x3C,0x00,    #  8, 8
    0x1C,0x22,0x42,0x7C,0x40,0x20,0x3C,0x00,    #  9, 9
    0x18,0x18,0x24,0x24,0x7E,0x42,0x81,0x00,    #  A, 10
    0x3E,0x42,0x42,0x3E,0x42,0x42,0x3E,0x00,    #  B, 11
    0x7C,0x02,0x01,0x01,0x01,0x02,0x7C,0x00,    #  C, 12
    0x3E,0x62,0x42,0x42,0x42,0x22,0x1E,0x00,    #  D, 13
    0x7E,0x02,0x02,0x3E,0x02,0x02,0x7E,0x00,    #  E, 14
    0x7E,0x02,0x02,0x3E,0x02,0x02,0x02,0x00,    #  F, 15
    0x7C,0x02,0x01,0x71,0x41,0x42,0x7C,0x00,    #  G, 16
    0x42,0x42,0x42,0x7E,0x42,0x42,0x42,0x00,    #  H, 17
    0x3E,0x08,0x08,0x08,0x08,0x08,0x3E,0x00,    #  I, 18
    0x3C,0x20,0x20,0x20,0x20,0x20,0x1E,0x00,    #  J, 19
    0x22,0x12,0x0A,0x0E,0x1A,0x22,0x42,0x00,    #  K, 20
    0x02,0x02,0x02,0x02,0x02,0x02,0x7E,0x00,    #  L, 21
    0x63,0x63,0x55,0x55,0x55,0x49,0x41,0x00,    #  M, 22
    0x46,0x46,0x4A,0x5A,0x52,0x62,0x42,0x00,    #  N, 23
    0x1C,0x22,0x41,0x41,0x41,0x22,0x1C,0x00,    #  O, 24
    0x3E,0x42,0x42,0x3E,0x02,0x02,0x02,0x00,    #  P, 25
    0x3C,0x62,0x41,0x41,0x41,0x22,0x1C,0x60,    #  Q, 26
    0x1E,0x22,0x22,0x1E,0x12,0x22,0x42,0x00,    #  R, 27
    0x7C,0x02,0x06,0x38,0x40,0x40,0x3E,0x00,    #  S, 28
    0x7F,0x08,0x08,0x08,0x08,0x08,0x08,0x00,    #  T, 29
    0x42,0x42,0x42,0x42,0x42,0x42,0x3C,0x00,    #  U, 30
    0x81,0x42,0x42,0x26,0x14,0x14,0x08,0x00,    #  V, 31
    0x81,0x89,0x59,0x5A,0x56,0x66,0x24,0x00,    #  W, 32
    0xC3,0x66,0x3C,0x18,0x3C,0x62,0xC1,0x00,    #  X, 33
    0x41,0x22,0x14,0x08,0x08,0x08,0x08,0x00,    #  Y, 34
    0x7F,0x20,0x10,0x08,0x04,0x02,0x7F,0x00,    #  Z, 35
    
    0x00,0x00,0x40,0xff,0x40,0x00,0x00,0x00,    #  <, 35
    0x00,0x00,0x02,0xff,0x02,0x00,0x00,0x00,    #  >, 35
    0x08,0x1c,0x08,0x08,0x08,0x08,0x08,0x00,    #  ^, 35
    0x08,0x08,0x08,0x08,0x08,0x1c,0x08,0x00,    #  d, 35
    0x7F,0x20,0x10,0x08,0x04,0x02,0x7F,0x00,    #  Z, 35
    0x7F,0x20,0x10,0x08,0x04,0x02,0x7F,0x00,    #  Z, 35
    0x7F,0x20,0x10,0x08,0x04,0x02,0x7F,0x00,    #  Z, 35
    0x7F,0x20,0x10,0x08,0x04,0x02,0x7F,0x00,    #  Z, 35
    )


def disp_char(c=0):
    if c > len(font)//8:
        c = len(font)//8
    for i in range(8):
        write_data(i+1, font[(c+1)*8-i-1])
        
        
def disp_lowercase_char(c='a'):
    idx = ord(c)-ord('a')
    if (idx>=0)and(idx<=(ord('z')-ord('a'))):
        for i in range(8):
            write_data(i+1, font[(idx+1+10)*8-i-1])
            
            
def disp_uppercase_char(c='A'):
    idx = ord(c)-ord('A')
    if (idx>=0)and(idx<=(ord('Z')-ord('A'))):
        for i in range(8):
            write_data(i+1, font_capital[(idx+1+10)*8-i-1])
            

def disp_sym(c=1):
    idx = ord('Z')-ord('A')+c
    if c <= 6:
        for i in range(8):
            write_data(i+1, font_capital[(idx+1+10)*8-i-1])
    
    

def disp_num(n=0):
    if (n>=100)or(n<0):
        disp_char(38)
        print('Display num range is 0-99.')
        return
    if n>=10:
        n2=int(n//10)
        n1=int(n%10)
        for i in range(8):
            dn2 = font[(n2+1)*8-i-1]>>1
            dn1 = font[(n1+1)*8-i-1]<<3
            write_data(i+1, dn2|dn1) 
        return
    else:
        disp_char(n)
        return


def disp_7219_all():
    init_max7219()
    for i in range(8):
        write_data(i+1, 0xff)
    time.sleep_ms(1)

def clear_7219():
    init_max7219()
    for i in range(8):
        write_data(i+1, 0x00)
    #write_data(0x0c, 0x00)    # 关闭
    time.sleep_ms(1)
    
if __name__ == '__main__':
    print('Start Max7219 disp test...')
    time.sleep_ms(100)
    col = [0x00, 0x66, 0x99,0x81,0x42,0x24,0x18,0x00]
    init_max7219()
    disp_7219_all()
    time.sleep_ms(500)
    clear_7219()

    # 显示心形图
    for i in range(8):
        write_data(i+1, col[7-i])
    time.sleep_ms(500)
    
    # 显示符号
    for i in range(5):
        disp_sym(i)
        time.sleep_ms(500)
    
    
    disp_lowercase_char('a')
    time.sleep_ms(500)
    disp_lowercase_char('b')
    time.sleep_ms(500)
    disp_lowercase_char('y')
    time.sleep_ms(500)
    disp_lowercase_char('z')
    time.sleep_ms(500)
    disp_uppercase_char('A')
    time.sleep_ms(500)
    disp_uppercase_char('B')
    time.sleep_ms(500)
    disp_uppercase_char('Y')
    time.sleep_ms(500)
    disp_uppercase_char('Z')
    time.sleep_ms(500)
    
    # 显示小写数字和字母
    for n in range(36):
        for i in range(8):
            write_data(i+1, font[(n+1)*8-i-1])
        time.sleep_ms(500)

    # 显示大字数字及字母
    for n in range(36):
        for i in range(8):
            write_data(i+1, font_capital[(n+1)*8-i-1])
        time.sleep_ms(500)

    # 显示数字0-99
    for i in range(100):
        disp_num(i)
        time.sleep_ms(500)
    
    # 8*8LED全亮
    disp_7219_all()
    time.sleep_ms(1000)
    clear_7219()
    print('Max7219 disp test over.')
                      



