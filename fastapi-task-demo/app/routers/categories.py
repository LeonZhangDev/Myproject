"""Category 相关接口。"""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies.auth import verify_token
from app.exceptions.app_exception import AppException
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse
from app.schemas.common import ErrorResponse


router = APIRouter(
    prefix="/categories",
    tags=["Category"],
)


@router.get(
    "",
    response_model=list[CategoryResponse],
    summary="查询分类",
)
async def get_categories(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(verify_token),
):
    result = await db.execute(
        select(Category).order_by(Category.id)
    )
    return result.scalars().all()


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=201,
    summary="创建分类",
    responses={
        409: {
            "model": ErrorResponse,
            "description": "分类已存在",
        },
    },
)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(verify_token),
):
    # begin() 划定事务范围：正常退出自动 COMMIT，异常自动 ROLLBACK。
    async with db.begin():
        existing = await db.scalar(
            select(Category).where(
                Category.name == data.name
            )
        )

        if existing is not None:
            raise AppException(
                status_code=409,
                code=40901,
                message="Category already exists",
                data={"name": data.name},
            )

        category = Category(
            name=data.name,
        )
        db.add(category)

        # flush 把 INSERT 发给数据库，从而拿到 category.id；
        # 但此时事务仍可以回滚，并不是 commit。
        await db.flush()

    await db.refresh(category)
    return category
