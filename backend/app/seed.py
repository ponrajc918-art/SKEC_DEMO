"""Synthetic development data. It is never created by a production environment."""
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from .core import hash_password
from .models import (Assignment, Circular, Department, Invoice, Notification, PasswordHistory, Permission, Result, Role,
    RolePermission, Staff, Student, SubjectOffering, TimetableEntry, User, UserRole)
from .permissions import PERMISSION_DESCRIPTIONS, ROLE_NAMES, ROLE_PERMISSIONS

ROLES=list(ROLE_NAMES)
DEMO_PASSWORD="DemoPass!2026"

def seed(db:Session):
    if db.query(User).first(): return
    cse=Department(code="CSE",name="Computer Science and Engineering")
    ece=Department(code="ECE",name="Electronics and Communication Engineering")
    db.add_all([cse,ece]); db.flush()
    roles={code:Role(code=code,name=code.replace("_"," ").title()) for code in ROLES}
    db.add_all(roles.values()); db.flush()
    permissions={code:Permission(code=code,description=description) for code,description in PERMISSION_DESCRIPTIONS.items()}
    db.add_all(permissions.values()); db.flush()
    db.add_all(RolePermission(role_id=roles[role].id,permission_id=permissions[permission].id) for role,codes in ROLE_PERMISSIONS.items() for permission in codes)
    def user(email:str,role:str):
        account=User(email=email,password_hash=hash_password(DEMO_PASSWORD),must_change_password=True)
        db.add(account); db.flush(); db.add(UserRole(user_id=account.id,role_id=roles[role].id)); return account
    students=[]
    for index,name in enumerate(["Aarav Kumar","Diya Nair","Kabir Shah","Meera Iyer"],1):
        email="student.demo@skec.example" if index==1 else f"student{index}.demo@skec.example"
        account=user(email,"student")
        students.append(Student(user_id=account.id,register_number=f"DEMO-CSE-00{index}",full_name=name,department_id=cse.id,programme="B.E. Computer Science and Engineering"))
    db.add_all(students)
    staff_account=user("faculty.demo@skec.example","staff")
    hod_account=user("hod.demo@skec.example","hod")
    principal_account=user("principal.demo@skec.example","principal")
    admin_account=user("admin.demo@skec.example","college_admin")
    faculty=Staff(user_id=staff_account.id,employee_id="DEMO-FAC-001",full_name="Dr. Ananya Rao",department_id=cse.id,designation="Assistant Professor")
    hod=Staff(user_id=hod_account.id,employee_id="DEMO-HOD-001",full_name="Dr. Vivek Menon",department_id=cse.id,designation="Head of Department")
    principal=Staff(user_id=principal_account.id,employee_id="DEMO-PRI-001",full_name="Dr. Kavita Sharma",department_id=ece.id,designation="Principal")
    db.add_all([faculty,hod,principal]); db.flush()
    for account in db.query(User).all(): db.add(PasswordHistory(user_id=account.id,password_hash=account.password_hash))
    offerings=[
      SubjectOffering(department_id=cse.id,staff_id=faculty.id,code="CSE301",title="Data Structures"),
      SubjectOffering(department_id=cse.id,staff_id=faculty.id,code="CSE302",title="Database Systems"),
    ]
    db.add_all(offerings); db.flush()
    for offering,day,period,room in [(offerings[0],"Monday",1,"Lab 204"),(offerings[1],"Tuesday",3,"Block A-12"),(offerings[0],"Thursday",2,"Lab 204")]:
        db.add(TimetableEntry(offering_id=offering.id,day_of_week=day,period=period,room=room,starts_at="09:00",ends_at="09:50"))
    db.add_all([
      Assignment(offering_id=offerings[0].id,title="Linked-list implementation",instructions="Implement and explain a singly linked-list operation set. Development demo task.",due_at=datetime.now(timezone.utc)+timedelta(days=6),max_marks=20,created_by=faculty.id),
      Assignment(offering_id=offerings[1].id,title="Normalisation worksheet",instructions="Identify normal forms for the supplied synthetic schema.",due_at=datetime.now(timezone.utc)+timedelta(days=10),max_marks=15,created_by=faculty.id),
    ])
    db.add_all([
      Result(student_id=students[0].id,subject_code="CSE301",exam_name="Internal assessment",marks=82,grade="A",status="published"),
      Result(student_id=students[0].id,subject_code="CSE302",exam_name="Internal assessment",marks=76,grade="A",status="published"),
      Invoice(student_id=students[0].id,number="DEMO-INV-001",total_paise=100000,status="open"),
      Circular(title="Demo orientation circular",body="Synthetic development announcement for the professional demonstration environment.",audience={"roles":["student","staff"]},status="published",published_by=admin_account.id),
      Notification(user_id=students[0].user_id,title="Assignment due soon",body="Linked-list implementation is due in six days.",kind="assignment"),
      Notification(user_id=faculty.user_id,title="Class roster ready",body="Your demonstration class roster is available.",kind="academic"),
    ])
    db.commit()
