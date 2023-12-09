from machine import UART
import time
from machine import Pin
# GPIO16->RX2  GPIO17->TX2
uart2 = UART(2, 115200)
uart2.init(115200, bits=8, parity=None, stop=1)
time.sleep_ms(100)

# FA AF 09 01 00 20 00 20 4a ED
# change id from 0x09 to 0x10
# FA AF 09 cd 00 10 00 00 e6 ED

print("Blue LED in Pin-2")
blueLed = Pin(2,Pin.OUT)
# ang_000_cmd = bytearray([0x00, 0x00, 0xFA,0xAF,0x00,0x01,0x00,0x20,0x00,0x20,0x41,0xED])
# ang_120_cmd = bytearray([0x00, 0x00, 0xFA,0xAF,0x00,0x01,0x78,0x20,0x00,0x20,0xB9,0xED])
# ang_240_cmd = bytearray([0x00, 0x00, 0xFA,0xAF,0x00,0x01,0xF0,0x20,0x00,0x20,0x31,0xED])

max_angle = 240
min_angle = 0
zero_pos_angle = 120
# Servo direction is anticlockwise
servo_direction = -1

max_ID = 240
broad_ID = 0

CMD_SET_ANGLE = 0x01

import math

base_L = 41.00
# print(base_L)
arm_up1_L = 80.0
arm_up2_L = 105.0

arm_down1_L = 80.0
arm_down2_L = 105.0

g_goal_x = 35.0
g_goal_y = 0.0

g_debug_info = 1

g_position_arr = [[50, 0],[50,-50],[50,-100],[100,-100],[150,-50],[150,0],[150,50],[100,100],[50,100],[50,50]]


# Base up point is (0, 20.5)    (0, base_L/2)
# Base down point is (0, -20.5) (0, -base_L/2)

def calc_back(goal_x, goal_y):
    ang_up = 0.0
    ang_down = 0.0

    v_arm_up_L = math.sqrt(goal_x*goal_x + (goal_y-base_L/2)*(goal_y-base_L/2))
    v_arm_down_L = math.sqrt(goal_x*goal_x + (goal_y+base_L/2)*(goal_y+base_L/2))
    #print("v_arm_up_L:"+str(v_arm_up_L))
    #print("v_arm_down_L:" + str(v_arm_down_L))

    cos_angle_up1 = (arm_up1_L*arm_up1_L)+(v_arm_up_L*v_arm_up_L)-(arm_up2_L*arm_up2_L)
    cos_angle_up1 = cos_angle_up1/(2*arm_up1_L*v_arm_up_L)
    cos_angle_down1 = (arm_down1_L*arm_down1_L)+(v_arm_down_L*v_arm_down_L)-(arm_down2_L*arm_down2_L)
    cos_angle_down1 = cos_angle_down1/(2*arm_down1_L*v_arm_down_L)
    #print("cos_angle_up1:"+str(cos_angle_up1))
    #print("cos_angle_down1:" + str(cos_angle_down1))

    angle_up_t1 = math.acos(cos_angle_up1)
    angle_down_t1 = math.acos(cos_angle_down1)
    #print("angle_up_t1:"+str(angle_up_t1*180/math.pi)+"  degree")
    #print("angle_down_t1:" + str(angle_down_t1*180/math.pi)+"  degree")

    cos_angle_up_v1 = (base_L*base_L)+(v_arm_up_L*v_arm_up_L)-(v_arm_down_L*v_arm_down_L)
    cos_angle_up_v1 = cos_angle_up_v1/(2*base_L*v_arm_up_L)
    cos_angle_down_v1 = (base_L*base_L)+(v_arm_down_L*v_arm_down_L)-(v_arm_up_L*v_arm_up_L)
    cos_angle_down_v1 = cos_angle_down_v1/(2*base_L*v_arm_down_L)
    #print("cos_angle_up_v1:"+str(cos_angle_up_v1))
    #print("cos_angle_down_v1:" + str(cos_angle_down_v1))

    angle_up_v1 = math.acos(cos_angle_up_v1)
    angle_down_v1 = math.acos(cos_angle_down_v1)
    #print("angle_up_v1:"+str(angle_up_v1*180/math.pi)+"  degree")
    #print("angle_down_v1:" + str(angle_down_v1*180/math.pi)+"  degree")

    ang_up = angle_up_v1 + angle_up_t1 - math.pi/2
    ang_down = math.pi/2 - angle_down_t1 - angle_down_v1

    print("ang_up:" + str(ang_up * 180 / math.pi) + "  degree")
    print("ang_down:" + str(ang_down * 180 / math.pi) + "  degree")
    
    # return angle in dgeree !!!
    ang_up = int(ang_up * 180 / math.pi + 0.5)
    ang_down = int(ang_down * 180 / math.pi + 0.5)

    return ang_up, ang_down



