# More information about PID Controller: http://en.wikipedia.org/wiki/PID_controller

import time

class PID:
    def __init__(self, P=1.0, I=0.0, D=0.0, st_ms=20):

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = st_ms/1000
        self.current_time = time.ticks_ms()     #This is the main difference with the original, use of microbit's time lib
        self.last_time = self.current_time

        self.clear()

    def clear(self):
        # Clears PID computations and coefficients
        self.SetPoint = 0.0
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        self.output = 0.0

    def update(self, feedback_value):
        # u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}
        # Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)

        self.current_time = time.ticks_ms()
        delta_time = time.ticks_diff(self.current_time, self.last_time) / 1000
        

        if delta_time >= self.sample_time:
            error = self.SetPoint - feedback_value
            delta_error = error - self.last_error
            
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = error

            ITerm = self.Ki * self.ITerm
            DTerm = self.Kd * self.DTerm
            #self.output = self.PTerm + ITerm + DTerm
            self.output = self.output + self.PTerm + ITerm + DTerm
            print('P ',round(self.PTerm,2),'I ',round(ITerm,2),
                  'D ',round(DTerm,2), 'O ', round(self.output,2),
                  'T ',round(self.SetPoint,2), 'V ',round(feedback_value,2))
            

    def setKp(self, proportional_gain):
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        self.Kd = derivative_gain

    def setSampleTime(self, sample_time):
        # PID that should be updated at a regular interval.
        # Based on a pre-determined sample time, the PID decides
        # if it should compute or return immediately.
        self.sample_time = sample_time
        

def simple_pid_test():
    print('Start simple_pid_test()...')
        
        
if __name__ == '__main__':
    simple_pid_test()
    output = 0.0
    pid1 = PID()
    pid1.SetPoint = 1.0
    pid1.setKp(0.9)
    pid1.setKi(1)
    pid1.setKd(0.0000)
    for i in range(50):
        time.sleep_ms(20)
        real_val = pid1.output
        pid1.update(real_val)
        #print('out:', real_val)
        
        

        