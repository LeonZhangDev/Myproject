"""HTTP 请求日志中间件。

中间件位于“请求进入路由之前”和“响应离开路由之后”，很适合做日志、耗时统计、追踪 ID 等公共工作。
"""

import time

from fastapi import Request


async def request_log_middleware(
    request: Request,
    call_next,
):
    """
    统计每次 HTTP 请求的处理时间。

    request:   当前请求对象，可读取 method、url、headers 等。
    call_next: 把请求继续交给后面的路由处理。
    """

    # perf_counter() 很适合计算一段代码实际耗时。
    start_time = time.perf_counter()

    # await call_next(request) 相当于：
    # “中间件先放行，让真正的接口继续处理请求”。
    response = await call_next(request)

    # 接口返回后，程序又回到中间件这里继续执行。
    process_time = time.perf_counter() - start_time

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"{response.status_code} "
        f"{process_time:.4f}s"
    )

    # 把后端处理耗时写入响应 Header。
    # 前端最终可以看到类似：X-Process-Time: 0.0013
    response.headers["X-Process-Time"] = (
        f"{process_time:.4f}"
    )

    return response
