"""文件上传路由。

这里处理 HTTP 上传流程；上传后的 PDF 处理逻辑放到 services/background.py，避免路由函数承担过多职责。
"""

from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, UploadFile

from app.core.config import MAX_FILE_SIZE, UPLOAD_DIR
from app.exceptions.app_exception import AppException
from app.services.background import process_pdf


# prefix="/upload" 表示这个文件里所有接口都会自动带 /upload 前缀。
# 所以下面的 @router.post("/pdf") 最终路径就是：/upload/pdf
router = APIRouter(
    prefix="/upload",
    tags=["File"],
)


@router.post(
    "/pdf",
    status_code=202,
    summary="上传 PDF",
)
async def upload_pdf(
    file: UploadFile,
    background_tasks: BackgroundTasks,
):
    # UploadFile.content_type 是客户端上传文件时携带的 MIME 类型。
    if file.content_type != "application/pdf":
        raise AppException(
            status_code=400,
            code=40001,
            message="Only PDF files are allowed",
        )

    # file.read() 是异步方法，所以要 await。
    # 这里先读完整内容，是为了后面检查文件大小并写入磁盘。
    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise AppException(
            status_code=413,
            code=41301,
            message="File is too large",
            data={
                "max_size_mb": 5,
            },
        )

    # Path(...).name 只保留最终文件名，
    # 可避免客户端通过 ../../xxx 之类路径影响保存位置。
    safe_filename = Path(
        file.filename or "upload.pdf"
    ).name

    file_path = UPLOAD_DIR / safe_filename

    # "wb" = write binary，以二进制形式保存 PDF。
    with open(
        file_path,
        "wb",
    ) as f:
        f.write(content)
    # 注意这里传的是函数 process_pdf 本身，不是 process_pdf(...) 的执行结果。
    background_tasks.add_task(
        process_pdf,
        str(file_path),
    )

    # 202 Accepted 表示请求已经接受，后台处理可以继续进行。
    return {
        "filename": safe_filename,
        "content_type": file.content_type,
        "size": len(content),
        "path": str(file_path),
    }
