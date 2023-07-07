#pip install urllib3==1.26.6
#pip install pipreqs

from Motor_Class import *
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Test Begin")
    try:
        while True:
            sleep(10)
            print("Test Begin")
            #motor_X.foward()
    except KeyboardInterrupt:
            print("cleanup")
            GPIO.cleanup()