import asyncio


async def main():
        await asyncio.sleep(5)
        print('hello')

asyncio.run(main())

print('world')