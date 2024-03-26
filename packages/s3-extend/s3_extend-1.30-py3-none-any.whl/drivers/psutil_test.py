import psutil

# check to see if the backplane is already running
try:
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        # print(proc.info['pid'], proc.info['name']) # list all found processes
        if 'backplane' in proc.info['name']:
            skip_backplane = True
            print(proc) # found!
except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
    pass
