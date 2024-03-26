import asyncio
import sys


async def ainput(string: str) -> str:
    await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s+' '))
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
buf = []
loop.run_until_complete(ainput(buf))
# while True:
#     z = await ainput(buf)
#     print(z)