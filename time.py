# import time
import datetime

# Initializing a date and time 
date_and_time = datetime.datetime.now()
  
print("Original time:") 
print(date_and_time) 
  
# Calling the timedelta() function  
time_change = datetime.timedelta(minutes=29) 
new_time = date_and_time + time_change 
  
# Printing the new datetime object 
print("changed time:") 
print(new_time) 