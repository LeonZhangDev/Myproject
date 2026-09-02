from fastapi import FastAPI, Request
import time
app = FastAPI()


@app.middleware("http")
async def my_middleware(
    request: Request,
    call_next,
):
    start_time = time.perf_counter()
    print("请求进来了")
    print("方法:", request.method)
    print("路径:", request.url.path)

    response = await call_next(request)

    print("响应要回去了")
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(
        process_time
    )
    print(
        request.method,
        request.url.path,
        start_time,
        process_time,
    )

    return response


@app.get("/test")
def test():
    print("正在执行 /test 接口")
    return {
        "message": "测试成功"
    }