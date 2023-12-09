from machine import Pin, ADC
import time

ADC_MAX_VOL = 3450

def print_voltage():
    adc_batt = ADC(Pin(35))
    adc_usb = ADC(Pin(4))
    adc_batt.atten(ADC.ATTN_11DB)
    adc_usb.atten(ADC.ATTN_11DB)
    for i in range(20):
        vad = adc_batt.read()
        batt_vol = int(vad*2*ADC_MAX_VOL/4095)
        print('batt_vol:', batt_vol,'mV', end='    ')
        vad_usb = adc_usb.read()
        usb_vol = int(vad_usb*2*ADC_MAX_VOL/4095)
        print('usb_vol:', usb_vol,'mV')
        time.sleep_ms(100)
        
        
def get_batt_voltage():
    adc_batt = ADC(Pin(35))
    adc_batt.atten(ADC.ATTN_11DB)
    vad = adc_batt.read()
    batt_vol = int(vad*2*ADC_MAX_VOL/4095)
    return batt_vol


def get_usb_voltage():
    adc_usb = ADC(Pin(4))
    adc_usb.atten(ADC.ATTN_11DB)
    vad = adc_usb.read()
    usb_vol = int(vad*2*ADC_MAX_VOL/4095)
    return usb_vol
    

if __name__ == '__main__':
    print_voltage()



