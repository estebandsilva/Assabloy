from Motor_Class import *

class Sequencia:
    def __init__(self, SW_emergency):

        self._SW_emergency = SW_emergency
        self.motor_X = Motor(ENA =  6, PUL_out = 0, DIR_out = 25, PUL_in = 23, DIR_in = 17 , SW_ini = 12, SW_fin = 20, radius = 24)
        #self.motor_Y = Motor(ENA = 24, PUL_out = 3, DIR_out = 16, PUL_in = 22, DIR_in = 18 , SW_ini = [4, 27], SW_fin = [21, 13], radius = 15)

        GPIO.setup(self._SW_emergency, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self._SW_emergency, GPIO.RISING, callback=self.stop)

        print("Foward ")

        self.motor_X.calibration()
        #self.motor_Y.calibration()
        self.motor_X.stop()
        self.stop()
        sleep(0.5)

        self.motor_X.foward()
        sleep(10)
        self.origin()

    def create_list(self, initial, final, steps):
        return [initial + i * ((final - initial) / (steps - 1)) for i in range(steps)]


    def stop(self):
        self.motor_X.stop()
        #self.motor_Y.stop()

    def go_to(self, motor, final_disp):
        origin_pulse = motor.total_pulses
        final_pulse = round((final_disp/motor._distance_per_rev)*motor._pulses_per_rev)
        if final_pulse> motor.max_pulses:
           final_pulse = motor.max_pulses
        elif final_pulse< 0:
            final_pulse = 0

        #print("Origin = ",origin_pulse, " --> Final=", final_pulse, " Accuracy=", motor._accuacy_pulses )
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

        X_i = self.create_list(origin_x, X_fin, 10)
        #Y_i = self.create_list(origin_y, Y_fin, 100)
        Y_i = X_i
        for x,y in zip(X_i, Y_i):
            X_bool, Y_bool = False, False
            while X_bool==False or Y_bool==False:
                X_bool = self.go_to(self.motor_X, x)
                #Y_bool = self.go_to(self.motor_Y,y)
                Y_bool = True
    def origin(self):
        self.go_to_2D(0,0)

    def trajectory(self):
        pass

sequencia = Sequencia(SW_emergency=19)