def cal_back_test():
    position_arr = [[50, 0],[50,-50],[50,-100],[100,-100],[150,-50],[150,0],[150,50],[100,100],[50,100],[50,50]]
    for poi in position_arr:
        ang_u, ang_d = calc_back(poi[0],poi[1])
        print("ang_u:%d" % ang_u)
        print(ang_u)
        print("ang_d:%d" % ang_d)
        print(ang_d)
        print("-----")


def print_hex(bytes):
    l = [hex(int(i)) for i in bytes]
    print(' '.join(l))

def send_angle(uart, ID=0, angle=120, move_time=0, lock_time=0):
    ang_ba = bytearray([0x00, 0x00, 0xFA,0xAF,0x00,0x01,0x00,0x20,0x00,0x20,0x41,0xED,0x00,0x0a,0x0d])
    if angle > max_angle:
        angle = max_angle
    if angle < min_angle:
        angle = min_angle
    if ID > max_ID:
        ID = max_ID
    if ID < broad_ID:
        ID = broad_ID
    ang_ba[4] = ID
    ang_ba[5] = CMD_SET_ANGLE
    ang_ba[6] = angle
    ang_ba[7] = move_time%256
    ang_ba[8] = int(lock_time/256)
    ang_ba[9] = int(lock_time%256)
    
    check_sum = ang_ba[4] + ang_ba[5] + ang_ba[6] + ang_ba[7] + ang_ba[8] + ang_ba[9]
        
    ang_ba[10] = check_sum % 256
    #print_hex(ang_ba)
    #time.sleep_ms(10)
    uart.write(ang_ba)
    time.sleep_ms(5)


#send_angle(uart, ID=0, angle=120, move_time=0, lock_time=0)
#send_angle(0,9,120)
#send_angle(uart=0, ID=0, angle=0, move_time=32, lock_time=32)
'''
while 1:
    print("Start to Scara robot test...")
    for i in range(30):
        print("send %d:" % i)
        send_angle(uart2, ID=0, angle=(i-15)*5+120, move_time=0, lock_time=0)
        blueLed.value(1)
        time.sleep_ms(500)
        blueLed.value(0)
        time.sleep_ms(500)
    print("End of Scara robot test")
'''

#cal_back_test()

id_servo_up = 0x10
id_servo_down = 0x09
while 1:
    i = 0
    for poi in g_position_arr:
        print('Point X: %d' % i)
        i = i + 1
        ang_u, ang_d = calc_back(poi[0],poi[1])
        ang_servo_up = zero_pos_angle + ang_u*servo_direction
        ang_servo_down = zero_pos_angle + ang_d*servo_direction
        
        send_angle(uart2, ID=id_servo_up, angle=int(ang_servo_up), move_time=0, lock_time=0)
        time.sleep_ms(20)
        send_angle(uart2, ID=id_servo_down, angle=int(ang_servo_down), move_time=0, lock_time=0)
        time.sleep_ms(20)
        blueLed.value(1)
        time.sleep_ms(1000)
        blueLed.value(0)
        time.sleep_ms(500)
    print("Test over a circle")






