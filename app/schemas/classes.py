# ============================================================
# schemas/classes.py —— 班级数据校验模型（Schema）
# ============================================================
# 这个文件定义了"班级"相关的数据校验规则。
#
# 什么是 Schema？
#   Schema 是 Pydantic 提供的工具，用来检查数据是否符合预期。
#   比如：班级名称不能为空、长度不能超过 50 个字符。
#
# 为什么需要 Schema？
#   前端传来的数据可能有问题（比如少了字段、格式不对），
#   用 Schema 可以在进入业务逻辑之前就把这些问题拦下来，
#   避免脏数据进入数据库。
#
# 常见的 Schema 类型：
#   - Create: 新增时用的校验规则
#   - Update: 更新时用的校验规则
#   - Read: 返回给前端时的数据格式
# ============================================================

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.teacher import TeacherRead


class ClassBase(BaseModel):
    """
    班级基础信息模型。

    这个类定义了班级共有的字段，Create 和 Read 都继承它。
    """

    # Field(...) 表示这个字段是必填的
    # min_length=1 表示不能为空字符串
    # max_length=20 表示最多 20 个字符
    class_no: str = Field(..., min_length=1, max_length=20, description='班级编号')

    class_name: str = Field(..., min_length=1, max_length=50, description='班级名称')

    # date 类型会自动校验格式是否为合法日期
    class_open_time: date = Field(..., description='开课时间')

    # str | None 表示这个字段可以是字符串，也可以是空
    head_teacher_no: str | None = Field(None, max_length=20, description='班主任编号')
    instructor_no: str | None = Field(None, max_length=20, description='授课老师编号')
    description: str | None = Field(None, max_length=500, description='班级描述')


class ClassCreate(ClassBase):
    """
    新增班级时的请求模型。

    直接继承 ClassBase，因为新增时需要所有字段。
    """
    pass


class ClassUpdate(BaseModel):
    """
    更新班级时的请求模型。

    和 ClassCreate 的区别：
        - 所有字段都是可选的（没有 ... 标记）
        - 这样前端可以只传要修改的字段，不用传全部
    """

    class_name: str | None = Field(None, min_length=1, max_length=50)
    class_open_time: date | None = None
    head_teacher_no: str | None = Field(None, max_length=20)
    instructor_no: str | None = Field(None, max_length=20)
    description: str | None = Field(None, max_length=500)


class ClassRead(ClassBase):
    """
    查询班级时的响应模型。

    model_config = ConfigDict(from_attributes=True) 的作用：
        告诉 Pydantic："可以从 SQLAlchemy 模型对象直接读取属性"
        这样我们就能直接把数据库查出来的对象转成一个 ClassRead 对象。
    """

    model_config = ConfigDict(from_attributes=True)

    # 响应时额外返回逻辑删除标记
    isdeleted: int


class ClassReadDetail(ClassRead):
    """
    班级详情响应模型（包含教师信息）。

    在 ClassRead 的基础上，额外返回班主任和授课老师的详细信息。
    """

    headteacher: TeacherRead | None = None
    instructor: TeacherRead | None = None
