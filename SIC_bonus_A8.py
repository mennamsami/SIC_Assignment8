import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime
import time

monitoring_period = 300 # ( 5 minutes )

while True:
    
    current_time = datetime.datetime.now()

    file_date = current_time - datetime.timedelta(days=1)
    file_name = file_date.strftime("%Y-%m-%d") + "-pub.log"

    try:
        # Loading the log file into a Pandas Frame
        df = pd.read_csv(file_name, header=None, names=["timestamp", "cpu_usage", "num_logical_cpus", "used_memory", "used_disk_space", "current_host_ip"])

        # Convert the timestamp column to a datetime (object)
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S")

        df["hour"] = df["timestamp"].dt.hour
        df["minute"] = df["timestamp"].dt.minute

        # X and y arrays for linear regression
        X = df[["hour", "minute"]]
        y = df["cpu_usage"]

        # Linear regression model to the data
        model = LinearRegression()
        model.fit(X, y)

        # Predicting of the CPU usage for the next day at 12:00 PM
        prediction_date = file_date + datetime.timedelta(days=1)
        prediction_time = datetime.time(hour=12, minute=0, second=0)
        prediction_datetime = datetime.datetime.combine(prediction_date, prediction_time)
        prediction_hour = prediction_datetime.hour
        prediction_minute = prediction_datetime.minute
        prediction = model.predict([[prediction_hour, prediction_minute]])

        # Print the predicted CPU usage for the next day
        print("Predicted CPU usage for " + prediction_date.strftime("%Y-%m-%d") + " at 12:00 PM: " + str(prediction))

    except FileNotFoundError:
        # If the log file for the previous day is not found, it will print an error message
        print("Log file for " + file_date.strftime("%Y-%m-%d") + " error, not found")

    # delay
    time.sleep(monitoring_period)