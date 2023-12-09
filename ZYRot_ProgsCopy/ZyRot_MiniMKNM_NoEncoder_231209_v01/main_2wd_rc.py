# import dcmot_pos_spe_dualPID
# import time
# # from beep_music import beep_music_melody
# # import max7219_8x8led_iosimu as max7219
# 
# if __name__ == '__main__':
#     start_ms = time.ticks_ms()
#     print('Boot OK. ms:', start_ms)
# #     max7219.init_max7219()
# #     max7219.disp_uppercase_char('T')
# #     beep_music_melody(8)
#     print('start zy2wd_dpid_rc_main()')
#     dcmot_pos_spe_dualPID.pos_spe_dualPID_test()


import time
from zyrot_2wd_dualPid_RC import zy2wd_dpid_rc_main
from beep_music import beep_music_melody, pwm_set_0
import max7219_8x8led_iosimu as max7219
    
if __name__ == '__main__':
    start_ms = time.ticks_ms()
    pwm_set_0()
    print('Boot OK. ms:', start_ms)
    max7219.init_max7219()
    max7219.disp_uppercase_char('R')
    beep_music_melody(8)
    print('start zy2wd_dpid_rc_main()')
    zy2wd_dpid_rc_main()

# import time
# from zyrot_2wd_dualPID_obj import ZYRot_2WD_DPID_Test
#     
# if __name__ == '__main__':
#     start_ms = time.ticks_ms()
#     print('Boot OK. ms:', start_ms)
#     ZYRot_2WD_DPID_Test()

    
