import asyncio
import time
async def io_task(name:str, seconds:str):
    print("f{name}kaishi")
    await asyncio.sleep(seconds)
    print("f{name}wancheng")
    return name

async def concurrent():
    await asyncio.gather(
        io_task("任务A", 2),
        io_task("任务B", 2),
        io_task("任务C", 2),
    )

async def main():
    start =time.perf_counter()
    await concurrent()
    end =time.perf_counter()
    
    print(f"并发耗时：{end - start:.2f} 秒")
    
asyncio.run(main())