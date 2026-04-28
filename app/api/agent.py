# ============================================================
# agent.py —— Agent 接口模块
# ============================================================
# 这个文件是给"智能助手"（Agent）用的接口。
# Agent 可以通过这里的接口：
#   1. 直接查询数据库（只能查，不能改，保证安全）
#   2. 把查询结果保存成 Excel 文件，或者写入数据库新表
#
# 为什么需要这个模块？
#   系统里其他接口都是固定的（比如只能查学生、只能查成绩），
#   Agent 可能需要灵活地查任意数据，所以单独开了一组接口。
# ============================================================

# --- 导入外部工具 ---
# typing 是 Python 自带的类型提示工具，让代码更清晰
from typing import Any, Literal

# pandas 是处理表格数据的库，就像 Excel 的 Python 版本
import pandas as pd

# FastAPI 是写 Web 接口的框架
# APIRouter 用来把一组接口打包成一个模块
# Depends 用来声明"这个参数需要依赖某个函数来提供"
# HTTPException 用来返回错误信息给前端
# status 里放了很多 HTTP 状态码的常量
from fastapi import APIRouter, Depends, HTTPException, status

# pydantic 用来定义"数据长什么样"，自动检查前端传的数据对不对
from pydantic import BaseModel, Field

# SQLAlchemy 是操作数据库的工具
# text 用来把普通字符串变成安全的 SQL 语句
from sqlalchemy import text
# Session 是数据库的"会话"，一次操作数据库的过程
from sqlalchemy.orm import Session

# --- 导入我们自己项目的工具 ---
# get_db 是一个函数，用来获取数据库连接
from app.core.database import get_db
# require_role 是一个检查权限的工具，只有管理员和老师能用这些接口
from app.dependencies import require_role
# ApiResponse 是我们统一的返回格式，所有接口都包成 {message, data} 的样子
from app.schemas.response import ApiResponse


# ============================================================
# 创建路由（Router）
# ============================================================
# router 就像快递的分拣中心，所有以 /agent 开头的请求都会送到这里处理
# prefix='/agent' 表示这些接口的网址前面都要加 /agent
# tags=['Agent接口'] 是在接口文档里给这组接口起个分类名字
router = APIRouter(prefix='/agent', tags=['Agent接口'])


# ============================================================
# 定义数据格式（Pydantic 模型）
# ============================================================
# 这些类规定了前端传什么数据、后端返回什么数据。
# 如果前端传的数据格式不对，FastAPI 会自动报错。

class SQLQueryRequest(BaseModel):
    """SQL 查询请求的数据格式"""
    # ... 表示这个字段必须传，不能为空
    # description 是在接口文档里显示的说明文字
    sql: str = Field(..., description='要执行的SQL查询语句（仅支持SELECT）')
    # | None 表示这个字段可以传，也可以不传
    # default=None 表示如果不传，默认就是 None（空）
    params: dict[str, Any] | None = Field(default=None, description='SQL参数')


class SQLQueryResponse(BaseModel):
    """SQL 查询返回的数据格式"""
    columns: list[str]           # 查询结果有哪些列，比如 ['姓名', '年龄']
    rows: list[dict[str, Any]]   # 每一行的数据，用字典表示
    row_count: int               # 一共查到了多少行


class SaveRequest(BaseModel):
    """保存数据请求的数据格式"""
    # Literal 表示这个字段只能是几个固定值中的一个
    source_type: Literal['sql', 'data'] = Field(..., description='数据来源类型：sql 或 data')
    # 当 source_type 选 'sql' 时，需要传 sql 语句
    sql: str | None = Field(default=None, description='当 source_type=sql 时，要执行的SELECT语句')
    params: dict[str, Any] | None = Field(default=None, description='SQL参数')
    # 当 source_type 选 'data' 时，需要直接传数据
    data: list[dict[str, Any]] | None = Field(default=None, description='当 source_type=data 时，要保存的数据')
    # target_type 表示要保存到哪里
    target_type: Literal['xlsx', 'db'] = Field(..., description='保存目标：xlsx 或 db')
    # 当 target_type 选 'db' 时，需要告诉系统写到哪个表
    table_name: str | None = Field(default=None, description='当 target_type=db 时，要写入的数据库表名')
    # 当 target_type 选 'xlsx' 时，需要告诉系统文件存到哪里
    file_path: str | None = Field(default=None, description='当 target_type=xlsx 时，xlsx文件保存路径（相对或绝对）')


