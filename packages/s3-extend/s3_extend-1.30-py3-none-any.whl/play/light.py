while True:
    value = input('value: ')
    value = int(value)
    if value < 25:
        print(100-value)
    else:
        print((1023-value) * (75/998))
