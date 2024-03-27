how to use this package:

after you download the package from PyPi

import this package like the following

import YasinDataPrepKit as Dtk

your can read a csv, json and Excel files and in order to do
that your need to do the next:

first you need to make an object and call the ReadingData class

obj = dtk.ReadingData(r"Your file absolute path")

make sure to always use (r"")when reading your data for 
correctly read your file path

after this your call the read() function like this

df = obj.read()

to print your data

print(df)

after you have done these steps correctly then the rest is easy 
you can do many function for data summary for instance:

to find mean of int and float columns you use

print(obj.calculate_mean())

to find the maximum

print(obj.max_value())

for handling missing values you can use either the remove or 
impute methods

print(obj.handle_missing_values('remove'))
print(obj.handle_missing_values('impute'))

the 'remove' and 'impute' is you specifying the strategy you
want to use to handle missing values


there is also a function for encoding using one hot encoding

print(obj.encode_categorical_data())


here is a list for all functions other than the ones above that 
you can use from this package

to calculate sum

print(obj.calculate_sum())

to calculate minimum

print(obj.min_value())

to calculate median

print(obj.median_value())

to calculate variance

print(obj.var_value())

to calculate standard deviation

print(obj.std_deviation())

to calculate correlation coefficient

print(obj.cor_coefficient())
