#pip install urllib3==1.26.6
#pip install pipreqs
#pipreqs --force

import threading
install_all = True


if install_all:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Adafruit-PCA9685==1.0.1"])


from Sequencia_Class import *
#from Motor_Class import *

#motor_X = Motor(ENA = 17, PUL_out = 18, DIR_out = 27, PUL_in = 7, DIR_in = 12 , SW_ini = 23, SW_fin = 24)

def pwm_task():
    sleep(0)

def print_task():
    #print("Pulses=", sequencia.motor_X.total_pulses, " Position=", sequencia.motor_X.position)
    pass
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Test Begin 2")

    try:
        while True:
            #motor_X.calibration()
            sleep(4)
            #print("Test Begin")

            #print("Pulses=", motor_X.total_pulses, " Position=", motor_X.position)
            print("Pulses=", sequencia.motor_X.total_pulses, " Position=", sequencia.motor_X.position)
            #pwm_thread = threading.Thread(target=pwm_task)
            #print_thread = threading.Thread(target=print_task)

            #pwm_thread.start()
            #print_thread.start()

            #pwm_thread.join()
            #print_thread.join()



    except KeyboardInterrupt:
            print("cleanup")
            GPIO.cleanup()