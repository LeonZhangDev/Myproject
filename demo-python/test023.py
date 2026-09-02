import asyncio
import time


async def io_task(name: str, seconds: int):
    print(f"{name} 开始")

    await asyncio.sleep(seconds)

    print(f"{name} 完成")

    return name


async def run_serial():
    await io_task("任务A", 2)
    await io_task("任务B", 2)
    await io_task("任务C", 2)


async def run_concurrent():
    await asyncio.gather(
        io_task("任务A", 2),
        io_task("任务B", 2),
        io_task("任务C", 2),
    )
    
async def main():

    print("===== 串行执行 =====")

    start = time.perf_counter()

    await run_serial()

    serial_time = time.perf_counter() - start

    print(f"串行耗时：{serial_time:.2f} 秒")

    print()

    print("===== 并发执行 =====")

    start = time.perf_counter()

    await run_concurrent()

    concurrent_time = time.perf_counter() - start

    print(f"并发耗时：{concurrent_time:.2f} 秒")

    print()

    print("===== 对比 =====")

    print(f"串行：{serial_time:.2f} 秒")
    print(f"并发：{concurrent_time:.2f} 秒")
    print(f"节省：{serial_time - concurrent_time:.2f} 秒")


asyncio.run(main())