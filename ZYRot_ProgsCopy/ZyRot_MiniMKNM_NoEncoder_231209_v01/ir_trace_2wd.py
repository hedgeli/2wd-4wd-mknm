from machine import Pin, ADC
import time


def ir_adc_test():
    adc_out1 = Pin(4, mode=Pin.OUT, pull=None)
    adc_out_left = Pin(2, mode=Pin.OUT, pull=None)
    adc_out_right = Pin(15, mode=Pin.OUT, pull=None)
    adc_left1 = ADC(Pin(36))  # adc0 vp
    adc_right1 = ADC(Pin(39))  # adc3 vn
    adc_left1.atten(ADC.ATTN_11DB)
    adc_right1.atten(ADC.ATTN_11DB)
    
    pinA = Pin(19, mode=Pin.OUT, pull=None)
    pinB = Pin(18, mode=Pin.OUT, pull=None)
    pinINH = Pin(5, mode=Pin.OUT, pull=None)
    
    for i in range(3000):
        pinINH.value(1)
        pinA.value(0)
        pinB.value(0)
        adc_out1.value(1)
        adc_out_left.value(0)
        adc_out_right.value(0)
        time.sleep_us(10)
        lv = adc_left1.read()
        rv = adc_right1.read()
        time.sleep_us(5)
        adc_out1.value(0)
        
        pinINH.value(0)
        pinA.value(0)
        pinB.value(1)
        adc_out1.value(0)
        adc_out_left.value(1)
        adc_out_right.value(0)
        time.sleep_us(10)
        lv1 = adc_left1.read()
        rv1 = adc_right1.read()
        time.sleep_us(5)
        adc_out1.value(0)
        
        pinINH.value(0)
        pinA.value(1)
        pinB.value(1)
        adc_out1.value(0)
        adc_out_left.value(0)
        adc_out_right.value(1)
        time.sleep_us(10)
        lv2 = adc_left1.read()
        rv2 = adc_right1.read()
        time.sleep_us(5)
        adc_out1.value(0)
        
        print('L,',lv,', R,',rv,'L1,',lv1,', R1,',rv1,'L2,',lv2,', R2,',rv2)
        #print('R-L,', rv-lv)
        time.sleep_ms(30)
        
        
        
if __name__ == '__main__':
    print('Start ir_adc_test()...')
    ir_adc_test()
    print('End ir_adc_test()...')
    
    

