class TeacherNotFoundException(Exception):
    """老师不存在异常"""
    pass

class CourseNotFoundException(Exception):
    """课程不存在异常"""
    pass

class DatabaseOperationException(Exception):
    """数据库操作异常"""
    pass

class InvalidDataException(Exception):
    """无效数据异常"""
    pass