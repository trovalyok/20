# pip install sqlalchemy==1.4.52
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return '[Student: %s, %s, %s]' % (self.id, self.name, self.age)


class Subject(Base):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True)
    subject_name = Column(String)

    def __repr__(self):
        return '[Subject: %s, %s]' % (self.id, self.subject_name)


class Student_subject(Base):
    __tablename__ = 'student_subject'

    student_subject_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))

    def __str__(self):
        return f'{self.student_subject_id}. Student #{self.student_id} is\
 registered for subject #{self.subject_id}'


DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{database}'

engine = create_engine(
    DATABASE_URI.format(
        host='localhost',
        database='postgres',
        user='user',
        password='password',
        port=5432,
    )
)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

students_data = [
    {"id": 1, "name": "Bae", "age": 18},
    {"id": 2, "name": "Eddy", "age": 21},
    {"id": 3, "name": "Lily", "age": 22},
    {"id": 4, "name": "Jenny", "age": 19}
]

subjects_data = [
    {"id": 1, "subject_name": "English"},
    {"id": 2, "subject_name": "Spanish"},
    {"id": 3, "subject_name": "Chinese"},
    {"id": 4, "subject_name": "Math"}
]

student_subject_data = [
    {"student_id": 1, "subject_id": 1, "student_subject_id": 1},
    {"student_id": 1, "subject_id": 2, "student_subject_id": 2},
    {"student_id": 2, "subject_id": 3, "student_subject_id": 3},
    {"student_id": 3, "subject_id": 1, "student_subject_id": 4},
    {"student_id": 4, "subject_id": 4, "student_subject_id": 5}
]

for data in students_data:
    student = Student(**data)
    session.add(student)

for data in subjects_data:
    subject = Subject(**data)
    session.add(subject)

for data in student_subject_data:
    student_subject = Student_subject(**data)
    session.add(student_subject)

session.commit()

english_students = session.query(Student)\
    .join(Student_subject, Student.id == Student_subject.student_id)\
    .join(Subject, Student_subject.subject_id == Subject.id)\
    .filter(Subject.subject_name == 'English')\
    .all()

english_students_names = [student.name for student in english_students]
print("Students who visited 'English' classes:", english_students_names)

session.close()
