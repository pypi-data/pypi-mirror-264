import supervisor

print("listening...")

while True:
    # if supervisor.runtime.serial_bytes_available:
    value = input().strip()
    # Sometimes Windows sends an extra (or missing) newline - ignore them
    if value == "":
        continue
    if value == 'v':
        print("RX: Got it")
