"""项目公共配置。

把会被多个模块使用的配置集中放在这里，避免在路由文件中重复写常量。
后续接入环境变量时，也可以优先从这一层改造。
"""

from pathlib import Path


# Path("uploads") 表示 uploads 文件夹。
# mkdir(..., exist_ok=True) 表示：没有就创建，已经存在也不报错。
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# 最大上传大小：5 MB。
# 5 * 1024 * 1024 = 5,242,880 字节。
MAX_FILE_SIZE = 5 * 1024 * 1024


# 浏览器会把“协议 + 域名/IP + 端口”视为一个 Origin。
# 例如 localhost:5173 和 127.0.0.1:5173 是两个不同 Origin。
ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
