from Motor_Class import *

class Sequencia:
    def __init__(self, SW_emergency):


        self._SW_emergency = SW_emergency
        self.motor_X = Motor(ENA = 14, PUL_out = 18, DIR_out = 15, PUL_in = 12, DIR_in = 7 , SW_ini = 23, SW_fin = 24)
        #self.motor_Y = Motor(ENA = 14, PUL_out = 18, DIR_out = 15, PUL_in = 12, DIR_in = 7 , SW_ini = 23, SW_fin = 24)

        #GPIO.add_event_detect(self._SW_emergency, GPIO.RISING, callback=self.stop)

        self.motor_X.calibration()
        #self.motor_Y.calibration()


    def stop(self):
        self.motor_X.stop()
        #self.motor_Y.stop()

    def go_to(self, motor, final_disp):
        origin_pulse = motor.total_pulses
        final_pulse = (motor.final/motor._pulses_per_rev)*motor._distance_per_rev
        if final_pulse> motor.max_pulses:
           final_pulse = motor.max_pulses
        elif final_pulse< 0:
            final_pulse = 0

        if origin_pulse< final_pulse - motor._accuacy_pulses:
            motor.foward()
        elif origin_pulse> final_pulse + motor._accuacy_pulses:
            motor.backward()
        else:
            motor.stop()
    def go_to_2D(self, X, Y):
        origin_x = self.motor_X.position
        #origin_y = self.motor_Y.position

        X_i = [1,2]
        Y_i = [1,2]
        for x,y in zip(X_i, Y_i):
            self.go_to(self.motor_X, x)
            #self.go_to(self.motor_Y, y)
    def origin(self):
        self.go_to(0,0)

    def trajectory(self):
        pass

sequencia = Sequencia(SW_emergency=None)
