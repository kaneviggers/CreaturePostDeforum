from secondaryWindow import *
import asyncio

async def openWindow():
    init()

async def main():
    asyncio.create_task(openWindow())

asyncio.run(main())