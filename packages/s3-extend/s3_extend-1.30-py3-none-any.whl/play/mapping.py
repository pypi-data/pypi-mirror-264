# original range is from 0 - 100
# we wish to map a value within that range to a value in a new range

# Here is an example of use:
# Enter value you wish to convert to a new value:55
# Enter new range starting value: -240
# Enter new range ending value:240
# The converted value is:  24


a = 0 # original range low value
b = 100 # original range high value

while True:
    x = int(input("Enter value you wish to convert to a new value:"))
    c = int(input("Enter new range starting value: "))
    d = int(input("Enter new range ending value:"))

    print('The converted value is: ', round(((x-a)*((d-c)/(b-a)))+ c))

