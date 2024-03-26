while True:
    value = int(input('value: '))

    n = max( 0, value-18)
    if n<50:
        print(int(n/2))
    else:
        print(25 + min( 75, int( (n-50) * (75/580) ) ))
