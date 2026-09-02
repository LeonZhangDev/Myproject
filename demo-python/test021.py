import asyncio
import time

async def io_task(name:str, seconds:int):
    print(f"{name}kaishi")
    
    await asyncio.sleep(seconds)
    
    print(f"{name}wancheng")
    
    return name

async def serial():
    await io_task("taskA",2)
    await io_task("taskB",2)
    await io_task("taskC",2)
    
async def main():
    start =time.perf_counter()
    await serial()
    end = time,perf_counter()
    print(f"xiaohao:{start-end}")
    
asyncio.run(main())