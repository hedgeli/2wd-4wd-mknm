# test.py Test program for IR remote control decoder
# Supports Pyboard, ESP32 and ESP8266

# Author: Peter Hinch
# Copyright Peter Hinch 2020 Released under the MIT license

# Run this to characterise a remote.

from sys import platform
import time
import gc
from machine import Pin, freq
from ir_rx.print_error import print_error  # Optional print of error codes
# Import all implemented classes
from ir_rx.nec import NEC_8, NEC_16
from ir_rx.sony import SONY_12, SONY_15, SONY_20
from ir_rx.philips import RC5_IR, RC6_M0
from ir_rx.mce import MCE

from zyrot_2WD_IR_rawPWM import rawPWM_2WD

import max7219_8x8led_iosimu as max7219

'''
cmd value
front  24
back   82
left   8
right  90
repeat -1
OK     28
'''

rec_cmd = 0

CMD_FRONT = 24
CMD_BACK  = 82
CMD_LEFT  = 8
CMD_RIGHT = 90
CMD_OK    = 28
CMD_REPEAT = -1
CMD_OVER_TIME = -2

zy2wd = rawPWM_2WD()
CMD_TIME_MS  =  200
ir_cmd_duty = 200
ir_cmd_turn_duty = 200

disp_buf = 'R'

ir_rec_stamp_ms = 0

# Define pin according to platform
if platform == 'pyboard':
    p = Pin('X3', Pin.IN)
elif platform == 'esp8266':
    freq(160000000)
    p = Pin(13, Pin.IN)
elif platform == 'esp32' or platform == 'esp32_LoBo':
    p = Pin(19, Pin.IN)
elif platform == 'rp2':
    p = Pin(16, Pin.IN)

# User callback
def cb(data, addr, ctrl):
    global rec_cmd
    global zy2wd
    global disp_buf
    global ir_rec_stamp_ms
    if data < 0:  # NEC protocol sends repeat codes.
        rec_cmd = data
        print('Repeat code:', rec_cmd)
    else:
        rec_cmd = data
        print('rec_cmd:',rec_cmd)
        #print('Data {:02x} Addr {:04x} Ctrl {:02x}'.format(data, addr, ctrl))
        
    ir_rec_stamp_ms = time.ticks_ms()        
    if rec_cmd == CMD_FRONT:
        print('CMD_FRONT')
        max7219.disp_sym(3)
        disp_buf = 's3'
        zy2wd.move(ir_cmd_duty, ir_cmd_duty)
    elif rec_cmd == CMD_BACK:
        print('CMD_BACK')
        max7219.disp_sym(4)
        disp_buf = 's4'
        zy2wd.move(-ir_cmd_duty, -ir_cmd_duty)
    elif rec_cmd == CMD_RIGHT:
        print('CMD_RIGHT')
        max7219.disp_sym(1)
        disp_buf = 's1'
        zy2wd.move(-ir_cmd_turn_duty, ir_cmd_turn_duty)
    elif rec_cmd == CMD_LEFT:
        print('CMD_LEFT')
        max7219.disp_sym(2)
        disp_buf = 's2'
        zy2wd.move(ir_cmd_turn_duty, -ir_cmd_turn_duty)
    elif rec_cmd == CMD_OK:
        print('CMD_OK')
        zy2wd.stop()
    elif rec_cmd == CMD_REPEAT:
        #print('CMD_REPEAT')
        pass
    else:
        pass
                

def test(proto=0):
    global zy2wd
    global disp_buf
    classes = (NEC_8, NEC_16, SONY_12, SONY_15, SONY_20, RC5_IR, RC6_M0, MCE)
    ir = classes[proto](p, cb)  # Instantiate receiver
    ir.error_function(print_error)  # Show debug information
    #ir.verbose = True
    # A real application would do something here...
    global rec_cmd
    global ir_rec_stamp_ms
    
    try:
        while True:
            #print('running')
            time_ms = time.ticks_ms()
            if (time_ms - ir_rec_stamp_ms) >= CMD_TIME_MS:
                rec_cmd = CMD_OVER_TIME
                zy2wd.stop()
                if disp_buf != 'R':
                    max7219.disp_uppercase_char('R')
                    disp_buf = 'R'
            time.sleep_ms(CMD_TIME_MS)
            gc.collect()
    except KeyboardInterrupt:
        ir.close()

# **** DISPLAY GREETING ****
s = '''Test for IR receiver. Run:
from ir_rx.test import test
test() for NEC 8 bit protocol,
test(1) for NEC 16 bit,
test(2) for Sony SIRC 12 bit,
test(3) for Sony SIRC 15 bit,
test(4) for Sony SIRC 20 bit,
test(5) for Philips RC-5 protocol,
test(6) for RC6 mode 0.
test(7) for Microsoft Vista MCE.

Hit ctrl-c to stop, then ctrl-d to soft reset.'''

from beep_music import beep_music_melody
import max7219_8x8led_iosimu as max7219

def main():
    max7219.init_max7219()
    max7219.disp_uppercase_char('R')
    beep_music_melody(8)
    print('Start zy2wd 红外遥控.')
    print(s)
    max7219.init_max7219()
    test(1)

if __name__ == '__main__':
    main()
