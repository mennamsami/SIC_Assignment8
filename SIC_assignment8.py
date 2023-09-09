import psutil
import time
import datetime
#To import the necessary modules for the script: psutil for system process information, time for waiting between iterations, and datetime for getting the current date and time.

monitoring_period = 5 
memory_Tpercentage = 80
#To set the monitoring period and memory percentage. monitoring_period is the number of seconds between each iteration of the loop, and memory_percentage is the percentage of memory usage above which a notification file will be created.

current_time = datetime.datetime.now()
log_file_name = current_time.strftime("%Y-%m-%d") + "-pub.log"
notification_file_name = current_time.strftime("%Y-%m-%d") + "-notification.log"
log_file = open(log_file_name, "a")
#To get the current date and time using datetime.datetime.now() and format it as a string in the format "YYYY-MM-DD" using strftime().

while True:
    now = datetime.datetime.now()
    cpu_usage = psutil.cpu_percent()
    num_logical_cpus = psutil.cpu_count(logical=True)
    used_memory = psutil.virtual_memory().percent
    used_disk_space = psutil.disk_usage('/').percent
    current_host_ip = psutil.net_if_addrs()['eth0'][0].address
    log_file.write(now.strftime("%Y-%m-%d %H:%M:%S") + ", " + str(cpu_usage) + ", " + str(num_logical_cpus) + ", " + str(used_memory) + ", " + str(used_disk_space) + ", " + current_host_ip + "\n")
    if used_memory > memory_Tpercentage:
        notification_file = open(notification_file_name, "w")
        notification_file.write("Low memory detected")
        notification_file.close()
    time.sleep(monitoring_period)
#Then it will run continuously until the loop is stopped. Within the loop,
#the current date and time are obtained, along with system process information using psutil module. The information is then written to the log file using log_file.write() in the format specified in the instructions. If memory usage exceeds the threshold, a notification file is created "Low memory detected". The loop then waits for the monitoring period using time.sleep() before starting the next iteration.

