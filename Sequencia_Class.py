from Motor_Class import *

class Sequencia:
    def __init__(self, SW_emergency):

        self._SW_emergency = SW_emergency
        self.motor_X = Motor(ENA = 6, PUL_out = 3, DIR_out = 16, PUL_in = 27, DIR_in = 18 , SW_ini = 12, SW_fin = 20, radius = 24/2, distance=1755)
        self.motor_Y = Motor(ENA = 24, PUL_out = 0, DIR_out = 25, PUL_in = 4, DIR_in = 17 , SW_ini = 23, SW_fin = 22, radius = 15/2, distance=1680)

        #GPIO.setup(self._SW_emergency, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO.add_event_detect(self._SW_emergency, GPIO.RISING, callback=self.stop)

        print("Foward ")
        self.motor_X.foward()
        self.motor_Y.foward()
        sleep(0.5)

        self.stop()
        sleep(0.5)
        self.motor_X.calibration()
        self.motor_Y.calibration()
        self.stop()
        #self.origin()

        self.motor_X.foward()
        self.motor_Y.foward()
        sleep(0.5)
        self.origin()
        self.go_to_2D(0,self.motor_Y.max_disp)

        #self.move_1D(self.motor_Y, self.motor_Y.max_disp / 10)

        #self.trajectory()


    def create_list(self, initial, final, steps):
        return [initial + i * ((final - initial) / (steps - 1)) for i in range(steps)]


    def stop(self):
        self.motor_X.stop()
        self.motor_Y.stop()

    def go_to(self, motor, final_disp):
        origin_pulse = motor.total_pulses
        #print("Final_disp =", final_disp)
        final_pulse = round(final_disp*motor.puls_per_dist)
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
        origin_y = self.motor_Y.position

        X_i = self.create_list(origin_x, X_fin, 10)
        Y_i = self.create_list(origin_y, Y_fin, 10)
        print("LIST Xi -> ", X_i)
        print("LIST Yi -> ", X_i)

        for x,y in zip(X_i, Y_i):
            X_bool, Y_bool = False, False
            while X_bool==False or Y_bool==False:
                try:
                    X_bool = self.go_to(self.motor_X, x)
                    Y_bool = self.go_to(self.motor_Y, y)
                except KeyboardInterrupt:
                    self.stop()
        self.stop()

    def move_1D(self, motor, move):
        origin = motor.position
        X_fin = abs(origin + move)

        X_i = self.create_list(origin, X_fin, 2)
        print("LIST -> ", X_i)

        for x in X_i:
            X_bool = False
            while X_bool == False:
                try:
                    X_bool = self.go_to(motor, x)
                except KeyboardInterrupt:
                    self.stop()
        self.stop()

    def origin(self):
        self.go_to_2D(0,0)

    def trajectory(self):
        X_bool = True
        self.motor_X.foward()
        if X_bool!=self.motor_X.direction:
            self.motor_Y.foward()
            X_bool = self.motor_X.direction
            self.move_1D(self.motor_Y,self.motor_Y.max_disp/10)

sequencia = Sequencia(SW_emergency=19)