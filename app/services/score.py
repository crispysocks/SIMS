# ============================================================
# services/score.py —— 成绩业务逻辑
# ============================================================
# 这个文件负责处理"成绩"相关的具体业务操作。
#
# 包含的功能：
#   - 查询所有成绩、查询某个学生的成绩
#   - 录入成绩（检查学生是否存在、检查是否重复录入）
#   - 修改成绩
#   - 删除成绩（逻辑删除）
#   - 考试排名（同分同名次）
#   - 班级成绩报表（平均分、优秀率、及格率）
# ============================================================

from fastapi import HTTPException
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.classes import ClassInfo
from app.models.score import Score
from app.models.student import Student
from app.schemas.score import ScoreCreate, ScoreRead, ScoreUpdate


def list_all_scores(db: Session) -> list[ScoreRead]:
    """
    查询所有未删除的成绩记录。

    按考试序次和学生编号排序，方便查看。
    """
    return [
        ScoreRead.model_validate(item)
        for item in db.query(Score)
        .filter(Score.isdeleted == 0)
        .order_by(Score.exam_no, Score.student_no)
        .all()
    ]


def list_scores_by_student(db: Session, student_no: str) -> list[ScoreRead]:
    """
    查询指定学生的所有未删除成绩。

    按考试序次排序。
    """
    return [
        ScoreRead.model_validate(item)
        for item in db.query(Score)
        .filter(Score.student_no == student_no, Score.isdeleted == 0)
        .order_by(Score.exam_no)
        .all()
    ]


def create_score(db: Session, data: ScoreCreate) -> ScoreRead:
    """
    录入学生成绩。

    校验规则：
        1. 学生必须存在且未删除
        2. 该学生该次考试的成绩不能已存在
    """
    student = db.query(Student).filter(Student.student_no == data.student_no, Student.isdeleted == 0).first()
    if not student:
        raise HTTPException(status_code=404, detail='学生不存在')

    existing = db.query(Score).filter(
        Score.student_no == data.student_no,
        Score.exam_no == data.exam_no,
        Score.isdeleted == 0,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail='该学生该次考核成绩已存在')

    score = Score(**data.model_dump()) # 从请求体中提取数据，创建成绩记录的ORM对象
    db.add(score)
    db.commit()
    db.refresh(score)
    return ScoreRead.model_validate(score)
    


def update_score(db: Session, data: ScoreUpdate) -> ScoreRead:
    """
    修改指定学生某次考试的成绩。
    """
    # 查询数据库中符合条件且未删除的成绩记录
    score = db.query(Score).filter(
        Score.student_no == data.student_no,
        Score.exam_no == data.exam_no,
        Score.isdeleted == 0,
    ).first()
    # 如果未找到对应成绩记录，抛出404异常
    if not score:
        raise HTTPException(status_code=404, detail='成绩记录不存在')
    # 更新成绩分数（必填字段）
    score.score = data.score
    # 如果请求中提供了考试日期，则更新考试日期字段
    if data.exam_date is not None:
        score.exam_date = data.exam_date

    db.commit()
    db.refresh(score)
    #使用 Pydantic 模型验证并转换为响应体格式后返回
    return ScoreRead.model_validate(score)


def delete_score(db: Session, student_no: str, exam_no: int) -> None:
    """
    删除指定学生某次考试的成绩（逻辑删除）。
    """
    # 查询数据库中符合条件且未被逻辑删除的成绩记录
    score = db.query(Score).filter(
        Score.student_no == student_no,
        Score.exam_no == exam_no,
        Score.isdeleted == 0,
    ).first()
    # 如果未找到对应的成绩记录，抛出404异常
    if not score:
        raise HTTPException(status_code=404, detail='成绩记录不存在')

    # 将记录的删除标记字段设置为1，实现逻辑删除
    score.isdeleted = 1
    db.commit()


