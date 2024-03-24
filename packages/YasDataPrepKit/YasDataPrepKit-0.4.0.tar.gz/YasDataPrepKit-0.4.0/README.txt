How to use:

import YasDataPrepKit as dtk

#create an object and call the class like this:
obj = dtk.ReadingData(r"Your file path")
#to read the data you call the read() function
Read_data = obj.read()

#after this you can call the functions you want, for example:

#you can calculate the mean for your columns with int or float values like this:

print(obj.calculate_mean())