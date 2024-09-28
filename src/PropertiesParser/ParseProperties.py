from src.repository.AssignmentRepository import *
from src.repository.StudentRepository import *
from src.repository.GradeRepository import *
from jproperties import Properties

def find_grade_repository():
    configurations = Properties()

    with open("settings.properties", "rb") as configuration_file:
        configurations.load(configuration_file)
        repository = configurations.get("REPOSITORY").data
        location = configurations.get("GRADE").data
        if repository == "in_memory":
            return GradeRepository()
        elif repository == "text_file":
            return TextFileGradeRepository(location)
        elif repository == "pickle_file":
            return GradeRepositoryBinaryFile(location)

def find_student_repository():
    configurations = Properties()

    with open("settings.properties", "rb") as configuration_file:
        configurations.load(configuration_file)
        repository = configurations.get("REPOSITORY").data
        location = configurations.get("STUDENT").data
        if repository == "in_memory":
            return StudentRepository()
        elif repository == "text_file":
            return TextFileStudentRepository(location)
        elif repository == "pickle_file":
            return StudentRepositoryBinaryFile(location)

def find_assignment_repository():
    configurations = Properties()

    with open("settings.properties", "rb") as configuration_file:
        configurations.load(configuration_file)
        repository = configurations.get("REPOSITORY").data
        location = configurations.get("ASSIGNMENT").data
        if repository == "in_memory":
            return AssignmentRepository()
        elif repository == "text_file":
            return TextFileAssignmentRepository(location)
        elif repository == "pickle_file":
            return AssignmentRepositoryBinaryFile(location)