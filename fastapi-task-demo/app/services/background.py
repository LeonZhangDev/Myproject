"""可复用的后台业务函数。

services 层放“做事情”的代码；router 只决定什么时候调用它们。
"""

def process_pdf(
    file_path: str,
):
    """
    PDF 上传成功后执行的后台任务。

    重点：客户端不需要等这个函数执行完成，
    HTTP 响应可以先返回，然后 FastAPI 再执行这里的轻量任务。
    """

    print(
        f"开始处理 PDF: {file_path}"
    )

    # 以后这里可以继续扩展成：
    # 1. 解析 PDF
    # 2. chunk 文本切块
    # 3. embedding 向量化
    # 4. 写入向量数据库

    print(
        f"PDF 处理完成: {file_path}"
    )


def write_task_log(
    message: str,
):
    """创建任务后，后台追加一条日志到 task.log。"""

    # "a" = append（追加模式），不会覆盖之前的日志。
    with open(
        "task.log",
        "a",
        encoding="utf-8",
    ) as f:
        f.write(message + "\n")
