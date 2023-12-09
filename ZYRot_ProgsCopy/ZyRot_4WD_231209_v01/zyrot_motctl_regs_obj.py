'''
Register configration
0x0100           DC motor PWM duty value, for all motors. -1000 ~ +1000
0x0101-0x0106    NO 1~6 DC motor PWM duty value, each -1000 ~ +1000

0x0200           3line servo motor angle value, for all servo. -1800 ~ +1800
0x0201-0x020C    NO 1~12 3line servo motor angle value, each -1800 ~ +1800

0x0300           5line servo motor angle value, for all servo. -1800 ~ +1800
0x0301-0x0306    NO 1~6 5line servo motor angle value, each -1800 ~ +1800
    
0x0501-0x0506    5line servo motor angle ADC RAW value, read only
0x0510           Battary voltage 0~12000mV, read only
0x0511           5V input voltage 0~6000mv, read only

0x0601-0x0602    Joystick X Y regaddr
0x0603-0x0604    Joystick power angle regaddr

0xFC01-0XFC04    APP function code and 3 short int paras

'''

class ZYRot_motctl_regs_obj():

    MOTCTL_HW_VERSION = 30

    DC_MOT_REG_ADDR_BASE = 0X0100
    SERVO_3LINE_REG_ADDR_BASE = 0X0200
    ANGLE_5LINE_SERVO_ADDR_BASE = 0X0300

    JOYSTICK_REG_ADDR_BASE = 0X0601

    JOYSTICK_X_REG_ADDR = 0x0601
    JOYSTICK_Y_REG_ADDR = 0X0602
    JOYSTICK_POWER_REG_ADDR = 0X0603
    JOYSTICK_ANGLE_REG_ADDR = 0X0604
    JOYSTICK_ANGSPE_REG_ADDR = 0X0605


    FCODE_REG_ADDR_BASE = 0XFC01;
    FCODE_REG_ADDR_PARA1 = 0XFC02;
    FCODE_REG_ADDR_PARA2 = 0XFC03;
    FCODE_REG_ADDR_PARA3 = 0XFC04;


    FCODE_FORWARD = 0XFC11;                    
    FCODE_BACK = 0XFC12;                       
    FCODE_LEFT = 0XFC13;                       
    FCODE_RIGHT = 0XFC14;                      
    FCODE_TURN_LEFT = 0XFC15;                  
    FCODE_TURN_RIGHT = 0XFC16;
    
    FCODE_SET_V_W_T = 0XFC20
                                               
    FCODE_F1 = 0XFC01;                         
    FCODE_F2 = 0XFC02;                         
    FCODE_F3 = 0XFC03;                         
    FCODE_F4 = 0XFC04;                         
    FCODE_F5 = 0XFC05;                         
    FCODE_F6 = 0XFC06;                         
                                               
    FCODE_F7 = 0XFC07;                         
    FCODE_F8 = 0XFC08;                         
    FCODE_F9 = 0XFC09;                         
    FCODE_F10 = 0XFC0A;                        
    FCODE_F11 = 0XFC0B;                        
    FCODE_F12 = 0XFC0C;

    def __init__(self):
        self.motctl_regs_dict = {
            0x0000  :  0,
            
            0x0100  :  0  ,
            0x0101  :  0  ,    # NO 1~6 DC motor PWM duty value, each -1000 ~ +1000
            0x0102  :  0  ,
            0x0103  :  0  ,
            0x0104  :  0  ,
            0x0105  :  0  ,
            0x0106  :  0  ,
            
            0x0200  :  0  ,
            0x0201  :  0  ,    # NO 1~12 3line servo motor angle value, each -1800 ~ +1800, -180~+180 degree
            0x0202  :  0  ,
            0x0203  :  0  ,
            0x0204  :  0  ,
            0x0205  :  0  ,
            0x0206  :  0  ,
            0x0207  :  0  ,
            0x0208  :  0  ,
            0x0209  :  0  ,
            0x020a  :  0  ,
            0x020b  :  0  ,
            0x020c  :  0  ,
            
            0x0300  :  0  ,
            0x0301  :  0  ,    # NO 1~6 5line servo motor angle value, each -1800 ~ +1800
            0x0302  :  0  ,
            0x0303  :  0  ,
            0x0304  :  0  ,
            0x0305  :  0  ,
            0x0306  :  0  ,
            
            0x0601  :  0  ,    # joystick x value
            0x0602  :  0  ,    # joystick y value
            0x0603  :  0  ,    # joystick power value 
            0x0604  :  0  ,    # joystick angle value
            0x0605  :  0  ,    # joystick angle speed value 角速度？
            

            0x1301  :  0  ,    # NO 1~6  5line servo motor angle ADC RAW value, read only
            0x1302  :  0  ,
            0x1303  :  0  ,
            0x1304  :  0  ,
            0x1305  :  0  ,
            0x1306  :  0  ,    
                   
            0x1310  :  0  ,    # Battary voltage 0~28000mV, read only
            0x1311  :  0  ,
            
            
            0xfc01  :  0  ,    # APP function code and 3 short int paras
            0xfc02  :  0  ,    # para1
            0xfc03  :  0  ,    # para2
            0xfc04  :  0  ,    # para3
                   }


    def set_regs_val(self, regNum=0,regAddr=0,vals=[0]):
        for i in range(regNum):
            self.motctl_regs_dict[regAddr+i] = vals[i]
            
            
    def get_regs_val(self, RegNum=0,RegAddr=0):
        if RegNum == 0:
            return []
        regs_val = []
        for i in range(RegNum):
             regs_val.append(self.motctl_regs_dict[RegAddr+i])
        return regs_val
    


def motctl_regs_test():
    print('Start motctl_regs_test()...')
#     print(motctl_regs_dict.keys())
#     print(motctl_regs_dict.values())
    ctlregs = ZYRot_motctl_regs_obj()
    print(ctlregs.motctl_regs_dict)
    vals = [1,2,3,4,5,6,7,8,9,10,11,12]
    ctlregs.set_regs_val(12,zyrot_motctl_regs_obj.SERVO_3LINE_REG_ADDR_BASE,vals)
    print(ctlregs.motctl_regs_dict)
    read_val = ctlregs.get_regs_val(12,zyrot_motctl_regs_obj.SERVO_3LINE_REG_ADDR_BASE)
    print('get_regs_val:', read_val)
    return


if __name__ == '__main__':
    motctl_regs_test()






