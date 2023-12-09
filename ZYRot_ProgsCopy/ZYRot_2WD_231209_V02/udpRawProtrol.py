
import zyrot_config as config

'''
UDP Raw protrol
byte NO     0        1        2        3        4        5        6        xx        n-2      n-1      n 
byte info   start    addr     fcode    regCntH  regCntL  regAddrH regAddrL Datas     ChksumH  ChksumL  End(0xfe)
            0xfa     0x01
'''

UDP_RAW_PROTROCTL_VERSION = 200

'''
function code
0x03   read registers 
0x10   write registers

'''
FCODE_READ_REGS  = 0X03
FCODE_WRITE_REGS = 0X10

'''
Register configration
0x0100           DC motor PWM duty value, for all motors. -1023 ~ +1023
0x0101-0x0106    NO 1~6 DC motor PWM duty value, each -1023 ~ +1023

0x0200           3line servo motor angle value, for all servo. -1800 ~ +1800
0x0201-0x010C    NO 1~12 3line servo motor angle value, each -1800 ~ +1800

0x0300           5line servo motor angle value, for all servo. -1800 ~ +1800
0x0301-0x0306    NO 1~6 5line servo motor angle value, each -1800 ~ +1800
    
0x1301-0x1306    5line servo motor angle, read only
0x1310           Battary voltage 0~12000mV, read only
0x1311           5V input voltage 0~6000mv, read only
'''

'''
examples

Read saddr 01 regaddr 0x1301 for 4 regs
fa 01 03 00 04 13 01 01 16 fe

write all DC motor pwm duty to 500
byte NO     0        1        2        3        4        5        6        xx        n-2      n-1      n 
byte info   start    addr     fcode    regNumH  regNumL  regAddrH regAddrL Datas     ChksumH  ChksumL  End(0xfe)
            0xfa     0x01     0x10     0X00     0x01     0X10     0X00     0x01 0xf4 0x02     0x11     0xfe

write all DC motor pwm duty to -500
index  0    1    2    3    4    5    6    7    8    9    10   11
       0xfa 0x01 0x10 0X00 0x01 0X10 0X00 0xFE 0x0C 0xNN 0xNN 0xfe

'''

'''
>>> frmb = b'\xfa\x01\x10\x00\x01\x10\x00\xfe\x0c'
>>> frmb
b'\xfa\x01\x10\x00\x01\x10\x00\xfe\x0c'
>>> struct.unpack('>BBBhhh', frmb)
(250, 1, 16, 1, 4096, -500)
>>> values = struct.unpack('>BBBhhh', frmb)
>>> values
(250, 1, 16, 1, 4096, -500)
>> vallist = list(values)
>>> vallist
[250, 1, 16, 1, 4096, -500]
>>> packbarr = struct.pack('>BBBhhh',*vallist)
>>> packbarr
b'\xfa\x01\x10\x00\x01\x10\x00\xfe\x0c'
>>> packbarr = struct.pack('>BBBhhh',*values)
>>> packbarr
b'\xfa\x01\x10\x00\x01\x10\x00\xfe\x0c'
'''

import struct
import zyrot_utils
import zyrot_motctl_regs


SELF_ADDR = 0X01

START_BYTE = b'\xFA'
END_BYTE  = b'\xFE'


FRM_START_IDX  = 0X00
SLAVE_ADDR_IDX = 0X01
FCODE_IDX      = 0X02
REG_NUM_IDX    = 0X03
REG_ADDR_IDX   = 0X05
REG_VALUE_IDX  = 0X07


def parse_recv_data(values_fmt, recvfrm):
    import struct
#     data_fmt = '>BBBhhhHB'
    values = struct.unpack(values_fmt,recvfrm)
    return values

def prepare_frm(SelfAddr = 0x01,Fcode = FCODE_READ_REGS,
                RegNum = 0,RegAddr = 0,RegVals = [],
                ByteOrder = '>',Valfmt = 'h'):
    import struct
    func_bytes = struct.pack(ByteOrder+'BB',*[SelfAddr,Fcode])
    frm_bytearr = b''
    regNum_bytes = struct.pack(ByteOrder+'H',RegNum)
    
#     if Fcode == FCODE_READ_REGS:
#         frm_bytearr = START_BYTE + func_bytes + regNum_bytes
        
    # Fcode = FCODE_WRITE_REGS
    if RegNum > 0:
        values_bytes = struct.pack(ByteOrder+Valfmt*len(RegVals),*RegVals)
        regAddr_bytes = struct.pack(ByteOrder+'H',RegAddr)
        frm_bytearr = START_BYTE + func_bytes + regNum_bytes \
                      + regAddr_bytes + values_bytes
    elif RegNum == 0:
        frm_bytearr = START_BYTE + func_bytes + regNum_bytes
    else:
        print('Error! regNum must >= 0')
        return
    chksum = 0
    for i in range(len(frm_bytearr)):
        chksum += frm_bytearr[i]
