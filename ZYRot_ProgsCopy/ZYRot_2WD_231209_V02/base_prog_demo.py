# 一、  GPIO输出，控制LED灯
from machine import Pin

# 5,18,19脚输出低电平，关闭对应的LED，方便使用第21脚演示
Pin(5, Pin.OUT,value=0)
Pin(18, Pin.OUT,value=0)
Pin(19, Pin.OUT,value=0)

led = Pin(21, Pin.OUT)
led.on()        # 点亮LED
led.off()       # 关闭LED

# 二、  时间延迟
import time
for i in range(10):        # LED 闪烁10次
    led.on()
    time.sleep_ms(500)     # 亮500ms
    led.off()
    time.sleep_ms(500)     # 灭500ms
    
# 定义函数，方便重复调用
def led_lamp(N=10):
    for i in range(N):        # LED 闪烁10次
        led.on()
        time.sleep_ms(500)     # 亮500ms
        led.off()
        time.sleep_ms(500)     # 灭500ms
        
    
# 三、  使用PWM功能调节LED亮度
from machine import Pin, PWM
import time
import pwm_motor_test    # 防止PWM操作影响电机
pwm_motor_test.pwm_init()

pwm21 = PWM(Pin(21))
pwm21.duty(0)
for i in range(5):  # 循环5次
    for j in range(20):
        pwm21.duty(j*50)  # 渐亮
        time.sleep_ms(100)  
    for j in range(20):
        pwm21.duty(1000-j*50) # 渐灭
        time.sleep_ms(100)
    
    
# 四、  无源压电蜂鸣器及音阶演奏
# # 从1000Hz到5000Hz驱动无源压电蜂鸣器    
# beep = PWM(Pin(0),freq=1000)
# beep.duty(512)
# time.sleep(1)
# beep = PWM(Pin(0),freq=2000)
# beep.duty(512)
# time.sleep(1)
# beep = PWM(Pin(0),freq=3000)
# beep.duty(512)
# time.sleep(1)
# beep = PWM(Pin(0),freq=4000)
# beep.duty(512)
# time.sleep(1)
# beep = PWM(Pin(0),freq=5000)
# beep.duty(512)
# time.sleep(1)
# beep.duty(0)

# 无源压电蜂鸣器音阶演奏
# 从C5（中央C音）到C8
beep = PWM(Pin(0),freq=523)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=587)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=659)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=698)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=783)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=880)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=987)
beep.duty(512)
time.sleep(1)
beep.duty(0)

# C6
beep = PWM(Pin(0),freq=1046)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=1174)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=1318)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=1396)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=1568)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=1760)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=1975)
beep.duty(512)
time.sleep(1)

# C7
beep = PWM(Pin(0),freq=2093)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=2349)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=2637)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=2793)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=3135)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=3520)
beep.duty(512)
time.sleep(1)
beep = PWM(Pin(0),freq=3950)
beep.duty(512)
time.sleep(1)

# C8
beep = PWM(Pin(0),freq=4186)
beep.duty(512)
time.sleep(1)
beep.duty(0)

#  五、 ADC电池及充电电压测量
from machine import ADC, Pin
import time
ADC_MAX_VOL = 3450
adc_batt = ADC(Pin(35))
#adc_usb = ADC(Pin(4))   # Hardware V2.5andlower 绿色或蓝色PCB板
adc_usb = ADC(Pin(34))   # Hardware V3.0 黑色PCB板
adc_batt.atten(ADC.ATTN_11DB)
adc_usb.atten(ADC.ATTN_11DB)
for i in range(200):
    vad = adc_batt.read()
    batt_vol = int(vad*2*ADC_MAX_VOL/4095)
    print('bat_V:', batt_vol,'mV', end=' ')
    vad_usb = adc_usb.read()
    usb_vol = int(vad_usb*2*ADC_MAX_VOL/4095)
    print('usb_V:', usb_vol,'mV')
    time.sleep_ms(100)
    

#  六、 函数定义
def print_voltage(N=50):
    from import ADC, Pin
    import time
    ADC_MAX_VOL = 3450
    adc_batt = ADC(Pin(35))
    adc_usb = ADC(Pin(4))
    adc_batt.atten(ADC.ATTN_11DB)
    adc_usb.atten(ADC.ATTN_11DB)
    for i in range(N):
        # 循环N次
        vad = adc_batt.read()
        batt_vol = int(vad*2*ADC_MAX_VOL/4095)
        print('batt_vol:', batt_vol,'mV', end='    ')
        vad_usb = adc_usb.read()
        usb_vol = int(vad_usb*2*ADC_MAX_VOL/4095)
        print('usb_vol:', usb_vol,'mV')
        time.sleep_ms(100)


#  七、 Max7219驱动8*8LED点阵显示
import max7219_8x8led_iosimu as led8x8
led8x8.clear_7219()
led8x8.disp_lowercase_char('a')
time.sleep_ms(500)
led8x8.disp_lowercase_char('b')
time.sleep_ms(500)
led8x8.disp_lowercase_char('y')
time.sleep_ms(500)
led8x8.disp_lowercase_char('z')
time.sleep_ms(500)
led8x8.disp_uppercase_char('A')
time.sleep_ms(500)
led8x8.disp_uppercase_char('B')
time.sleep_ms(500)
led8x8.disp_uppercase_char('Y')
time.sleep_ms(500)
led8x8.disp_uppercase_char('Z')
time.sleep_ms(500)
led8x8.led8x8.clear_7219()
led8x8.disp_num(0)
time.sleep_ms(500)
led8x8.disp_num(50)
time.sleep_ms(500)
led8x8.disp_num(99)
time.sleep_ms(500)


# 八、 面向对象编程
if __name__ == '__main__':
    import time
    from zyrot_2WD_IR_rawPWM import rawPWM_2WD
    zy2wd = rawPWM_2WD()
    for i in range(10):
        print("zyrot_2WD_IR_rawPWM test...", i)
        print('Move front in duty 200 for 1000ms')
        zy2wd.move(200, 200)
        time.sleep_ms(1000)
        zy2wd.move(0, 0)
        time.sleep_ms(300)
        print('Move back in duty 200 for 1000ms')
        zy2wd.move(-200, -200)
        time.sleep_ms(1000)
        zy2wd.move(0, 0)
        time.sleep_ms(300)
        print('Turn right in duty 200 for 1000ms')
        zy2wd.move(0, -200)
        time.sleep_ms(1000)
        zy2wd.move(0, 0)
        time.sleep_ms(300)
        print('Turn left in duty 200 for 1000ms')
        zy2wd.move(-200, 0)
        time.sleep_ms(1000)
        zy2wd.move(0, 0)
        time.sleep_ms(300)


#  定时器、中断、串行并行同步异步通信、直流电机PID速度/位置控制、
#  多线程、Wifi网络编程、ROS机器人编程 等等内容待续……。

