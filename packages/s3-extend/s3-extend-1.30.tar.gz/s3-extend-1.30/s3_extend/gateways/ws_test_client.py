#!/usr/bin/env python

import asyncio
import json
from websockets.sync.client import connect


def hello():
    with connect("ws://localhost:9002") as websocket:
        # msg = JSON.stringify({"id": "to_esp8266_gateway"});
        payload = json.dumps({"id": "to_esp8266_gateway"})
        # websocket.send("Hello world!")
        message = websocket.recv()
        print(f"Received: {message}")


hello()