#         print('i chksum',i,chksum)
    chksum = chksum % 65536
#     print('chksum:', chksum)
    chksum_bytes = struct.pack(ByteOrder+'H',chksum)
#     print('cksum_bytes:',chksum_bytes)
    frm_bytearr = frm_bytearr + chksum_bytes + END_BYTE
    
#     print('prepared frame bytearray:', frm_bytearr)
        
    return frm_bytearr


def send_frm(bytearr=b''):
    
    return


# 计算检验和
def cal_checksum(bytearr=b''):
    bnum = len(bytearr)
    chksum = 0
    for i in range(bnum-3):
        chksum += bytearr[i]
    return chksum%655536


def cal_crc(ByteArr = b''):
    pass   # Todo
    return 
    



def parse_recv_bytearr( bytearr=b'', val_format='>BBB',
                       byteOrder = '>', valfmt = 'h'): 
    import struct
    (start,saddr,fcode) = struct.unpack(val_format,bytearr)
    if config.LOG_LEVEL&config.PARSE_LOG > 0:
        print('start:',start,'    saddr:',saddr,'    fcode:',fcode)
    if start != int.from_bytes(START_BYTE,'big'):
        print('error start byte! 0x%x' % start)
        return []
    if saddr != SELF_ADDR:
        print('frame addr(0x%x) is not for this machine(0x%x)' % saddr,SELF_ADDR)
        return []
    if bytearr[-1] != int.from_bytes(END_BYTE,'big'):
        print('receive frame not complete.')
        return []
    
    if fcode == FCODE_READ_REGS:
        regNum  = struct.unpack('>H',bytearr,REG_NUM_IDX)
        regAddr = struct.unpack('>H',bytearr,REG_ADDR_IDX)
        
        chksum = struct.unpack('>H',bytearr,len(bytearr)-3)
        calsum = cal_checksum(bytearr)
        if chksum[0] != calsum:
            print('FCODE_WRITE_REGS  Receive frame check sum error!')
            print('rec chksum:',chksum,'calc sum:',calsum)
            return []
        
        # 读取控制板寄存器值    
        reg_vals = zyrot_motctl_regs.get_regs_val(RegNum=regNum[0],RegAddr=regAddr[0])
        parse_res = {'fcode':[],'saddr':[],'regNum':[], 'regAddr':[],'datas':[],'ack_frm_bytearr':[]}
        parse_res['saddr'] = saddr
        parse_res['fcode'] = fcode
        parse_res['datas'] = reg_vals
        parse_res['regNum'] = regNum[0]
        parse_res['regAddr'] = regAddr[0]
            
        # 应答帧，返回寄存器数据
        parse_res['ack_frm_bytearr'] = prepare_frm(SelfAddr=saddr,Fcode=FCODE_READ_REGS,
                                      RegNum=regNum[0],RegAddr=regAddr[0],RegVals=reg_vals)
        if config.LOG_LEVEL&config.PARSE_LOG > 0:
            print('Parse Fcode Read regs:')
            print(parse_res)
        return parse_res
    
    
    if fcode == FCODE_WRITE_REGS:
        regNum  = struct.unpack('>H',bytearr,REG_NUM_IDX)
        regaddr = struct.unpack('>H',bytearr,REG_ADDR_IDX)
        #print('regNum:',regNum,'regaddr:',regaddr)
        chksum = struct.unpack('>H',bytearr,len(bytearr)-3)
        calsum = cal_checksum(bytearr)
        if chksum[0] != calsum:
            print('FCODE_WRITE_REGS  Receive frame check sum error!')
            print('rec chksum:',chksum,'calc sum:',calsum)
            return []
        
        val_fmt = byteOrder + valfmt *regNum[0]
        reg_recv_vals = struct.unpack(val_fmt,bytearr,REG_VALUE_IDX)
        if config.LOG_LEVEL&config.PARSE_LOG > 0:
            print('reg_recv_vals:', reg_recv_vals)
        parse_res = {'fcode':[],'saddr':[],'regNum':[], 'regAddr':[],'datas':[],'ack_frm_bytearr':[]}
        parse_res['saddr'] = saddr
        parse_res['fcode'] = fcode
        parse_res['datas'] = reg_recv_vals
        parse_res['regNum'] = regNum
        parse_res['regAddr'] = regaddr
