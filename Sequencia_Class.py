from Motor_Class import *
from datalog import *

class Sequencia:
    def __init__(self):

        self.SW_emergency = 5
        GPIO.setup(self.SW_emergency, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.motor_X = Motor(ENA = 6, PUL_out = 3, DIR_out = 16, PUL_in = 27, DIR_in = 18 , SW_ini = 12, SW_fin = 20, radius = 24/2, distance=1755)
        self.motor_Y = Motor(ENA = 24, PUL_out = 0, DIR_out = 25, PUL_in = 4, DIR_in = 17 , SW_ini = 23, SW_fin = 22, radius = 15/2, distance=1680)

        self.setup()




        #print("Foward ")
        self.motor_X.foward()
        self.motor_Y.foward()
        sleep(0.5)

        self.stop()
        sleep(0.5)

        self.motor_X.calibration()
        self.motor_X.foward()
        sleep(0.5)
        self.stop()


        self.motor_Y.calibration()
        self.motor_Y.foward()
        sleep(0.5)
        self.stop()


        self.motor_Y.foward()


        #self.origin()
        #sleep(3)
        #self.motor_X.foward()
        #self.motor_Y.foward()
        #sleep(0.5)
        #self.go_to_2D(50,self.motor_Y.max_disp)

       #self.move_1D(self.motor_X, 50)
        #self.move_1D(self.motor_Y, self.motor_Y.max_disp / 10)

        #self.trajectory()

        #self.motor_X.foward()


    def create_list(self, initial, final, steps):
        return [initial + i * ((final - initial) / (steps - 1)) for i in range(steps)]


    def stop(self):
        self.motor_X.stop()
        self.motor_Y.stop()

    def sw_emergency_fx(self):
        #if not GPIO.input(self.SW_emergency):
        if True:
            print("Button pressed! - STOP")
            #self.motor_X.stop()
            #self.motor_Y.stop()
        else:
            print("Button released! - START")

    def go_to(self, motor, final_disp):
        origin_pulse = motor.total_pulses
        if origin_pulse> motor.max_pulses:
           origin_pulse = motor.max_pulses
        elif origin_pulse< 0:
            origin_pulse = 0

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
        #print("LIST Xi -> ", X_i)
        #print("LIST Yi -> ", Y_i)

        for x,y in zip(X_i, Y_i):
            X_bool, Y_bool = False, False
            #print("X - Pulses=", self.motor_X.total_pulses, " Position=", round(self.motor_X.position, 2)," Fin=", round(x, 2))
            #print("Y - Pulses=", self.motor_Y.total_pulses, " Position=", round(self.motor_Y.position, 2)," Fin=", round(y, 2))
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
        #print("LIST -> ", X_i)

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

    def trajectory_X(self,X_bool):
        if X_bool!=self.motor_X.direction:
            self.motor_X.stop()
            if self.motor_Y.direction:
                self.motor_Y.foward()
            else:
                self.motor_Y.backward()
            sleep(2)
            self.motor_Y.stop()
            if self.motor_X.direction:
                self.motor_X.foward()
            else:
                self.motor_X.backward()
        return self.motor_X.direction

    def trajectory_Y(self,Y_bool):
        if Y_bool!=self.motor_Y.direction:
            self.stop()
            self.motor_Y.stop()
            if self.motor_X.direction:
                self.motor_X.foward()
            else:
                self.motor_X.backward()
            sleep(2)
            self.motor_X.stop()
            self.stop()
            if self.motor_Y.direction:
                self.motor_Y.foward()
            else:
                self.motor_Y.backward()
        return self.motor_Y.direction

    def update_file(self):
        datalog(self.file, round(self.motor_X.position, 2), round(self.motor_Y.position, 2))

    def setup(self):
        GPIO.add_event_detect(self.SW_emergency, GPIO.BOTH, callback=self.sw_emergency_fx)
        self.file = create_file()




sequencia = Sequencia()