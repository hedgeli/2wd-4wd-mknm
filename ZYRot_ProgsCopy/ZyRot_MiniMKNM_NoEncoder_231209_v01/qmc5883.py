import math
import machine
from ustruct import pack
from array import array
import time

class QMC5883L():
    def __init__ (self, scl=5, sda=4 ):
        self.i2c =i2c= machine.I2C(scl=machine.Pin(scl), sda=machine.Pin(sda), freq=100000)
        #self.address=const(13)
        # Initialize sensor.
        i2c.start()
        #Write Register 0BH by 0x01 (Define Set/Reset period)
        i2c.writeto_mem(13, 0xB, b'\x01')
        #Write Register 09H by 0x1D 
        # (Define OSR = 512, Full Scale Range = 8 Gauss, ODR = 200Hz, set continuous measurement mode)
        i2c.writeto_mem(13, 0x9, b'\x11101')
        i2c.stop()

        # Reserve some memory for the raw xyz measurements.
        self.data = array('B', [0] * 9)
           
    def reset(self):
        """performs a reset of the device by writing to the memory address 0xA, the value of b '\ x10000000' """
        #Write Register 0AH by 0x80
        self.i2c.writeto_mem(13, 0xA, b'\x10000000')

    def stanbdy (self):
        """device goes into a sleep state by writing to memory address 0x9, b '\ x00' """
        self.i2c.writeto_mem(13, 0x9, b'\x00')

    def read(self):
        """performs a reading of the data in the position of momoria 0x00, by means of a buffer"""
        data = self.data
        #Read data register 00H ~ 05H.
        
        
        self.i2c.readfrom_mem_into(13, 0x00, data)
        time.sleep(0.005)
        #self.i2c.readfrom_mem_into(13, 0x00, temperature)
        #time.sleep(0.005)

        x = (data[1] << 8) | data[0]
        y = (data[3] << 8) | data[2]
        z = (data[5] << 8) | data[4]
        status =data[6]
        temperature = (data[8] << 8) | data[7]
        scale =3000
        temperature_offest=50.0

#         return (x / scale, y / scale, z / scale, status,
#                 (temperature / 100 + temperature_offest))
        return (x, y, z, status,
                 (temperature / 100 + temperature_offest))
    
    
    
if __name__ == '__main__':
    import time
    qmc=QMC5883L()
    for i in range(600):
        x, y, z, status, temp =qmc.read()
        #print (round(x,5), round(y,5), round(z,5))
        #print('%.3f, %.3f, %.3f' % (x,y,z))
        if x > 32767:
            x = x - 65536
        if y > 32767:
            y = y - 65536
        if z > 32767:
            z = z - 65536
        print(x,y,z)
        time.sleep_ms(100)
    
    
    
    