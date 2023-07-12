from Motor_Class import *

class Sequencia(Motor):
    def __init__(self, ):
        self.motor_X = Motor(ENA = 14, PUL_out = 18, DIR_out = 15, PUL_in = 12, DIR_in = 7 , SW_ini = 23, SW_fin = 24)
        #self.motor_Y = Motor(ENA = 14, PUL_out = 18, DIR_out = 15, PUL_in = 12, DIR_in = 7 , SW_ini = 23, SW_fin = 24)

sequencia = Sequencia()