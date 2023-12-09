'''
ROBOT_NAME option:
    ZYRot_2WD_CIRCLE
    ZYRot_4MKNM
    ZYRot_4WD
'''



ROBOT_NAME = 'ZYRot_DPIC_2WD_D41'
ARM_TYPE = 'NO_ARM'    # ARM_4X3L_SERVO

'''
0:  no debug log
1:  commulation log
2:  parse log
4:  motor position log
8:  
'''
NO_LOG = 0
COMM_LOG = 1
PARSE_LOG = 2
MOTOR_POS_LOG = 4

LOG_LEVEL = NO_LOG

#
MOTOR_PID_NO_LOG = 0
MOTOR_PID_LOG  = 1
motor_pid_log_level = MOTOR_PID_NO_LOG

MOVE_MODE_NO_BLOCK = 0
MOVE_MODE_BLOCK  = 1   #
MIN_MOVE_TIME_S  = 0.05

move_add_time_ms = 550


SSID_F = 'ZYRot_4MKNM_'
PWD = '12345678'
PORT = 12345

WHEEL_D_mm = 41   # for mini2WD 41mm
WHEEL_LR_DIS = 95


BOARD_VER = 'V1.X'
VIN5V_ADC_PIN = 34
USB_V_ADC_TH  = 1500

CHARGE_MODE_DEEPSLEEP = True
#CHARGE_MODE_DEEPSLEEP = False

RC_LOST_CONN_TIME_MS = 1100


