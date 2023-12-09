import zyrot_motctl_regs as mctlregs
from machine import Pin,ADC,PWM
import time
import zyrot_utils


zyrot_4MKNM_paras_dict = {
    'name'        : 'ZYRot_4MKNM',
    'hw_version'  : 200,
    'vxy_scale'   : 8,
    'vw_scale'    : 100,
    'wheel_Dia'   : 52,    # 轮直径52mm
    'wheel_Dist'  : 135,   # 两轮轴距135mm
    '4mknm_length'  : 125,   #前后轴距离125mm
    '4mknm_bodlen' : 250,  # 本体长度250mm
    }
 
L_R_REG_ADDR = 0x0100
L1_REG_ADDR = 0X0101
L2_REG_ADDR = 0x0102
R1_REG_ADDR = 0X0103
R2_REG_ADDR = 0X0104



# zyrot_4MKNM_regs_dict = {
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

LEFT2_FOR_PWM_PIN = 18
LEFT2_BACK_PWM_PIN = 5

RIGHT1_FOR_PWM_PIN = 12
RIGHT1_BACK_PWM_PIN = 13

RIGHT2_FOR_PWM_PIN = 21
RIGHT2_BACK_PWM_PIN = 19

zyrot_4MKNM_pwm_dict = {
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
    print('zyrot_4MKNM pwm_init()')
    pwm_left1_forward = PWM(Pin(LEFT1_FOR_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    pwm_left1_back = PWM(Pin(LEFT1_BACK_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    
    pwm_right1_forward = PWM(Pin(RIGHT1_FOR_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    pwm_right1_back = PWM(Pin(RIGHT1_BACK_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    
    zyrot_4MKNM_pwm_dict['pwm_left1_forward'] = pwm_left1_forward
    zyrot_4MKNM_pwm_dict['pwm_left1_back'] = pwm_left1_back
    
    zyrot_4MKNM_pwm_dict['pwm_right1_forward'] = pwm_right1_forward
    zyrot_4MKNM_pwm_dict['pwm_right1_back'] = pwm_right1_back
    
    pwm_left2_forward = PWM(Pin(LEFT2_FOR_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    pwm_left2_back = PWM(Pin(LEFT2_BACK_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    
    pwm_right2_forward = PWM(Pin(RIGHT2_FOR_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    pwm_right2_back = PWM(Pin(RIGHT2_BACK_PWM_PIN),duty=0,freq=ZYROT_PWM_FREQ)
    
    zyrot_4MKNM_pwm_dict['pwm_left2_forward'] = pwm_left2_forward
    zyrot_4MKNM_pwm_dict['pwm_left2_back'] = pwm_left2_back
    
    zyrot_4MKNM_pwm_dict['pwm_right2_forward'] = pwm_right2_forward
    zyrot_4MKNM_pwm_dict['pwm_right2_back'] = pwm_right2_back
    
    update_pwm_duty()
    
    
def update_pwm_duty():
    pwm_duty = mctlregs.motctl_regs_dict[L1_REG_ADDR]
    if(pwm_duty >= 0):
        zyrot_4MKNM_pwm_dict['pwm_left1_back'].duty(0)
        zyrot_4MKNM_pwm_dict['pwm_left1_forward'].duty(pwm_duty)
    elif(pwm_duty < 0):
        zyrot_4MKNM_pwm_dict['pwm_left1_forward'].duty(0)
        zyrot_4MKNM_pwm_dict['pwm_left1_back'].duty(-pwm_duty)
        
    pwm_duty = mctlregs.motctl_regs_dict[R1_REG_ADDR]
    if(pwm_duty >= 0):
        zyrot_4MKNM_pwm_dict['pwm_right1_back'].duty(0)
        zyrot_4MKNM_pwm_dict['pwm_right1_forward'].duty(pwm_duty)
    elif(pwm_duty < 0):
        zyrot_4MKNM_pwm_dict['pwm_right1_forward'].duty(0)
        zyrot_4MKNM_pwm_dict['pwm_right1_back'].duty(-pwm_duty)
        
    pwm_duty = mctlregs.motctl_regs_dict[L2_REG_ADDR]
    if(pwm_duty >= 0):
        zyrot_4MKNM_pwm_dict['pwm_left2_back'].duty(0)
        zyrot_4MKNM_pwm_dict['pwm_left2_forward'].duty(pwm_duty)
    elif(pwm_duty < 0):
        zyrot_4MKNM_pwm_dict['pwm_left2_forward'].duty(0)
        zyrot_4MKNM_pwm_dict['pwm_left2_back'].duty(-pwm_duty)
        
    pwm_duty = mctlregs.motctl_regs_dict[R2_REG_ADDR]
    if(pwm_duty >= 0):
        zyrot_4MKNM_pwm_dict['pwm_right2_back'].duty(0)
        zyrot_4MKNM_pwm_dict['pwm_right2_forward'].duty(pwm_duty)
    elif(pwm_duty < 0):
        zyrot_4MKNM_pwm_dict['pwm_right2_forward'].duty(0)
        zyrot_4MKNM_pwm_dict['pwm_right2_back'].duty(-pwm_duty)
        
        
def joystick_mknm_updata_pwm(vy=0, vx=0, vw=0):
    # a = W/2, b = L/2
    # vl1 = vy + vx - vw(a+b)
    # vl2 = vy - vx - vw(a+b)
    # vr1 = vy - vx + vw(a+b)
    # vr2 = vy + vx + vw(a+b)
    a = zyrot_4MKNM_paras_dict['wheel_Dist']/2
    b = zyrot_4MKNM_paras_dict['4mknm_length']/2
    vw_div_scale = zyrot_4MKNM_paras_dict['vw_scale']
    a_b = int((a + b)/2)
    
    vl1 = int(vy+vx+vw*a_b/vw_div_scale)
    vl2 = int(vy-vx-vw*a_b/vw_div_scale)
    
    vr1 = int(vy-vx+vw*a_b/vw_div_scale)
    vr2 = int(vy+vx-vw*a_b/vw_div_scale)
    
    vscale = zyrot_4MKNM_paras_dict['vxy_scale']
    vl1 = zyrot_utils.limit_max_min(vl1*vscale)
    vl2 = zyrot_utils.limit_max_min(vl2*vscale)
    vr1 = zyrot_utils.limit_max_min(vr1*vscale)
    vr2 = zyrot_utils.limit_max_min(vr2*vscale)
    
    mctlregs.set_regs_val(4,L1_REG_ADDR,[vl1,vl2,vr1,vr2])
    update_pwm_duty()
    
    
def mknm_update_regs_pwm(regnum, regaddr, vals):
#     mctlregs.set_regs_val(regnum,regaddr,vals)
    vx = 0
    vy = 0
    vw = 0
#     print('regaddr:',regaddr,'fcode addr base:',mctlregs.FCODE_REG_ADDR_BASE)
    if regaddr == mctlregs.FCODE_REG_ADDR_BASE:
#         print('vals[0]:',vals[0], '    fcode:', mctlregs.FCODE_FORWARD)
        if vals[0]&0xffff == mctlregs.FCODE_FORWARD:
            vy = mctlregs.motctl_regs_dict[mctlregs.FCODE_REG_ADDR_PARA1]
#             print('Forward:',vy)
        elif vals[0]&0xffff == mctlregs.FCODE_BACK:
            vy = -mctlregs.motctl_regs_dict[mctlregs.FCODE_REG_ADDR_PARA1]
#             print('Back:',vy)
        elif vals[0]&0xffff == mctlregs.FCODE_LEFT:
            vx = mctlregs.motctl_regs_dict[mctlregs.FCODE_REG_ADDR_PARA1]
#             print('Left:',vx)
        elif vals[0]&0xffff == mctlregs.FCODE_RIGHT:
            vx = -mctlregs.motctl_regs_dict[mctlregs.FCODE_REG_ADDR_PARA1]
#             print('Right:',vx)
        elif vals[0]&0xffff == mctlregs.FCODE_TURN_LEFT:
            vw = mctlregs.motctl_regs_dict[mctlregs.FCODE_REG_ADDR_PARA1]
#             print('Turn left:',vw)
        elif vals[0]&0xffff == mctlregs.FCODE_TURN_RIGHT:
            vw = -mctlregs.motctl_regs_dict[mctlregs.FCODE_REG_ADDR_PARA1]
#             print('Turn right:',vw)
            
    elif regaddr == mctlregs.JOYSTICK_REG_ADDR_BASE:
        vy = mctlregs.motctl_regs_dict[mctlregs.JOYSTICK_Y_REG_ADDR]
        vx = mctlregs.motctl_regs_dict[mctlregs.JOYSTICK_X_REG_ADDR]
        vw = 0  #mctlregs.motctl_regs_dict[zy4mknm.JOYSTICK_ANGSPE_REG_ADDR]
    joystick_mknm_updata_pwm(vy,vx,vw)
    
    
def joystick_4mknm_test():
    print('Start joystick_4mknm_test()')
    pwm_init()
    update_pwm_duty()
    time.sleep_ms(1000)
    for i in range(5):
        print('joystick_4mknm_test() cnt:', i)
        joystick_mknm_updata_pwm(500,0,0)
        time.sleep_ms(2000)
        joystick_mknm_updata_pwm(0,0,0)
        time.sleep_ms(1000)
        joystick_mknm_updata_pwm(-500,0,0)
        time.sleep_ms(2000)
        joystick_mknm_updata_pwm(0,0,0)
        time.sleep_ms(1000)
        
        joystick_mknm_updata_pwm(0,500,0)
        time.sleep_ms(2000)
        joystick_mknm_updata_pwm(0,0,0)
        time.sleep_ms(1000)
        joystick_mknm_updata_pwm(0,-500,0)
        time.sleep_ms(2000)
        joystick_mknm_updata_pwm(0,0,0)
        time.sleep_ms(1000)
    
    
def zyrot_4MKNM_test():
    import time
    print('Start zyrot_4MKNM_test()')
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
    print(zyrot_4MKNM_paras_dict)



if __name__ == '__main__':
    print_robot_info()
    #zyrot_4MKNM_test()
    joystick_4mknm_test()



