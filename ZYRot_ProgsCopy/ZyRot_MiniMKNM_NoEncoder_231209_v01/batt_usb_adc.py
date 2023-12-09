from machine import Pin, ADC
import time
import zyrot_config

from max7219_8x8led_iosimu import disp_num, init_max7219

def print_voltage():
    adc_batt = ADC(Pin(35))
    adc_usb = ADC(Pin(zyrot_config.VIN5V_ADC_PIN))
    adc_batt.atten(ADC.ATTN_11DB)
    adc_usb.atten(ADC.ATTN_11DB)
    
    init_max7219()
    
    for i in range(50):
        time.sleep_ms(100)
        vad = adc_batt.read()
        batt_vol = int(vad*2*3600/4095)
        print('batt_vol:', batt_vol,'mV', end='    ')
        vad_usb = adc_usb.read()
        usb_vol = int(vad_usb*2*3600/4095)
        print('usb_vol:', usb_vol,'mV')
        disp_num(usb_vol//100)
        time.sleep_ms(100)
        
        
def get_batt_voltage():
    adc_batt = ADC(Pin(35))
    adc_batt.atten(ADC.ATTN_11DB)
    vad = adc_batt.read()
    batt_vol = int(vad*2*3600/4095)
    return batt_vol


def get_usb_voltage():
    adc_usb = ADC(Pin(zyrot_config.VIN5V_ADC_PIN))
    adc_usb.atten(ADC.ATTN_11DB)
    vad = adc_usb.read()
    usb_vol = int(vad*2*3600/4095)
    return usb_vol
     

if __name__ == '__main__':
    print_voltage()



