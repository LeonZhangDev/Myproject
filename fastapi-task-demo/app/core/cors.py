"""CORS 配置。

把跨域规则从 main.py 拆出来，使应用入口只保留 setup_cors(app) 这一行注册代码。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import ORIGINS


def setup_cors(app: FastAPI) -> None:
    """给 FastAPI 应用添加 CORS 中间件。"""

    app.add_middleware(
        CORSMiddleware,

        # 哪些前端地址允许调用后端。
        allow_origins=ORIGINS,

        # 是否允许携带 Cookie、Authorization 等凭证。
        allow_credentials=True,

        # 浏览器允许跨域调用哪些 HTTP 方法。
        # OPTIONS 是浏览器跨域请求时常见的“预检请求”。
        allow_methods=[
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "OPTIONS",
        ],

        # 前端跨域请求允许携带哪些 Header。
        allow_headers=[
            "Content-Type",
            "Authorization",
            "X-Token",
        ],

        # 默认情况下，浏览器 JS 不一定能读取所有响应 Header。
        # expose_headers 让前端可以读取 X-Process-Time。
        expose_headers=[
            "X-Process-Time",
        ],
    )
