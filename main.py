#pip install urllib3==1.26.6
#pip install pipreqs
import threading


from Motor_Class import *

def pwm_task():
    sleep(0)

def print_task():
    print("Pulses=", motor_X.total_pulses, " Position=", motor_X.position)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Test Begin")



    try:
        while True:
            sleep(10)
            #print("Test Begin")
            #motor_X.foward()
            #print("Pulses=", motor_X.total_pulses, " Position=", motor_X.position)
            #pwm_thread = threading.Thread(target=pwm_task)
            #print_thread = threading.Thread(target=print_task)

            #pwm_thread.start()
            #print_thread.start()

            #pwm_thread.join()
            #print_thread.join()



    except KeyboardInterrupt:
            print("cleanup")
            GPIO.cleanup()