import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.student import Student
from app.models.user import SysUser
from app.schemas.student import (
    StudentCreate,
    StudentListResponse,
    StudentResponse,
    StudentUpdate,
)
from app.utils.excel import export_dicts_to_excel, read_excel_to_dicts
from app.utils.file import save_upload_file

router = APIRouter(prefix="/api/students", tags=["学生管理"])


@router.get("/", response_model=StudentListResponse)
def get_students(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str = Query(None),
    current_user: SysUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Student)

    if keyword:
        query = query.filter(
            (Student.name.contains(keyword)) | (Student.student_no.contains(keyword))
        )

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "items": [StudentResponse.model_validate(s) for s in items],
        "page": page,
        "page_size": page_size,
    }


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    current_user: SysUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentResponse.model_validate(student)


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    data: StudentCreate,
    current_user: SysUser = Depends(require_role(["admin", "teacher"])),
    db: Session = Depends(get_db),
):
    existing = db.query(Student).filter(Student.student_no == data.student_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student number already exists")

    student = Student(**data.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return StudentResponse.model_validate(student)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    data: StudentUpdate,
    current_user: SysUser = Depends(require_role(["admin", "teacher"])),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return StudentResponse.model_validate(student)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    current_user: SysUser = Depends(require_role(["admin"])),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return None


@router.post("/upload")
async def upload_avatar(
    student_id: int,
    file: UploadFile = File(...),
    current_user: SysUser = Depends(require_role(["admin", "teacher"])),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    filename = await save_upload_file(file)
    student.avatar = filename
    db.commit()

    return {"avatar": filename}


@router.post("/import")
def import_students(
    file: UploadFile = File(...),
    current_user: SysUser = Depends(require_role(["admin"])),
    db: Session = Depends(get_db),
):
    ext = file.filename.split(".")[-1]
    if ext not in ["xlsx", "xls"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    temp_filename = f"{uuid.uuid4()}.{ext}"
    temp_path = os.path.join("./backend/uploads", temp_filename)
    os.makedirs("./backend/uploads", exist_ok=True)

    with open(temp_path, "wb") as f:
        f.write(file.file.read())

    try:
        records = read_excel_to_dicts(temp_path)

        imported = 0
        errors = []
        for i, record in enumerate(records):
            try:
                existing = (
                    db.query(Student).filter(Student.student_no == record.get("student_no")).first()
                )
                if existing:
                    for key, value in record.items():
                        if value is not None and hasattr(existing, key):
                            setattr(existing, key, value)
                else:
                    student = Student(**{k: v for k, v in record.items() if v is not None})
                    db.add(student)
                imported += 1
            except Exception as e:
                errors.append(f"Row {i + 2}: {str(e)}")

        db.commit()
        return {"imported": imported, "errors": errors}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@router.get("/export")
def export_students(
    current_user: SysUser = Depends(get_current_user), db: Session = Depends(get_db)
):
    students = db.query(Student).all()

    data = []
    for s in students:
        data.append(
            {
                "student_no": s.student_no,
                "name": s.name,
                "gender": "男" if s.gender == 0 else "女",
                "age": s.age,
                "grade": s.grade,
                "class_name": s.class_name,
                "phone": s.phone,
                "address": s.address,
                "email": s.email,
                "status": ["在读", "休学", "毕业"][s.status] if s.status else "在读",
            }
        )

    filename = f"students_{uuid.uuid4()}.xlsx"
    filepath = os.path.join("./backend/uploads", filename)
    os.makedirs("./backend/uploads", exist_ok=True)

    export_dicts_to_excel(data, filepath)

    return FileResponse(
        filepath,
        filename="students.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
