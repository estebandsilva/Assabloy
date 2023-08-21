from __future__ import division
from time import sleep
import RPi.GPIO as GPIO
import math

import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685


# Raspberry Pi Zero: PWM --> GPIO 12, 13, 18, 19


class Motor:
    _microsteps = 8 # microsteps to divide --> Change with Microstep Driver
    _pulses_per_rev = _microsteps*200  # 200 pulses per revolution
    _max_rev_min = 200-85 # maximum revolution per minute
    _min_rev_min = 50  # maximum revolution per minute
    #_distance_per_rev = 2*math.pi*10 # mm per revolution
    #_max_freq = round(_pulses_per_rev*_max_rev_min/60) # frequency maxima in HZ
    #_min_freq = round(_pulses_per_rev * _min_rev_min/60)  # frequency minimum IN Hz
    _duty_cycle = 50


    # constructor
    def __init__(self, ENA, PUL_out, DIR_out, PUL_in, DIR_in, SW_ini, SW_fin, radius=24, distance=1755):

        self.radius = radius # radius of the polea in mm
        self.distance = distance
        self._distance_per_rev = 2 * math.pi * self.radius  # mm per revolution
        self._max_freq = round(self._pulses_per_rev * self._max_rev_min / 60)  # frequency maxima in HZ
        self._min_freq = round(self._pulses_per_rev * self._min_rev_min / 60)  # frequency minimum IN Hz
        print("Frequency=", self._max_freq)

        self.total_pulses = 0
        self.position = 0
        self.max_pulses = 1300
        self.max_disp = (1755/self._distance_per_rev)*self._pulses_per_rev  # maximum steps of all displacment

        self._accuacy = 1/2  # accuracy in mm
        self._accuacy_pulses = math.ceil((self._accuacy /self._distance_per_rev)*self._pulses_per_rev)
        self._accuacy_pulses= 1

        self._ENA = ENA # (High to BLOCK / LOW to mOVE).
        #self._PUL_out = PUL_out
        self._DIR_out = DIR_out
        self._PUL_in = PUL_in
        self._DIR_in = DIR_in
        self._SW_ini = SW_ini
        self._SW_fin = SW_fin


        self.direction = True #Clockwise=1, Anticlock = 0
        self.movement = False

        self._SW_ini_bool = False
        self._SW_fin_bool = False
        self._calibration_bool = False

        self.PUL_pwm = PUL_out


        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._ENA, GPIO.OUT, initial = GPIO.HIGH)
        GPIO.setup(self._DIR_out, GPIO.OUT, initial = GPIO.HIGH)
        GPIO.setup(self._PUL_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._DIR_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._SW_ini, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._SW_fin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(self._max_freq)
        self.setup()


    def  count_pulses(self, channel):
        if self.direction==True:
            self.total_pulses +=1
        else:
            self.total_pulses -=1
        #self.position = (self.total_pulses/self._pulses_per_rev)*self._distance_per_rev*(self.distance/self.max_pulses)
        self.position = (self.total_pulses)* (self.distance / self.max_pulses)
        print("Pulses=",self.total_pulses, " Position=", round(self.position,2))

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
        if GPIO.input(self._SW_ini)==False:
            if self.movement:
                print("SWITCH INI-", self._SW_ini)
                self.foward()
            if self._calibration_bool == True and self._SW_ini_bool == False:
                self.total_pulses = 0
                self.position = 0
                self._SW_ini_bool = True


    def direction_change_false(self, channel):
        if GPIO.input(self._SW_fin)==False:
            if self.movement:
                print("SWITCH FIN-", self._SW_fin)
                self.backward()
            if self._calibration_bool == True and self._SW_fin_bool == False:
                self.max_pulses = self.total_pulses
                self.max_disp = (self.max_pulses)*(self.distance/self.max_pulses)
                self._SW_fin_bool = True


    def foward(self):
        #self.direction = True
        #GPIO.output(self._ENA, GPIO.LOW)

        if self.movement==False:
            self.start()
        GPIO.output(self._DIR_out, GPIO.HIGH)
        #self.pwm.start(self._duty_cycle)  # start PWM of required Duty Cycle

    def backward(self):
        #self.direction = False
        #GPIO.output(self._ENA, GPIO.LOW)
        if self.movement==False:
            self.start()
        GPIO.output(self._DIR_out, GPIO.LOW)
        #self.pwm.start(self._duty_cycle)  # start PWM of required Duty Cycle

    def change_velocity(self, frequency):
        if frequency>self._max_freq:
            frequency=self._max_freq
        elif frequency<self._min_freq:
            frequency = self._min_freq
        #self.pwm.ChangeFrequency(frequency)
        self.pwm.set_pwm_freq(frequency)


    def start(self):
        self.movement = True
        GPIO.output(self._ENA, GPIO.LOW)
        #self.pwm.start(self._duty_cycle)  # start PWM of required Duty Cycle
        self.pwm.set_pwm(self.PUL_pwm, 0, 100)

    def stop(self):
        self.movement = False
        GPIO.output(self._ENA, GPIO.LOW)
        #self.pwm.stop()
        self.pwm.set_pwm(self.PUL_pwm, 0, 0)
        sleep(0.01)


    def setup(self):
        time_bounce = round(1000*(1/self._max_freq)*0.9)*0
        if time_bounce>0:
            GPIO.add_event_detect(self._PUL_in, GPIO.RISING, callback=self.count_pulses, bouncetime=time_bounce)
        else:
            GPIO.add_event_detect(self._PUL_in, GPIO.RISING, callback=self.count_pulses)

        GPIO.add_event_detect(self._DIR_in, GPIO.BOTH, callback=self.direction_change)
        GPIO.add_event_detect(self._SW_ini, GPIO.FALLING, callback=self.direction_change_true)
        GPIO.add_event_detect(self._SW_fin, GPIO.FALLING, callback=self.direction_change_false)


    def calibration(self):
        self.start()
        self._SW_ini_bool = False
        self._SW_fin_bool = False
        self._calibration_bool = True
        print("Calibration: Started.")
        print("Calibration Initial: Started 1. Actual Pulses = ", self.total_pulses, " Position =",  round(self.position,2))
        self.backward()
        while self._calibration_bool:
            if self._SW_ini_bool == False:
                pass
            else:
                break
        print("Calibration Initial: Completed 1. Actual Pulses = ", self.total_pulses, " Position =", round(self.position,2))
        print("Calibration Final: Started.")
        self.foward()
        self._SW_fin_bool = False
        while self._calibration_bool:
                if self._SW_fin_bool == False:
                    pass
                else:
                    break
        print("Calibration Final: Completed.  Total Max Pulse = ", self.max_pulses, " Position =",  round(self.position,2))

        print("Calibration Initial: Started 2. Actual Pulses = ", self.total_pulses, " Position =",  round(self.position,2))
        self.backward()
        self._SW_ini_bool = False
        while self._calibration_bool:
            if self._SW_ini_bool == False:
                pass
            else:
                break
        print("Calibration Initial: Completed 2. Actual Pulses = ", self.total_pulses, " Position =",  round(self.position,2))
        self._calibration_bool = False
        print("Calibration: Completed.")
        print("Calibration Final: Completed.  Total Max Pulse = ", self.max_pulses, "Total Max Distance = ", self.max_disp)
        self.stop()
        print("Stop Motors")



