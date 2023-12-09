import zyrot_motctl_regs as mctlregs
from machine import Pin,ADC,PWM
import time

'''
send left right pwm 400 401:
fa 01 10 00 0c 01 01 01 90 01 91 00 67 00 68 00 69 00 6a 00 6b 00 6c 00 6d 00 6e 00 6f 00 65 06 64 fe
send left right pwm -400 -401:
fa 01 10 00 0c 01 01 fe 70 fe 6f ff 99 ff 98 ff 97 ff 96 ff 95 ff 94 ff 93 ff 92 ff 91 ff 9b 13 c2 fe
send left right pwm 0 0:
fa 01 10 00 0c 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 19 fe

'''

zyrot_2WD_paras_dict = {
    'name'        : 'ZYRot_2WD_CIRCLE',
    'hw_version'  : 100,
    'wheel_Dia'   : 68,    # 轮直径68mm
    'wheel_Dist'  : 118,   # 两轮轴距118mm
    'rot2wd_Dia'  : 145,   # 本体直径145mm
    }
 
L_R_REG_ADDR = 0x0100
L_REG_ADDR = 0X0101
R_REG_ADDR = 0X0102

# zyrot_2WD_regs_dict = {
# #     0x5100  :  0  ,
# #     0x5101  :  0  ,    # NO 1~6 DC motor PWM duty value, each -1000 ~ +1000
# #     0x5102  :  0  ,
#     'L_RMotDuty'  :  0,
#     'LMotDuty'    :  0,
#     'RMotDuty'    :  0,
#     }

ZYROT_PWM_FREQ = 500
PWM_TEST_DUTY = 300

LEFT_FOR_PWM_PIN = 27
LEFT_BACK_PWM_PIN = 14

RIGHT_FOR_PWM_PIN = 12
RIGHT_BACK_PWM_PIN = 13

zyrot_2WD_pwm_dict = {
    'pwm_left_forward'    :  [],
    'pwm_left_back'       :  [],
    'pwm_right_forward'   :  [],
    'pwm_right_back'      :  []
    }


def update_2wd_regs():
    zyrot_2WD_regs_dict['LMotDuty'] = mctlregs.motctl_regs_dict[L_REG_ADDR]
    zyrot_2WD_regs_dict['RMotDuty'] = mctlregs.motctl_regs_dict[R_REG_ADDR]
    zyrot_2WD_regs_dict['L_RMotDuty'] = mctlregs.motctl_regs_dict[L_R_REG_ADDR]
    
def pwm_init():
    print('zyrot_2WD pwm_init()')
    pwm_left_forward = PWM(Pin(LEFT_FOR_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    pwm_left_back = PWM(Pin(LEFT_BACK_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    
    pwm_right_forward = PWM(Pin(RIGHT_FOR_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    pwm_right_back = PWM(Pin(RIGHT_BACK_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    
    zyrot_2WD_pwm_dict['pwm_left_forward'] = pwm_left_forward
    zyrot_2WD_pwm_dict['pwm_left_back'] = pwm_left_back
    
    zyrot_2WD_pwm_dict['pwm_right_forward'] = pwm_right_forward
    zyrot_2WD_pwm_dict['pwm_right_back'] = pwm_right_back
    
    update_pwm_duty()
    
    
def update_pwm_duty():
    pwm_duty = mctlregs.motctl_regs_dict[L_REG_ADDR]
    if(pwm_duty >= 0):
        zyrot_2WD_pwm_dict['pwm_left_back'].duty(0)
        zyrot_2WD_pwm_dict['pwm_left_forward'].duty(pwm_duty)
    elif(pwm_duty < 0):
        zyrot_2WD_pwm_dict['pwm_left_forward'].duty(0)
        zyrot_2WD_pwm_dict['pwm_left_back'].duty(-pwm_duty)
        
    pwm_duty = mctlregs.motctl_regs_dict[R_REG_ADDR]
    if(pwm_duty >= 0):
        zyrot_2WD_pwm_dict['pwm_right_back'].duty(0)
        zyrot_2WD_pwm_dict['pwm_right_forward'].duty(pwm_duty)
    elif(pwm_duty < 0):
        zyrot_2WD_pwm_dict['pwm_right_forward'].duty(0)
        zyrot_2WD_pwm_dict['pwm_right_back'].duty(-pwm_duty)
    
    
def zyrot_2wd_test(test_duty = PWM_TEST_DUTY):
    import time
    print('Start zyrot_2wd_test()')
    pwm_init()
    update_pwm_duty()
    time.sleep_ms(1000)
    
    for i in range(5):
        print('test cnt:',i)
        mctlregs.set_regs_val(2,L_REG_ADDR,[test_duty,test_duty])
        update_pwm_duty()
        time.sleep_ms(1000)
        mctlregs.set_regs_val(2,L_REG_ADDR,[0,0])
        update_pwm_duty()
        time.sleep_ms(100)
        mctlregs.set_regs_val(2,L_REG_ADDR,[-test_duty,-test_duty])
        update_pwm_duty()
        time.sleep_ms(1000)
        
    mctlregs.set_regs_val(2,L_REG_ADDR,[0,0])
    update_pwm_duty()
    

def print_robot_info():
    print(zyrot_2WD_paras_dict)
#     print(zyrot_2WD_regs_dict)


if __name__ == '__main__':
    print_robot_info()
    zyrot_2wd_test()

