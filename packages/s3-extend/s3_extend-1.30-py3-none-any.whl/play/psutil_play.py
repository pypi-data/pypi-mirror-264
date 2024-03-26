import psutil
import sys

# iterate through all the processes
for proc in psutil.process_iter(attrs=['pid', 'name']):
    # check if backplane is running
    if 'backplane' in proc.info['name']:
        print('Backplane is running')
        sys.exit(0)
    else:
        # print out process name other than backplane
        # for all processes found
        print(proc.info['name'])

print('Backplane is not running')
