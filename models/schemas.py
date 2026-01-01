from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    username: string
    password_hash: str
    role: str # 'Admin', 'Enseignant', 'Étudiant'
    email: str
    created_at: str

@dataclass
class Student:
    id: int
    first_name: str
    last_name: str
    birth_date: str
    class_name: str

@dataclass
class Teacher:
    id: int
    first_name: str
    last_name: str
    specialty: str

@dataclass
class Subject:
    id: int
    name: str
    teacher_id: int
    class_name: str

@dataclass
class Grade:
    id: int
    student_id: int
    subject_id: int
    grade: float
    date: str