import json

payload = '{"ipaddr": "192.1.33.55"}'

z = json.loads(payload)
q = z['ipaddr']

if 'ipaddr' in payload:
    payload = payload.split(": ")
    payload = payload[1][:-1]
    ipaddr = payload[1:-2]
    sock_address = (ipaddr, 9000)
    # first = payload.split(": ")
    # print(ip_addr)
    print(sock_address)


