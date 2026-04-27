from typing import Any, Literal

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import require_role
from app.schemas.response import ApiResponse

router = APIRouter(prefix='/agent', tags=['Agent接口'])


class SQLQueryRequest(BaseModel):
    sql: str = Field(..., description='要执行的SQL查询语句（仅支持SELECT）')
    params: dict[str, Any] | None = Field(default=None, description='SQL参数')


class SQLQueryResponse(BaseModel):
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int


class SaveRequest(BaseModel):
    source_type: Literal['sql', 'data'] = Field(..., description='数据来源类型：sql 或 data')
    sql: str | None = Field(default=None, description='当 source_type=sql 时，要执行的SELECT语句')
    params: dict[str, Any] | None = Field(default=None, description='SQL参数')
    data: list[dict[str, Any]] | None = Field(default=None, description='当 source_type=data 时，要保存的数据')
    target_type: Literal['xlsx', 'db'] = Field(..., description='保存目标：xlsx 或 db')
    table_name: str | None = Field(default=None, description='当 target_type=db 时，要写入的数据库表名')
    file_path: str | None = Field(default=None, description='当 target_type=xlsx 时，xlsx文件保存路径（相对或绝对）')


def _validate_select_only(sql: str) -> None:
    """验证SQL语句仅为SELECT查询。"""
    stripped = sql.strip().lower()
    if not stripped.startswith('select'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='仅允许执行SELECT查询语句',
        )
    forbidden = ['insert', 'update', 'delete', 'drop', 'truncate', 'alter', 'create', 'grant', 'revoke']
    for keyword in forbidden:
        if keyword in stripped:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'SQL中包含禁止的关键字: {keyword}',
            )


def _rows_to_dicts(rows: Any, columns: list[str]) -> list[dict[str, Any]]:
    """将SQLAlchemy行结果转换为字典列表。"""
    result: list[dict[str, Any]] = []
    for row in rows:
        if hasattr(row, '_mapping'):
            result.append(dict(row._mapping))
        else:
            result.append(dict(zip(columns, row)))
    return result


@router.post('/sql/query', summary='Agent SQL查询', dependencies=[Depends(require_role(['admin', 'teacher']))])
def agent_sql_query(
    req: SQLQueryRequest,
    db: Session = Depends(get_db),
) -> ApiResponse[SQLQueryResponse]:
    """Agent通过SQL直接查询数据库（仅SELECT）。"""
    _validate_select_only(req.sql)
    try:
        result = db.execute(text(req.sql), req.params or {})
        columns = list(result.keys())
        rows = result.fetchall()
        data = _rows_to_dicts(rows, columns)
        return ApiResponse(
            message='查询成功',
            data=SQLQueryResponse(columns=columns, rows=data, row_count=len(data)),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'SQL执行错误: {str(e)}',
        )


@router.post('/save', summary='Agent保存数据到xlsx或数据库', dependencies=[Depends(require_role(['admin', 'teacher']))])
def agent_save(
    req: SaveRequest,
    db: Session = Depends(get_db),
) -> ApiResponse[dict[str, Any]]:
    """Agent将查询结果或原始数据保存到xlsx文件或数据库表中。"""
    df: pd.DataFrame | None = None

    if req.source_type == 'sql':
        if not req.sql:
            raise HTTPException(status_code=400, detail='source_type为sql时必须提供sql字段')
        _validate_select_only(req.sql)
        try:
            df = pd.read_sql(req.sql, db.bind, params=req.params)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f'SQL查询失败: {str(e)}')
    elif req.source_type == 'data':
        if not req.data:
            raise HTTPException(status_code=400, detail='source_type为data时必须提供data字段')
        df = pd.DataFrame(req.data)
    else:
        raise HTTPException(status_code=400, detail='不支持的source_type')

    if df is None or df.empty:
        raise HTTPException(status_code=400, detail='没有可保存的数据')

    if req.target_type == 'xlsx':
        if not req.file_path:
            raise HTTPException(status_code=400, detail='target_type为xlsx时必须提供file_path')
        try:
            df.to_excel(req.file_path, index=False, engine='openpyxl')
            return ApiResponse(message='保存成功', data={'file_path': req.file_path, 'row_count': len(df)})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'保存xlsx失败: {str(e)}')

    elif req.target_type == 'db':
        if not req.table_name:
            raise HTTPException(status_code=400, detail='target_type为db时必须提供table_name')
        try:
            df.to_sql(req.table_name, db.bind, if_exists='append', index=False)
            return ApiResponse(message='保存成功', data={'table_name': req.table_name, 'row_count': len(df)})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'写入数据库失败: {str(e)}')
    else:
        raise HTTPException(status_code=400, detail='不支持的target_type')
