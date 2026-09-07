"""聊天接口的请求模型。"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    # 客户端 POST /chat/stream 时提交：
    # {"message": "你好"}
    message: str
