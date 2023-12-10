import zyrot_motctl_regs as mctlregs
from machine import Pin,ADC,PWM
import time
from servo_3line import Servo
import zyrot_utils as utils

SERVO1_PWM_PIN = 26
SERVO2_PWM_PIN = 15

SERVO3_PWM_PIN = 23
SERVO4_PWM_PIN = 22

ANGLE1_REG_ADDR = 0X0201
ANGLE2_REG_ADDR = 0X0202
ANGLE3_REG_ADDR = 0X0203
ANGLE4_REG_ADDR = 0X0204

zyrot_arm_4servo_dict = {
    'servo1'    :  [],
    'servo2'    :  [],
    'servo3'    :  [],
    'servo4'    :  []
    }

zyrot_servo_angle_dict = {
    'angle1'   : 0,
    'angle2'   : 0,
    'angle3'   : 0,
    'angle4'   : 0,
    }


def init_arm_4servo():
    print('arm_4servo_init()')
    zyrot_arm_4servo_dict['servo1'] = Servo(Pin(SERVO1_PWM_PIN))
    zyrot_arm_4servo_dict['servo2'] = Servo(Pin(SERVO2_PWM_PIN))
    zyrot_arm_4servo_dict['servo3'] = Servo(Pin(SERVO3_PWM_PIN))
    zyrot_arm_4servo_dict['servo4'] = Servo(Pin(SERVO4_PWM_PIN))
    
def update_arm_4servo_angle():
#     print('update_arm_4servo_angle()')
    angle1 = int((mctlregs.motctl_regs_dict[ANGLE1_REG_ADDR]+1023)*180/2046)    # todo change the app value min and max 
    angle2 = int((mctlregs.motctl_regs_dict[ANGLE2_REG_ADDR]+1023)*180/2046)
    angle3 = int((mctlregs.motctl_regs_dict[ANGLE3_REG_ADDR]+1023)*180/2046)
    angle4 = int((mctlregs.motctl_regs_dict[ANGLE4_REG_ADDR]+1023)*180/2046)
    angle1 = utils.limit_max_min(angle1, 0 ,180)
    angle2 = utils.limit_max_min(angle2, 0 ,180)
    angle3 = utils.limit_max_min(angle3, 0 ,180)
    angle4 = utils.limit_max_min(angle4, 0 ,180)
    zyrot_servo_angle_dict['angle1'] = angle1
    zyrot_servo_angle_dict['angle2'] = angle2
    zyrot_servo_angle_dict['angle3'] = angle3
    zyrot_servo_angle_dict['angle4'] = angle4
    
    zyrot_arm_4servo_dict['servo1'].write_angle(angle1)
    zyrot_arm_4servo_dict['servo2'].write_angle(angle2)
    zyrot_arm_4servo_dict['servo3'].write_angle(angle3)
    zyrot_arm_4servo_dict['servo4'].write_angle(angle4)
    
    
    
def arm_4servo_test():
    print('arm_4servo_test()')
    init_arm_4servo()
    
    for i in range(10):
        print('servo_3line_test():', i)
        print('set angle 0')
        zyrot_arm_4servo_dict['servo1'].write_angle(0)
        zyrot_arm_4servo_dict['servo2'].write_angle(0)
        zyrot_arm_4servo_dict['servo3'].write_angle(0)
        zyrot_arm_4servo_dict['servo4'].write_angle(0)
        time.sleep_ms(1500)
        print('set angle 180')
        zyrot_arm_4servo_dict['servo1'].write_angle(180)
        zyrot_arm_4servo_dict['servo2'].write_angle(180)
        zyrot_arm_4servo_dict['servo3'].write_angle(180)
        zyrot_arm_4servo_dict['servo4'].write_angle(180)
        time.sleep_ms(1500)
        print('set angle 90')
        zyrot_arm_4servo_dict['servo1'].write_angle(90)
        zyrot_arm_4servo_dict['servo2'].write_angle(90)
        zyrot_arm_4servo_dict['servo3'].write_angle(90)
        zyrot_arm_4servo_dict['servo4'].write_angle(90)
        time.sleep_ms(1500)
    
    
if __name__ == '__main__':
    arm_4servo_test()
    


