# 测试指南

## 工具栈

- **pytest** — 测试运行器
- **pytest fixture** — 依赖注入，共享测试资源
- **SQLAlchemy** — 数据库查询

## 目录结构

```
tests/
├── __init__.py
├── conftest.py       # fixture 定义
└── test_database.py # 数据库测试
```

## 运行

```bash
# 运行所有测试
uv run pytest tests/ -v

# 运行指定文件
uv run pytest tests/test_database.py -v

# 运行指定测试
uv run pytest tests/test_database.py::TestDatabaseConnection::test_mysql_version -v
```

## conftest.py 结构

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
```

`sys.path.insert` 解决模块导入问题，路径指向项目根目录。

### Fixture 说明

| Fixture | scope | 说明 |
|---------|-------|------|
| `engine` | `session` | SQLAlchemy 引擎，整个测试会话共享 |
| `engine_url` | `session` | 数据库 URL |
| `db_session` | `function` | 数据库会话，每个测试函数独立，用完自动关闭 |

`sesssion` scope 的 fixture 在测试会话开始时创建一次，所有测试共享，适合数据库连接池。  
`function` scope 的 fixture 每个测试函数独立创建，适合需要独立数据状态的场景。

## 写测试

```python
import pytest
from sqlalchemy import text

class TestDatabaseConnection:
    def test_mysql_version(self, engine):
        """测试 MySQL 版本"""
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            assert version.startswith("8.0"), f"Expected MySQL 8.x, got {version}"

    def test_database_exists(self, engine):
        """测试数据库存在"""
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DATABASE()"))
            db_name = result.fetchone()[0]
            assert db_name == "student_management"

    def test_session_query(self, db_session):
        """测试会话查询"""
        result = db_session.execute(text("SELECT DATABASE()"))
        db_name = result.fetchone()[0]
        assert db_name == "student_management"
```

- 测试类用 `Test` 开头
- 测试方法用 `test_` 开头
- Fixture 通过参数自动注入（pytest 读取函数签名）
- 使用原生 SQL 的场景，用 `text()` 包裹 SQL 字符串（防止 SQLAlchemy 转译）

## 扩展

### 新建测试文件

在 `tests/` 下新建 `test_xxx.py`，conftest.py 中的 fixture 自动生效，无需 import。

```python
# tests/test_student.py
import pytest
from sqlalchemy import text

class TestStudent:
    def test_student_table_exists(self, engine):
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES LIKE 'student'"))
            assert result.fetchone() is not None
```

### 添加新 Fixture

在 `conftest.py` 中定义，其他测试文件直接使用：

```python
@pytest.fixture(scope="function")
def mock_data(db_session):
    """在 db_session 上添加测试数据"""
    db_session.execute(text("INSERT INTO student (name) VALUES ('test')"))
    db_session.commit()
    yield "test"
    # teardown: 清理测试数据
    db_session.execute(text("DELETE FROM student WHERE name = 'test'"))
    db_session.commit()
```