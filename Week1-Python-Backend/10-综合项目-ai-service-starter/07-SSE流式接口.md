---
tags: [week1, project]
difficulty: P0
status: learning
---
# SSE 流式接口
```python
async def events():
    for token in ["你","好","！"]:
        await asyncio.sleep(0.2)
        yield ServerSentEvent(event="token",data=token)
return EventSourceResponse(events())
```

关联：[[../08-流式通信/02-SSE]]。
