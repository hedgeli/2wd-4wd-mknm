
import time
from zyrot_2wd_dualPID_obj import ZYRot_2WD_DPID_Test
    
if __name__ == '__main__':
    start_ms = time.ticks_ms()
    print('Boot OK. ms:', start_ms)
    ZYRot_2WD_DPID_Test()
    
