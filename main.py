#pip install urllib3==1.26.6
#pip install pipreqs
#pipreqs --force

import threading
install_all = False


if install_all:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip3", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip3", "install", "-r", "requirements.txt"])
    subprocess.check_call([sys.executable, "-m", "pip3", "install", "Adafruit-PCA9685==1.0.1"])


from Sequencia_Class import *

def pwm_task():
    sleep(0)

def print_task():
    #print("Pulses=", sequencia.motor_X.total_pulses, " Position=", sequencia.motor_X.position)
    pass
# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    print("Test Begin")
    Y_bool = sequencia.motor_Y.direction

    try:
        while True:

            #X_bool = sequencia.trajectory_X(X_bool)
            Y_bool = sequencia.trajectory_Y(Y_bool)
            sequencia.update_file()

            #
            #print("Test Begin")

            #print("Pulses=", motor_X.total_pulses, " Position=", motor_X.position)
            #print("Pulses=", sequencia.motor_X.total_pulses, " Position=", round(sequencia.motor_X.position,2))
            print("X - Pulses=", sequencia.motor_X.total_pulses, " Position=", round(sequencia.motor_X.position, 2),
                  "Y - Pulses=", sequencia.motor_Y.total_pulses, " Position=", round(sequencia.motor_Y.position, 2))
            #pwm_thread = threading.Thread(target=pwm_task)
            #print_thread = threading.Thread(target=print_task)

            #pwm_thread.start()
            #print_thread.start()

            #pwm_thread.join()
            #print_thread.join()



    except KeyboardInterrupt:
            sequencia.stop()
            print("cleanup")
            GPIO.cleanup()