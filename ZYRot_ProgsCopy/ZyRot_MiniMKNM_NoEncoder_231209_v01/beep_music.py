from machine import Pin,PWM
import math
import time

def pwm_set_0():
#     pwm1 = PWM(Pin(27), freq=500, duty=0)
#     pwm2 = PWM(Pin(14), freq=500, duty=0)
#     
#     pwm3 = PWM(Pin(13), freq=500, duty=0)
#     pwm4 = PWM(Pin(12), freq=500, duty=0) 
#     
#     
#     pwm5 = PWM(Pin(18), freq=500, duty=0)
#     pwm6 = PWM(Pin(5), freq=500, duty=0)   
#     
#     pwm7 = PWM(Pin(19), freq=500, duty=0)
#     pwm8 = PWM(Pin(21), freq=500, duty=0)
#     
#     pwm9 = PWM(Pin(26), freq=500, duty=0)   
#     pwm10 = PWM(Pin(15), freq=500, duty=0)
# 
#     pwm11 = PWM(Pin(23), freq=500, duty=0)
#     pwm12 = PWM(Pin(22), freq=500, duty=0)
    Pin(27, Pin.OUT, value=0)
    Pin(14, Pin.OUT, value=0)
    Pin(12, Pin.OUT, value=0)
    Pin(13, Pin.OUT, value=0)
    
    Pin(21, Pin.OUT, value=0)
    Pin(19, Pin.OUT, value=0)
    Pin(18, Pin.OUT, value=0)
    Pin(5, Pin.OUT, value=0)
    
    

def beep_music_melody(length=0):
    melody = [
    330, 330, 330, 262, 330, 392, 196, 262, 196, 165, 220, 247, 233, 220, 196, 330, 392,
    440, 349, 392, 330, 262, 294, 247, 262, 196, 165, 220, 247, 233, 220, 196, 330, 392,
    440, 349, 392, 330, 262, 294, 247, 392, 370, 330, 311, 330, 208, 220, 262, 220, 262,
    294, 392, 370, 330, 311, 330, 523, 523, 523, 392, 370, 330, 311, 330, 208, 220, 262,
    220, 262, 294, 311, 294, 262, 262, 262, 262, 262, 294, 330, 262, 220, 196, 262, 262,
    262, 262, 294, 330, 262, 262, 262, 262, 294, 330, 262, 220, 196]

    noteDurations = [
    8,4,4,8,4,2,2,
    3,3,3,4,4,8,4,8,8,8,4,8,4,3,8,8,3,
    3,3,3,4,4,8,4,8,8,8,4,8,4,3,8,8,2,
    8,8,8,4,4,8,8,4,8,8,3,8,8,8,4,4,4,8,2,
    8,8,8,4,4,8,8,4,8,8,3,3,3,1,
    8,4,4,8,4,8,4,8,2,8,4,4,8,4,1,
    8,4,4,8,4,8,4,8,2]
    music=PWM(Pin(0))
    music.duty(512)
    if length == 0:
        length = len(melody)
    elif length > len(melody):
        length = len(melody)
    
    for i in range(length):
      noteDuration = 800/noteDurations[i]
      music.freq(melody[i]*2)
      time.sleep_ms(int(noteDuration * 1.30))
    music.deinit()
    pin0 = Pin(0, Pin.OUT, value=1)

if __name__ == '__main__':
    beep_music_melody(8)

