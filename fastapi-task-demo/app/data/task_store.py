"""临时的数据存储层。

当前用 list 模拟数据库，方便先学习 FastAPI。以后接 SQLAlchemy 时，可以逐步把这里替换成真正的数据库访问代码。
"""

# 目前还没有接 MySQL / PostgreSQL / SQLAlchemy，
# 所以先用 Python list + dict 模拟数据库表。
#
# 注意：程序一重启，这里的运行时修改就会丢失。
# 后面学习数据库后，可以把这一层替换成真正的数据访问层。

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "description": "学习 FastAPI",
        "completed": False,
    },
    {
        "id": 2,
        "title": "Learn Pydantic",
        "description": "学习 Pydantic",
        "completed": True,
    },
]
