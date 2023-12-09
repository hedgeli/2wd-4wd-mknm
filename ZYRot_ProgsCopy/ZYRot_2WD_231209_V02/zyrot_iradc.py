
from machine import Pin, ADC
import time



if __name__ == '__main__':
    iradc1 = ADC(Pin(34))
    iradc2 = ADC(Pin(32))
    iradc3 = ADC(Pin(36))
    iradc1.atten(ADC.ATTN_11DB)
    iradc2.atten(ADC.ATTN_11DB)
    iradc3.atten(ADC.ATTN_11DB)
    
    for i in range(600):
        ir1 = iradc1.read()
        ir2 = iradc2.read()
        ir3 = iradc3.read()
        print('ir1:',ir1,'ir2:',ir2,'ir3:',ir3)
        time.sleep_ms(200)






