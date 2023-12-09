import time

def time_test():
    sus = time.ticks_us()
    val = 0.00
    for i in range(100):
        val = (i*1.001/2.002)*2.00 + val
    endus = time.ticks_us()
    print('val:',val,'us:', endus-sus)
  
  
if __name__ == '__main__':
    time_test()
  
  