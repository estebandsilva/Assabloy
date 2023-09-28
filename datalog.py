import os
import time
from datetime import datetime

def create_folder_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def write_info_to_file(file_path, info):
    with open(file_path, 'a') as f:
        f.write(info + '\n')

def create_file():
    now = datetime.now()
    folder_name = os.path.join('DATALOG', now.strftime('%d-%m-%Y'))
    #file_name = now.strftime('%H-%M-%S-%f')[:-3] + '.txt'
    file_name = now.strftime('%H-%M-%S') + '.txt'
    file_path = os.path.join(folder_name, file_name)
    create_folder_if_not_exists(folder_name)
    #info = "timestamp,dd_mm_yyyy,hh_mm_ss,x_position,y_position"
    info = "timestamp,x_position,y_position"
    write_info_to_file(file_path, info)

    return file_path

def datalog(file_path, x_position, y_position):

    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    dd_mm_yyyy = now.strftime('%d:%m:%Y')
    hh_mm_ss = now.strftime('%H:%M:%S.%f')[:-3]
    #x_position =  # Replace with your X position value
    #y_position =  # Replace with your Y position value


    '''
    # Generate a unique filename based on the current minute
    filename = now.strftime("%Y-%m-%d_%H-%M.txt")

    # Create and open the log file in append mode
    log_file_path = os.path.join(log_directory, filename)
    with open(log_file_path, "a") as log_file:
        log_file.write(f"Logging data at {current_time}\n")

    '''


    #info = f"Timestamp: {timestamp}, DD:MM:YYYY: {dd_mm_yyyy}, HH:MM:SS: {hh_mm_ss}, X pos: {x_position}, Y pos: {y_position}"
    #info = f"{timestamp},{dd_mm_yyyy},{hh_mm_ss},{x_position},{y_position}"
    info = f"{timestamp},{round(x_position, 2)},{round(y_position, 2)}"
    write_info_to_file(file_path, info)


if __name__ == "__main__":
    datalog()
