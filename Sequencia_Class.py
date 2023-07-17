from Motor_Class import *

class Sequencia:
    def __init__(self, SW_emergency):


        self._SW_emergency = SW_emergency
        self.motor_X = Motor(ENA = 22, PUL_out = 18, DIR_out = 27, PUL_in = 7, DIR_in = 12 , SW_ini = 23, SW_fin = 24)
        #self.motor_Y = Motor(ENA = 14, PUL_out = 18, DIR_out = 15, PUL_in = 12, DIR_in = 7 , SW_ini = 23, SW_fin = 24)

        #GPIO.add_event_detect(self._SW_emergency, GPIO.RISING, callback=self.stop)

        print("Foward ")
        #self.motor_X.foward()
        #sleep(10)
        #self.motor_X.stop()
        self.motor_X.calibration()
        sleep(10)
        self.motor_X.stop()
        sleep(10)
        print("Done")
        #self.motor_Y.calibration()

        #self.origin()

    def create_list(self, initial, final, steps):
        return [initial + i * ((final - initial) / (steps - 1)) for i in range(steps)]


    def stop(self):
        self.motor_X.stop()
        #self.motor_Y.stop()

    def go_to(self, motor, final_disp):
        origin_pulse = motor.total_pulses
        final_pulse = (final_disp/motor._distance_per_rev)*motor._pulses_per_rev
        if final_pulse> motor.max_pulses:
           final_pulse = motor.max_pulses
        elif final_pulse< 0:
            final_pulse = 0

        if origin_pulse < final_pulse - motor._accuacy_pulses:
            motor.foward()
            return False
        elif origin_pulse> final_pulse + motor._accuacy_pulses:
            motor.backward()
            return False
        else:
            motor.stop()
            return True
    def go_to_2D(self, X_fin, Y_fin):
        origin_x = self.motor_X.position
        #origin_y = self.motor_Y.position

        X_i = self.create_list(origin_x, X_fin, 100)
        #Y_i = self.create_list(origin_y, Y_fin, 100)
        Y_i = X_i
        for x,y in zip(X_i, Y_i):
            X_bool, Y_bool = False, False
            while X_bool==False or Y_bool==False:
                X_bool = self.go_to(self.motor_X, x)
                #Y_bool = self.go_to(self.motor_Y,Y)
                Y_bool = True
    def origin(self):
        self.go_to_2D(0,0)

    def trajectory(self):
        pass

sequencia = Sequencia(SW_emergency=None)