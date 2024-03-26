import asyncio
import websockets
import json


async def hello():
    # uri = "ws://127.0.0.1:9002"
    uri = "ws://127.0.0.1:9000"

    async with websockets.connect(uri) as websocket:
        # msg = json.dumps({"id": "to_esp8266_gateway"})
        msg = json.dumps({"id": "to_arduino_gateway"})

        await websocket.send(msg)
        # await asyncio.sleep(.2)
        # Change the ip address to match your ESP-8266
        # msg = json.dumps({"command": "ip_address", "address": "192.168.2.112"})
        #  await websocket.send(msg)
        # await asyncio.sleep(.2)

        # change the pin number if you need to
        msg = json.dumps({"command": "set_mode_digital_output", "pin": 6})
        await websocket.send(msg)
        # await asyncio.sleep(.2)

        while True:
            # change the pin number if you need to
            msg = json.dumps({"command": "digital_write", "pin": 6,
                                            "value": 1})
            await websocket.send(msg)

            await asyncio.sleep(.02)

            # change the pin number if you need to
            msg = json.dumps({"command": "digital_write", "pin": 6,
                              "value": 0})
            await websocket.send(msg)
            await asyncio.sleep(.02)


asyncio.run(hello())
