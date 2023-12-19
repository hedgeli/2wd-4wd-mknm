
from machine import Pin, ADC
import time

def get_batt_voltage():
    adc_batt = ADC(Pin(35))
    adc_batt.atten(ADC.ATTN_11DB)
    vad = adc_batt.read()
    batt_vol = int(vad*2*3600/4095)
    return batt_vol

if __name__ == '__main__':
    vol = get_batt_voltage()
    print("bat vol:", vol)
    
    for i in range(100):
        vol = get_batt_voltage()
        print("bat vol:", vol)
        time.sleep_ms(200)