#         prepare_frm(Selfaddr = 0x01,Fcode = FCODE_READ_REGS,
#                 RegNum = 0,Regaddr = 0,Regvals = [],
#                 ByteOrder = '>',Valfmt = 'h'):
        # 应答帧，返回从机地址和操作码
        parse_res['ack_frm_bytearr'] = prepare_frm(SelfAddr = 0x01,Fcode = FCODE_WRITE_REGS,
                RegNum = regNum[0],RegAddr = regaddr[0],RegVals = [],
                ByteOrder = '>',Valfmt = 'h')
        if config.LOG_LEVEL&config.PARSE_LOG > 0:
            print('Parse Fcode Write regs:')
            print(parse_res)
        return parse_res
        
    


def parse_test():
    data_s = [0xfa,0x01,0x10,0X00,0x01,0X10,0X00,0xFE,0x0C,0x02,0x26,0xfe]
    
    test_frm = struct.pack('B'*len(data_s),*data_s)
    print('test_frm',test_frm)
    parse_recv_bytearr(bytearr=test_frm)
    
#     def prepare_frm(SelfAddr = 0x01,Fcode = FCODE_READ_REGS,
#                 RegNum = 0,RegAddr = 0,RegVals = [],
#                 ByteOrder = '>',Valfmt = 'h'):
    
    send_frame_bytearray = prepare_frm(SelfAddr = 0x01,Fcode = FCODE_READ_REGS,
                RegNum = 4,RegAddr = 0x1301,RegVals = [],
                ByteOrder = '>',Valfmt = 'h')
#     print('send_frame_bytearray ',send_frame_bytearray)
    print('send_frame_bytearray:')
    zyrot_utils.printhex(send_frame_bytearray)
    
    parsed_vals = parse_recv_bytearr(bytearr=send_frame_bytearray)
    print('parsed_vals ',parsed_vals)
    
    send_frame_bytearray = prepare_frm(SelfAddr = 0x01,Fcode = FCODE_WRITE_REGS,
                RegNum = 4,RegAddr = 0x0201,RegVals = [-500,1000,-10000,20000],
                ByteOrder = '>',Valfmt = 'h')
    print('send_frame_bytearray:')
    zyrot_utils.printhex(send_frame_bytearray)
    
    send_frame_bytearray = prepare_frm(SelfAddr = 0x01,Fcode = FCODE_WRITE_REGS,
                RegNum = 12,RegAddr = 0x0201,RegVals = [100,101,103,104,105,106,107,108,109,110,111,101,],
                ByteOrder = '>',Valfmt = 'h')
    print('send_frame_bytearray:')
    zyrot_utils.printhex(send_frame_bytearray)
    
    send_frame_bytearray = prepare_frm(SelfAddr = 0x01,Fcode = FCODE_WRITE_REGS,
                RegNum = 12,RegAddr = 0x0201,RegVals = [10,11,13,14,15,16,17,18,19,10,11,11,],
                ByteOrder = '>',Valfmt = 'h')
    print('send_frame_bytearray:')
    zyrot_utils.printhex(send_frame_bytearray)
    
    send_frame_bytearray = prepare_frm(SelfAddr = 0x01,Fcode = FCODE_WRITE_REGS,
                RegNum = 12,RegAddr = 0x0101,RegVals = [400,401,103,104,105,106,107,108,109,110,111,101,],
                ByteOrder = '>',Valfmt = 'h')
    print('send_frame_bytearray:')
    zyrot_utils.printhex(send_frame_bytearray)

    send_frame_bytearray = prepare_frm(SelfAddr = 0x01,Fcode = FCODE_WRITE_REGS,
                RegNum = 12,RegAddr = 0x0101,RegVals = [0,0,0,0,0,0,0,0,0,0,0,0,],
                ByteOrder = '>',Valfmt = 'h')
    print('send_frame_bytearray:')
    zyrot_utils.printhex(send_frame_bytearray)
    
    send_frame_bytearray = prepare_frm(SelfAddr = 0x01,Fcode = FCODE_WRITE_REGS,
                RegNum = 12,RegAddr = 0x0101,RegVals = [-400,-401,-103,-104,-105,-106,-107,-108,-109,-110,-111,-101,],
                ByteOrder = '>',Valfmt = 'h')
    print('send_frame_bytearray:')
    zyrot_utils.printhex(send_frame_bytearray)
    
    parsed_vals = parse_recv_bytearr(bytearr=send_frame_bytearray)
    print('parsed_vals ',parsed_vals)


if __name__ == '__main__':
    parse_test()
    
    
