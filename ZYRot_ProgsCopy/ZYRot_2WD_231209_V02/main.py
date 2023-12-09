# import pwm_motor_test
# pwm_motor_test.pwm_init()
# import umodbus
# import uasyncio
# import time
# from dgram import UDPServer
# 
# import udpRawProtrol as udprpl
# import zyrot_motctl_regs as mctlregs
# import zyrot_config as config
# # import zyrot_2WD as zy2wd
# import zyrot_4WD as zy4wd
# import zyrot_arm_4servo as arm4s
# import zyrot_4MKNM as zy4mknm
# 
# 
# rec_cnt = 0
# 
# 
# def cb(msg, addr):
#     global rec_cnt
#     rec_cnt = rec_cnt+1
#     if config.LOG_LEVEL&config.PARSE_LOG > 0:
#         print('cnt:', rec_cnt, '++++',time.ticks_ms(),'Got:', msg)
#     parsed_vals = udprpl.parse_recv_bytearr(msg)
#     if config.LOG_LEVEL&config.PARSE_LOG > 0:
#         print('parsed_vals:', parsed_vals)
#     if parsed_vals == []:
#         return 
#     if parsed_vals['fcode'] == udprpl.FCODE_WRITE_REGS:
#         mctlregs.set_regs_val(parsed_vals['regNum'][0],parsed_vals['regAddr'][0],parsed_vals['datas'])
# #         print(mctlregs.motctl_regs_dict)
# #         if config.ROBOT_NAME == zy2wd.zyrot_2WD_paras_dict['name']:
# # #             print('udp cb update pwm duty.')
# #             zy2wd.update_pwm_duty()
#         if config.ROBOT_NAME == zy4wd.zyrot_4WD_paras_dict['name']:
# #             print('udp cb update pwm duty.')
#             zy4wd.update_pwm_duty()
#         if config.ROBOT_NAME == zy4mknm.zyrot_4MKNM_paras_dict['name']:
# #             vy = mctlregs.motctl_regs_dict[zy4mknm.JOYSTICK_Y_REG_ADDR]
# #             vx = mctlregs.motctl_regs_dict[zy4mknm.JOYSTICK_X_REG_ADDR]
# #             vw = mctlregs.motctl_regs_dict[zy4mknm.JOYSTICK_ANGSPE_REG_ADDR]
# #             zy4mknm.mknm_update_reg_pwm(vy,vx,vw)
#             zy4mknm.mknm_update_regs_pwm(parsed_vals['regNum'][0],parsed_vals['regAddr'][0],parsed_vals['datas'])
#         if config.ARM_TYPE == 'ARM_4X3L_SERVO':
#             arm4s.update_arm_4servo_angle()
#         #return 'ack'.encode('bin')
#         return parsed_vals['ack_frm_bytearr']
#     
#     if parsed_vals['fcode'] == udprpl.FCODE_READ_REGS:
#         # Todo
#         return parsed_vals['ack_frm_bytearr']
#         
#         
# 
# async def print_info():
#     while True:
#         print('...',time.ticks_ms())
#         await uasyncio.sleep_ms(2500)
#         print('---',time.ticks_ms())
#         await uasyncio.sleep_ms(2500)
#         
# async def print_time():
#     while True:
#         print('time',time.ticks_ms())
#         await uasyncio.sleep_ms(1000)
#         
# 
# def main():
#     print('Enter in main() ticks_ms:', time.ticks_ms())
# #     if config.ROBOT_NAME == zy2wd.zyrot_2WD_paras_dict['name']:
# #         zy2wd.pwm_init()
# #         zy2wd.update_pwm_duty()
#     if config.ROBOT_NAME == zy4wd.zyrot_4WD_paras_dict['name']:
#         zy4wd.pwm_init()
#         zy4wd.update_pwm_duty()
#     if config.ROBOT_NAME == zy4mknm.zyrot_4MKNM_paras_dict['name']:
#         zy4mknm.pwm_init()
#         zy4mknm.update_pwm_duty()
#     if config.ARM_TYPE == 'ARM_4X3L_SERVO':
#         arm4s.init_arm_4servo()
#         
#     ap_init()
#     time.sleep_ms(500)
#     s = UDPServer()
# #     l = uasyncio.get_event_loop()
# #     l.run_until_complete(s.serve(cb,'0.0.0.0',port))
#     uasyncio.create_task(print_info())
#     uasyncio.create_task(print_time())
#     uasyncio.run(s.serve(cb,'0.0.0.0',config.PORT))
# 
#     
# def ap_init():
#     print('Begin ap_init() ticks_ms:' , time.ticks_ms())
#     import network
#     import binascii
#     import machine 
#     global ap
#     
#     uid = machine.unique_id()
#     idstr = binascii.hexlify(uid).decode()
#     idstr_ssid = idstr[-4:]
#     
#     ap = network.WLAN(network.AP_IF) # create access-point interface
# #     ap.config(authmode=3)    # enable ap password
#     print('wifi ssid',config.SSID_F+idstr_ssid)
#     print('wifi password:',config.PWD)
#     ap.config(essid=config.SSID_F+idstr_ssid, password=config.PWD) # set the SSID of the access point
#     ap.config(max_clients=2) # set how many clients can connect to the network
#     ap.active(True)         # activate the interface
#     
    
# import pwm_motor_test
# if __name__ == '__main__':
#     pwm_motor_test.pwm_motor_test(3000)


'''
红外遥控
8*8LED点阵显示字母‘R’，
并根据红外控制信号显示前、后、左、右箭头
'''
import ir_nec16_main
if __name__ == '__main__':
    ir_nec16_main.main()


