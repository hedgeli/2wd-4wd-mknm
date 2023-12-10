from machine import Pin, ADC
import time


def ir_adc_test():
    adc_out1 = Pin(4, mode=Pin.OUT, pull=None)
    adc_left1 = ADC(Pin(36))  # adc0 vp
    adc_right1 = ADC(Pin(39))  # adc3 vn
    adc_left1.atten(ADC.ATTN_11DB)
    adc_right1.atten(ADC.ATTN_11DB)
    
    for i in range(3000):
        adc_out1.value(1)
        time.sleep_us(10)
        lv = adc_left1.read()
        rv = adc_right1.read()
        time.sleep_us(5)
        adc_out1.value(0)
        print('L,',lv,', R,',rv)
        #print('R-L,', rv-lv)
        time.sleep_ms(30)
        
        
        
if __name__ == '__main__':
    print('Start ir_adc_test()...')
    ir_adc_test()
    print('End ir_adc_test()...')
    
    