# ============================================================
# 辅助函数（不直接对外提供接口，只给上面的接口内部使用）
# ============================================================

def _validate_select_only(sql: str) -> None:
    """
    检查 SQL 语句是否只包含 SELECT（查询），不包含其他危险操作。

    为什么要检查？
        如果允许任意 SQL，有人可能会传 "DELETE FROM 学生表"，把数据全删了。
        所以只允许查询（SELECT），不允许增删改（INSERT/UPDATE/DELETE）。

    参数：
        sql: 前端传来的 SQL 语句字符串

    返回值：
        没有返回值。如果检查不通过，直接抛出错误，阻止执行。
    """
    # strip() 去掉字符串前后的空格
    # lower() 把所有字母变成小写，方便统一判断
    stripped = sql.strip().lower()

    # 必须以 select 开头
    if not stripped.startswith('select'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,  # 400 表示请求参数错误
            detail='仅允许执行SELECT查询语句',
        )

    # 禁止出现这些危险关键字
    forbidden = ['insert', 'update', 'delete', 'drop', 'truncate', 'alter', 'create', 'grant', 'revoke']
    for keyword in forbidden:
        if keyword in stripped:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'SQL中包含禁止的关键字: {keyword}',
            )


def _rows_to_dicts(rows: Any, columns: list[str]) -> list[dict[str, Any]]:
    """
    把数据库查出来的原始行数据，转换成字典列表。

    为什么要转换？
        数据库返回的数据是特殊的"行对象"，前端看不懂，
        转换成字典后，前端就能直接用了。

    参数：
        rows: 数据库返回的原始行数据
        columns: 这一批数据有哪些列名

    返回值：
        一个列表，里面每个元素都是一个字典，比如：
        [{'姓名': '张三', '年龄': 20}, {'姓名': '李四', '年龄': 21}]
    """
    result: list[dict[str, Any]] = []
    for row in rows:
        # 有的行对象有 _mapping 属性，可以直接转成字典
        if hasattr(row, '_mapping'):
            result.append(dict(row._mapping))
        else:
            # 如果没有 _mapping，就用 zip 把列名和值一一配对
            result.append(dict(zip(columns, row)))
    return result


# ============================================================
# 对外接口（前端可以调用的网址）
# ============================================================

@router.post('/sql/query', summary='Agent SQL查询', dependencies=[Depends(require_role(['admin', 'teacher']))])
def agent_sql_query(
    req: SQLQueryRequest,
    db: Session = Depends(get_db),
) -> ApiResponse[SQLQueryResponse]:
    """
    Agent 执行 SQL 查询接口。

    访问地址（例子）：POST http://localhost:8000/agent/sql/query
    需要权限：admin（管理员）或 teacher（老师）

    功能：
        接收一条 SELECT 查询语句，执行后返回查询结果。
        系统会自动检查，只允许 SELECT，不允许其他操作。

    参数：
        req: 前端传来的查询请求，包含 sql 语句和可选的参数
        db: 数据库连接，由 get_db() 自动提供，不用前端传

    返回值：
        统一格式的响应，data 里包含列名、行数据和总行数
    """
    # 第一步：安全检查，确保 SQL 只是查询
    _validate_select_only(req.sql)

    try:
        # 第二步：执行 SQL 语句
        # text() 把字符串变成安全的 SQL 对象，防止 SQL 注入攻击
        # req.params or {} 表示如果没有参数，就用空字典
        result = db.execute(text(req.sql), req.params or {})

        # 第三步：获取列名（表头）
        columns = list(result.keys())

        # 第四步：获取所有行数据
        rows = result.fetchall()

        # 第五步：转换成字典列表
        data = _rows_to_dicts(rows, columns)

        # 第六步：包装成统一格式返回
        return ApiResponse(
            message='查询成功',
            data=SQLQueryResponse(columns=columns, rows=data, row_count=len(data)),
        )

    except Exception as e:
        # 如果执行过程中出错了，返回 400 错误，告诉前端哪里错了
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'SQL执行错误: {str(e)}',
        )


