from db import session
from pprint import pprint
from sqlalchemy import func, desc

from models import Student, Group, Subject, Teacher, Grade

# Знайти 5 студентів з найвищим середнім балом з усіх предметів
def select_1():
    avg_grades = (
        session.query(Grade.student_id, func.avg(Grade.grade).label("average_grade"))
        .group_by(Grade.student_id)
        .subquery()
    )

    five_top_students = (
        session.query(Student.student_name, avg_grades.c.average_grade)
        .join(avg_grades, Student.id == avg_grades.c.student_id)
        .order_by(desc(avg_grades.c.average_grade))
        .limit(5)
        .all()
    )

    return five_top_students

# Знайти студента з найвищим середнім балом з певного предмету
def select_2(subject_id):
    best_student = (
        session.query(
            Student.student_name,
            func.avg(Grade.grade).label("average_grade"),
            Subject.subject_name.label("subject_name"),
        )
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id, Subject.subject_name)
        .order_by(desc(func.avg(Grade.grade)))
        .first()
    )

    if best_student:
        return [
            (
                best_student.student_name,
                float(best_student.average_grade),
                best_student.subject_name,
            )
        ]
    else:
        return []

# Знайти середній бал у групах з певного предмету
def select_3(subject_id):
    group_avrg = (
        session.query(
            Group.group_name.label("group_name"),
            func.avg(Grade.grade).label("average_grade"),
            Subject.subject_name.label("subject_name"),
        )
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id, Subject.subject_name)
        .order_by(Group.group_name)
        .all()
    )

    results = [
        (group_name, float(average_grade), subject_name)
        for group_name, average_grade, subject_name in group_avrg
    ]

    return results

# Знайти середній бал на потоці
def select_4():
    avrg_grade = session.query(func.avg(Grade.grade)).scalar()
    return [float(avrg_grade)]

# Знайти які курси читає певний викладач
def select_5(teacher_id):
    courses = (
        session.query(
            Teacher.teacher_name.label("teacher_name"),
            Subject.subject_name.label("subject_name"),
        )
        .join(Subject, Subject.teacher_id == Teacher.id)
        .filter(Teacher.id == teacher_id)
        .order_by(Subject.subject_name)
        .all()
    )

    return courses

# Знайти список студентів у певній групі
def select_6(group_id):
    students = (
        session.query(
            Group.group_name.label("group_name"),
            Student.student_name.label("student_name"),
        )
        .join(Student, Student.group_id == Group.id)
        .filter(Group.id == group_id)
        .order_by(Student.student_name)
        .all()
    )

    return students

# Знайти оцінки студентів у окремій групі з певного предмета
def select_7(group_id, subject_id):
    student_grades = (
        session.query(
            Group.group_name.label("group_name"),
            Student.student_name.label("student_name"),
            Subject.subject_name.label("subject_name"),
            Grade.grade,
            Grade.date_of.label("date"),
        )
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Group.id == group_id, Subject.id == subject_id)
        .order_by(Student.student_name)
        .all()
    )

    return student_grades

# Знайти середній бал, який ставить певний викладач зі своїх предметів
def select_8(teacher_id):
    avrg_grades = (
        session.query(
            Teacher.teacher_name.label("teacher_name"),
            Subject.subject_name.label("subject_name"),
            func.avg(Grade.grade).label("average_grade"),
        )
        .join(Subject, Subject.teacher_id == Teacher.id)
        .join(Grade, Grade.subject_id == Subject.id)
        .filter(Teacher.id == teacher_id)
        .group_by(Subject.id, Teacher.teacher_name)
        .order_by(Subject.subject_name)
        .all()
    )

    results = [
        (teacher_name, subject_name, float(average_grade))
        for teacher_name, subject_name, average_grade in avrg_grades
    ]

    return results

# Знайти список курсів, які відвідує певний студент
def select_9(student_id):
    courses = (
        session.query(
            Student.student_name.label("student_name"),
            Subject.subject_name.label("subject_name"),
        )
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Student.id == student_id)
        .distinct()
        .order_by(Subject.subject_name)
        .all()
    )

    return courses

# Список курсів, які певному студенту читає певний викладач
def select_10(student_id, teacher_id):
    teacher_courses = (
        session.query(
            Teacher.teacher_name.label("teacher_name"),
            Student.student_name.label("student_name"),
            Subject.subject_name.label("subject_name"),
        )
        .join(Subject, Subject.teacher_id == Teacher.id)
        .join(Grade, Grade.subject_id == Subject.id)
        .join(Student, Student.id == Grade.student_id)
        .filter(Teacher.id == teacher_id, Student.id == student_id)
        .distinct()
        .order_by(Subject.subject_name)
        .all()
    )

    return teacher_courses


def print_with_divider(title, result):
    print(f"{'='*20} {title} {'='*20}")
    pprint(result)
    print("\n")


print_with_divider("1. Result of select_1", select_1())
print_with_divider("2. Results of select_2 (Topic: Chemistry)", select_2(3))
print_with_divider("3. Results of select_3 (Topic: Biology)", select_3(4))
print_with_divider("4. Result of select_4", select_4())
print_with_divider("5. Results of select_5 (Name: 5)", select_5(2))
print_with_divider("6. Results of select_6 (Group: Group-C)", select_6(3))
print_with_divider(
    "7. Results of select_7 (Group: Group-C, Subject: Mathematics)", select_7(3, 1)
)
print_with_divider("8. Results of select_8 (Name: Benjamin Ross)", select_8(7))
print_with_divider("9. Results of select_9 (Name: Barbara Lara)", select_9(4))
print_with_divider(
    "10. Results of select_10 (Comparison: Shannon Howell and Jordan Johnson)",
    select_10(7, 4),
)
