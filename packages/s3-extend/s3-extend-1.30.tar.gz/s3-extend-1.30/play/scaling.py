
def scale(value, new_value_low, new_value_high ):


    input_low = 0
    input_high = 100

    return round(((value ) * ((new_value_high - new_value_low) /100)) +
                new_value_low)


while True:
    value, new_value_low, new_value_high = input('val low high').split()

    print(scale(int(value), int(new_value_low), int(new_value_high)))
