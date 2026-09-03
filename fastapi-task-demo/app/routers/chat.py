"""SSE 流式聊天路由。

这个示例重点展示 async def + yield + ServerSentEvent 的配合，后续可以把模拟 answer 替换成真实 LLM 流。
"""

import asyncio

from fastapi import APIRouter
from fastapi.sse import EventSourceResponse, ServerSentEvent

from app.schemas.chat import ChatRequest


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/stream",

    # EventSourceResponse 表示：
    # 这个接口不是一次性返回普通 JSON，而是持续发送 SSE 事件流。
    response_class=EventSourceResponse,
    summary="LLM 流式聊天",
)
async def chat_stream(
    data: ChatRequest,
):
    # yield 和 return 的关键区别：
    # return -> 一次返回后函数结束；
    # yield  -> 发送一部分数据，但函数以后还能继续往下运行。

    # 1. 先告诉前端：生成开始了。
    yield ServerSentEvent(
        data={
            "message": "generation started"
        },
        event="start",
    )

    # 2. 这里暂时不用真正的大模型，先模拟 LLM 输出。
    answer = (
        f"收到你的问题：{data.message}。"
        "这是一个模拟的流式回答。"
    )

    # 一次只发送一个字符，模拟 ChatGPT 一点点输出文字。
    for char in answer:
        # sleep 是为了模拟模型生成延迟。
        # 因为这是 async def，所以这里使用 await asyncio.sleep，
        # 不会像 time.sleep 那样直接阻塞当前事件循环。
        await asyncio.sleep(0.05)

        # ServerSentEvent 表示“一条 SSE 事件”。
        yield ServerSentEvent(
            data={
                "content": char
            },
            event="token",
        )

    # 3. 最后发送 done 事件，告诉前端流已经结束。
    yield ServerSentEvent(
        raw_data="[DONE]",
        event="done",
    )