def get_exam_ranking(db: Session, exam_no: int) -> list[dict]:
    """
    查询某次考试的学生成绩排名。

    排名规则：同分同名次
        比如：两个 100 分都是第 1 名，下一个 99 分是第 3 名

    返回值：
        包含学生信息和排名的字典列表
    """
    # 执行查询，获取本次考试的所有有效成绩记录，并关联学生信息和班级信息
    rows = (
        db.query(
            Student.student_no,
            Student.name.label('student_name'),
            Student.class_no,
            ClassInfo.class_name,
            Score.score,
        )
        .join(Score, Score.student_no == Student.student_no)# 内连接成绩表，关联学生表
        .join(ClassInfo, ClassInfo.class_no == Student.class_no) # 内连接班级表，关联学生表
        .filter(
            Student.isdeleted == 0,
            Score.isdeleted == 0,
            ClassInfo.isdeleted == 0,
            Score.exam_no == exam_no,
        )
        .order_by(Score.score.desc())  # 按分数从高到低排序
        .all()
    )

    result = [] # 初始化结果列表，用于存储包含排名的字典
    current_rank = 0 # 当前排名（实际名次，根据分数变化更新）
    prev_score = None # 上一条记录的分数，用于判断分数是否变化

    # 遍历排序后的结果，计算排名
    for idx, row in enumerate(rows, start=1):
        if row.score != prev_score: # idx 从 1 开始，表示当前是第几条记录
            current_rank = idx # 如果分数和上一个不同，更新当前排名
            prev_score = row.score # 记录当前分数，供下一条记录比较

        # 将一条学生成绩及排名信息添加到结果列表中
        result.append({
            'student_no': row.student_no,
            'student_name': row.student_name,
            'class_no': row.class_no,
            'class_name': row.class_name,
            'score': row.score,
            'rank': current_rank,
        })

    return result


def get_class_score_report(db: Session, exam_no: int) -> list[dict]:
    """
    生成班级成绩报表。

    统计每个班级的：
        - 学生人数
        - 平均分
        - 优秀率（>= 85 分）
        - 及格率（>= 60 分）
        - 优秀人数和及格人数

    返回值：
        按平均分从高到低排序的报表列表
    """
    rows = (
        db.query( # 开始构建查询
            Student.class_no,
            ClassInfo.class_name,
            Score.exam_no,
            func.count(Score.student_no).label('student_count'), # 学生人数（成绩记录数）
            func.avg(Score.score).label('avg_score'),
            # case 语句：分数 >= 85 记为 1，否则记为 0
            func.sum(case((Score.score >= 85, 1), else_=0)).label('excellent_count'), 
            func.sum(case((Score.score >= 60, 1), else_=0)).label('pass_count'), 
        )
        .join(Score, Score.student_no == Student.student_no) # 内连接成绩表
        .join(ClassInfo, ClassInfo.class_no == Student.class_no) # 内连接班级表
        .filter(
            Student.isdeleted == 0,
            Score.isdeleted == 0,
            ClassInfo.isdeleted == 0,
            Score.exam_no == exam_no,
        )
        .group_by(Student.class_no, ClassInfo.class_name, Score.exam_no) # 按班级+考试分组统计
        .order_by(func.avg(Score.score).desc()) # 按平均分从高到低排序
        .all()
    )

    report = []
     # 遍历每个班级的聚合结果，计算衍生指标（优秀率、及格率）
    for row in rows:
        count = row.student_count or 0
        avg_score = float(row.avg_score) if row.avg_score is not None else 0.0
        excellent_count = row.excellent_count or 0
        pass_count = row.pass_count or 0

        report.append({
            'class_no': row.class_no,
            'class_name': row.class_name,
            'exam_no': row.exam_no,
            'student_count': count,
            'avg_score': round(avg_score, 2),
            'excellent_rate': round(excellent_count / count, 4) if count else 0.0,
            'pass_rate': round(pass_count / count, 4) if count else 0.0,
            'excellent_count': excellent_count,
            'pass_count': pass_count,
        })

    return report
