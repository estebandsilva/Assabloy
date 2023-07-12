from time import sleep
import RPi.GPIO as GPIO
import math
# Raspberry Pi Zero: PWM --> GPIO 12, 13, 18, 19
class Motor:
    _microsteps = 1 # microsteps to divide --> Change with Microstep Driver
    _pulses_per_rev = _microsteps*200
    _max_rev_min = 200 # maximum revolution per minute
    _min_rev_min = 50  # maximum revolution per minute
    _distance_per_rev = 2*math.pi*10 # mm per revolution
    _max_freq = round(_pulses_per_rev*_max_rev_min/60) # frequency maxima in HZ
    _min_freq = round(_pulses_per_rev * _min_rev_min/60)  # frequency minimum IN Hz


    # constructor
    def __init__(self, ENA, PUL_out, DIR_out, PUL_in, DIR_in, SW_ini, SW_fin):
        self.total_pulses = 0
        self.position = 0
        self.max_pulses = 5000
        self.max_disp = (2000/self._distance_per_rev)*self._pulses_per_rev  # maximum steps of all displacment

        self._ENA = ENA # (High to Enable / LOW to Disable).
        self._PUL_out = PUL_out
        self._DIR_out = DIR_out
        self._PUL_in = PUL_in
        self._DIR_in = DIR_in
        self._SW_ini = SW_ini
        self._SW_fin = SW_fin


        self.direction = True #Clockwise=1, Anticlock = 0

        self._SW_ini_bool = False
        self._SW_fin_bool = False
        self._calibration_bool = True


        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._ENA, GPIO.OUT, initial = GPIO.HIGH)
        GPIO.setup(self._PUL_out, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(self._DIR_out, GPIO.OUT, initial = GPIO.HIGH)
        GPIO.setup(self._PUL_in, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self._DIR_in, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self._SW_ini, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self._SW_fin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.pwm = GPIO.PWM(self._PUL_out, self._max_freq)  # create PWM instance with frequency
        self.setup()




    def  count_pulses(self, channel):
        if self.direction==True:
            self.total_pulses +=1
        else:
            self.total_pulses -=1
        self.position = (self.total_pulses/self._pulses_per_rev)*self._distance_per_rev
        #print("Pulses=",self.total_pulses, " Position=", self.position)

    def change_direction(self, channel):
        if self.direction==False:
            self.foward()
            while GPIO.input(self._SW_ini):
                GPIO.wait_for_edge(self._SW_ini, GPIO.FALLING)
            self.total_pulses = 0  # Possible quitarlo --> Recalibra el conteo de pasos
        else:
            self.backward()
            while GPIO.input(self._SW_fin):
                GPIO.wait_for_edge(self._SW_ini, GPIO.FALLING)
            self.max_steps = self.total_pulses  # Possible quitarlo --> Recalibra el conteo de pasos



    def direction_change(self,channel):
        if GPIO.input(self._DIR_in):
            self.direction = True
        else:
            self.direction = False

    def direction_change_true(self, channel):
        self.foward()
        if self._calibration_bool == True and self._SW_ini_bool == False:
            self.total_pulses = 0
            self._SW_ini_bool = True


    def direction_change_false(self, channel):
        self.backward()
        if self._calibration_bool == True and self._SW_fin_bool == False:
            self.max_pulses = self.total_pulses
            self._SW_fin_bool = True



    def foward(self):
        #self.direction = True
        #GPIO.output(self._ENA, GPIO.HIGH)
        GPIO.output(self._DIR_out, GPIO.HIGH)
        #self.pwm.start(50)  # start PWM of required Duty Cycle

    def backward(self):
        #self.direction = False
        #GPIO.output(self._ENA, GPIO.HIGH)
        GPIO.output(self._DIR_out, GPIO.LOW)
        #self.pwm.start(50)  # start PWM of required Duty Cycle

    def change_velocity(self, frequency):
        if frequency>self._max_freq:
            frequency=self._max_freq
        elif frequency<self._min_freq:
            frequency = self._min_freq
        self.pwm.ChangeFrequency(frequency)

    def start(self):
        GPIO.output(self._ENA, GPIO.HIGH)
        self.pwm.start(50)  # start PWM of required Duty Cycle

    def stop(self):
        self.pwm.stop()
        GPIO.output(self._ENA, GPIO.LOW)

    def setup(self):
        GPIO.add_event_detect(self._PUL_in, GPIO.RISING, callback=self.count_pulses, bouncetime=round(1000*(1/self._max_freq)/2))
        GPIO.add_event_detect(self._DIR_in, GPIO.BOTH, callback=self.direction_change)
        GPIO.add_event_detect(self._SW_ini, GPIO.RISING, callback=self.direction_change_true)
        GPIO.add_event_detect(self._SW_fin, GPIO.RISING, callback=self.direction_change_false)


    def calibration(self):
        self.start()
        self._SW_ini_bool = False
        self._SW_fin_bool = False
        self._calibration_bool = True
        print("Calibration: Started.")
        print("Calibration Initial: Started 1.")
        self.backward()
        while self._calibration_bool:
            if self._SW_ini_bool == False:
                pass
            else:
                break
        print("Calibration Initial: Completed 1.")
        print("Calibration Final: Started.")
        self.foward()
        while self._calibration_bool:
                if self._SW_fin_bool == False:
                    pass
                else:
                    break
        print("Calibration Final: Completed. Total Max Pulse = ", self.max_pulses)

        print("Calibration Initial: Started 2.")
        self.backward()
        while self._calibration_bool:
            if self._SW_ini_bool == False:
                pass
            else:
                break
        print("Calibration Initial: Completed 2.")
        self._calibration_bool = False
        print("Calibration: Completed.")
        self.stop()



    def update(self):
        pass