@router.post('/save', summary='Agent保存数据到xlsx或数据库', dependencies=[Depends(require_role(['admin', 'teacher']))])
def agent_save(
    req: SaveRequest,
    db: Session = Depends(get_db),
) -> ApiResponse[dict[str, Any]]:
    """
    Agent 保存数据接口。

    访问地址（例子）：POST http://localhost:8000/agent/save
    需要权限：admin（管理员）或 teacher（老师）

    功能：
        可以把数据保存到两个地方：
        1. xlsx 文件 —— 生成 Excel 表格文件
        2. 数据库表 —— 把数据写入数据库的一张新表或已有表

        数据的来源也可以是两种：
        1. sql —— 先执行一条查询，把查询结果保存
        2. data —— 直接传数据来保存

    参数：
        req: 前端传来的保存请求，包含来源类型、目标类型、具体数据等
        db: 数据库连接，由 get_db() 自动提供

    返回值：
        统一格式的响应，data 里包含保存的文件路径或表名，以及保存了多少行
    """
    # df 是 pandas 的 DataFrame，可以理解为一张"内存中的表格"
    df: pd.DataFrame | None = None

    # ========== 第一步：根据来源类型，获取要保存的数据 ==========

    if req.source_type == 'sql':
        # 来源是 SQL 查询
        if not req.sql:
            raise HTTPException(status_code=400, detail='source_type为sql时必须提供sql字段')

        # 同样要先检查安全性
        _validate_select_only(req.sql)

        try:
            # 用 pandas 直接执行 SQL 并把结果变成 DataFrame
            # db.bind 是数据库连接引擎
            df = pd.read_sql(req.sql, db.bind, params=req.params)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f'SQL查询失败: {str(e)}')

    elif req.source_type == 'data':
        # 来源是直接传入的数据
        if not req.data:
            raise HTTPException(status_code=400, detail='source_type为data时必须提供data字段')
        # 直接把列表数据转成 DataFrame
        df = pd.DataFrame(req.data)

    else:
        # 如果 source_type 既不是 sql 也不是 data，就报错
        raise HTTPException(status_code=400, detail='不支持的source_type')

    # ========== 第二步：检查数据是否为空 ==========

    if df is None or df.empty:
        raise HTTPException(status_code=400, detail='没有可保存的数据')

    # ========== 第三步：根据目标类型，保存到对应的地方 ==========

    if req.target_type == 'xlsx':
        # 目标是 Excel 文件
        if not req.file_path:
            raise HTTPException(status_code=400, detail='target_type为xlsx时必须提供file_path')

        try:
            # to_excel 把 DataFrame 存成 Excel 文件
            # index=False 表示不保存行号
            # engine='openpyxl' 指定用 openpyxl 库来处理 xlsx 格式
            df.to_excel(req.file_path, index=False, engine='openpyxl')

            return ApiResponse(
                message='保存成功',
                data={'file_path': req.file_path, 'row_count': len(df)}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'保存xlsx失败: {str(e)}')

    elif req.target_type == 'db':
        # 目标是数据库表
        if not req.table_name:
            raise HTTPException(status_code=400, detail='target_type为db时必须提供table_name')

        try:
            # to_sql 把 DataFrame 写入数据库
            # if_exists='append' 表示如果表已存在，就追加数据；如果不存在，自动创建表
            # index=False 表示不保存 DataFrame 的行号作为一列
            df.to_sql(req.table_name, db.bind, if_exists='append', index=False)

            return ApiResponse(
                message='保存成功',
                data={'table_name': req.table_name, 'row_count': len(df)}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'写入数据库失败: {str(e)}')

    else:
        # 如果 target_type 既不是 xlsx 也不是 db，就报错
        raise HTTPException(status_code=400, detail='不支持的target_type')
