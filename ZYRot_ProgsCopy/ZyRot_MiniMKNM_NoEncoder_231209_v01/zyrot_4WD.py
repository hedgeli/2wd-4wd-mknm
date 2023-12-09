import zyrot_motctl_regs as mctlregs
from machine import Pin,ADC,PWM
import time


zyrot_4WD_paras_dict = {
    'name'        : 'ZYRot_4WD',
    'hw_version'  : 100,
    'wheel_Dia'   : 65,    # 轮直径65mm
    'wheel_Dist'  : 135,   # 两轮轴距135mm
    'rot4wd_Dia'  : 255,   # 本体直径255mm
    }
 
L_R_REG_ADDR = 0x0100
L1_REG_ADDR = 0X0101
L2_REG_ADDR = 0x0102
R1_REG_ADDR = 0X0103
R2_REG_ADDR = 0X0104

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

LEFT1_FOR_PWM_PIN = 27
LEFT1_BACK_PWM_PIN = 14

LEFT2_FOR_PWM_PIN = 5
LEFT2_BACK_PWM_PIN = 18

RIGHT1_FOR_PWM_PIN = 12
RIGHT1_BACK_PWM_PIN = 13

RIGHT2_FOR_PWM_PIN = 19
RIGHT2_BACK_PWM_PIN = 21

zyrot_4WD_pwm_dict = {
    'pwm_left1_forward'    :  [],
    'pwm_left1_back'       :  [],
    'pwm_right1_forward'   :  [],
    'pwm_right1_back'      :  [],
    
    'pwm_left2_forward'    :  [],
    'pwm_left2_back'       :  [],
    'pwm_right2_forward'   :  [],
    'pwm_right2_back'      :  []
    }


# def update_4wd_regs():
#     zyrot_4WD_regs_dict['L1MotDuty'] = mctlregs.motctl_regs_dict[L_REG_ADDR]
#     zyrot_4WD_regs_dict['R1MotDuty'] = mctlregs.motctl_regs_dict[R_REG_ADDR]
#     zyrot_4WD_regs_dict['L_RMotDuty'] = mctlregs.motctl_regs_dict[L_R_REG_ADDR]
    
def pwm_init():
    print('zyrot_4WD pwm_init()')
    pwm_left1_forward = PWM(Pin(LEFT1_FOR_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    pwm_left1_back = PWM(Pin(LEFT1_BACK_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    
    pwm_right1_forward = PWM(Pin(RIGHT1_FOR_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    pwm_right1_back = PWM(Pin(RIGHT1_BACK_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    
    zyrot_4WD_pwm_dict['pwm_left1_forward'] = pwm_left1_forward
    zyrot_4WD_pwm_dict['pwm_left1_back'] = pwm_left1_back
    
    zyrot_4WD_pwm_dict['pwm_right1_forward'] = pwm_right1_forward
    zyrot_4WD_pwm_dict['pwm_right1_back'] = pwm_right1_back
    
    pwm_left2_forward = PWM(Pin(LEFT2_FOR_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    pwm_left2_back = PWM(Pin(LEFT2_BACK_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    
    pwm_right2_forward = PWM(Pin(RIGHT2_FOR_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    pwm_right2_back = PWM(Pin(RIGHT2_BACK_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    
    zyrot_4WD_pwm_dict['pwm_left2_forward'] = pwm_left2_forward
    zyrot_4WD_pwm_dict['pwm_left2_back'] = pwm_left2_back
    
    zyrot_4WD_pwm_dict['pwm_right2_forward'] = pwm_right2_forward
    zyrot_4WD_pwm_dict['pwm_right2_back'] = pwm_right2_back
    
    update_pwm_duty()
    
    
def update_pwm_duty():
    pwm_duty = mctlregs.motctl_regs_dict[L1_REG_ADDR]
    if(pwm_duty >= 0):
        zyrot_4WD_pwm_dict['pwm_left1_back'].duty(0)
        zyrot_4WD_pwm_dict['pwm_left1_forward'].duty(pwm_duty)
    elif(pwm_duty < 0):
        zyrot_4WD_pwm_dict['pwm_left1_forward'].duty(0)
        zyrot_4WD_pwm_dict['pwm_left1_back'].duty(-pwm_duty)
        
    pwm_duty = mctlregs.motctl_regs_dict[R1_REG_ADDR]
    if(pwm_duty >= 0):
        zyrot_4WD_pwm_dict['pwm_right1_back'].duty(0)
        zyrot_4WD_pwm_dict['pwm_right1_forward'].duty(pwm_duty)
    elif(pwm_duty < 0):
        zyrot_4WD_pwm_dict['pwm_right1_forward'].duty(0)
        zyrot_4WD_pwm_dict['pwm_right1_back'].duty(-pwm_duty)
        
    pwm_duty = mctlregs.motctl_regs_dict[L2_REG_ADDR]
    if(pwm_duty >= 0):
        zyrot_4WD_pwm_dict['pwm_left2_back'].duty(0)
        zyrot_4WD_pwm_dict['pwm_left2_forward'].duty(pwm_duty)
    elif(pwm_duty < 0):
        zyrot_4WD_pwm_dict['pwm_left2_forward'].duty(0)
        zyrot_4WD_pwm_dict['pwm_left2_back'].duty(-pwm_duty)
        
    pwm_duty = mctlregs.motctl_regs_dict[R2_REG_ADDR]
    if(pwm_duty >= 0):
        zyrot_4WD_pwm_dict['pwm_right2_back'].duty(0)
        zyrot_4WD_pwm_dict['pwm_right2_forward'].duty(pwm_duty)
    elif(pwm_duty < 0):
        zyrot_4WD_pwm_dict['pwm_right2_forward'].duty(0)
        zyrot_4WD_pwm_dict['pwm_right2_back'].duty(-pwm_duty)
    
    
def zyrot_4wd_test():
    import time
    print('Start zyrot_4wd_test()')
    pwm_init()
    update_pwm_duty()
    time.sleep_ms(1000)
    
    for i in range(5):
        print('test cnt:',i)
        mctlregs.set_regs_val(4,L1_REG_ADDR,[PWM_TEST_DUTY,PWM_TEST_DUTY,PWM_TEST_DUTY,PWM_TEST_DUTY])
        update_pwm_duty()
        time.sleep_ms(1000)
        mctlregs.set_regs_val(4,L1_REG_ADDR,[0,0,0,0])
        update_pwm_duty()
        time.sleep_ms(100)
        mctlregs.set_regs_val(4,L1_REG_ADDR,[-PWM_TEST_DUTY,-PWM_TEST_DUTY,-PWM_TEST_DUTY,-PWM_TEST_DUTY])
        update_pwm_duty()
        time.sleep_ms(1000)
        
    mctlregs.set_regs_val(4,L1_REG_ADDR,[0,0,0,0])
    update_pwm_duty()
    

def print_robot_info():
    print(zyrot_4WD_paras_dict)
#     print(zyrot_2WD_regs_dict)


if __name__ == '__main__':
    print_robot_info()
    zyrot_4wd_test()


