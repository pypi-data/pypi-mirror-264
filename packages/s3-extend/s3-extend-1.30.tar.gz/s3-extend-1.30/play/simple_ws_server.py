import asyncio
import websockets
import json

async def hello(websocket, path):
    data = await websocket.recv()
    print('got something')

    # expecting an id string from client
    data = json.loads(data)

    # greeting = f"Hello {name}!"

    # await websocket.send(greeting)
    # print(f"> {greeting}")


start_server = websockets.serve(hello, "localhost", 9400)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
