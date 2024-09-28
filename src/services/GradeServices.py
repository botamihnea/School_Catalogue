#from src.repository.GradeRepository import GradeRepository
from datetime import date
from src.services.Undo_Redo_services import FunctionCall, Operation, CascadedOperation
import random

class GradeServices():
    def __init__(self, grade_repository, student_repository, assignment_repository, undo_redo_service):
        self.UndoRedoService = undo_redo_service
        self.__grade_repository = grade_repository
        self.__student_repository = student_repository
        self.__assignment_repository = assignment_repository
        self.generate_random_grades()

    def grade_student(self, assignment_id, student_id, grade_value):
        UndoCommand = FunctionCall(self.__grade_repository.remove_grade, *(assignment_id, student_id, grade_value))
        RedoCommand = FunctionCall(self.__grade_repository.add_grade, *(assignment_id, student_id, grade_value))
        UndoRedoOperation = [Operation(UndoCommand, RedoCommand)]
        self.UndoRedoService.record_operation(CascadedOperation(UndoRedoOperation))
        self.__grade_repository.add_grade(assignment_id, student_id, grade_value)

    def get_students_with_assignment(self, assignment_id):
        return self.__grade_repository.get_students_with_assignment(assignment_id)

    def remove_grade_by_assignment_id(self, to_remove_assignment_id):
        self.__grade_repository.remove_grade_by_assignment_id(to_remove_assignment_id)

    def get_all_grades(self):
        return self.__grade_repository.get_all_grades()

    def get_best_school_situation_students(self):
        student_dict = {}

        for grade in self.__grade_repository.get_all_grades():
            if str(grade.get_student_id()) not in student_dict.keys():
                student_dict[str(grade.get_student_id())] = []

            student_dict[str(grade.get_student_id())].append(grade.get_grade_value())

        student_list_with_according_grade = []

        for student_id in student_dict:
            mean = 0
            counter = 0

            for grade in student_dict[student_id]:
                mean += int(grade)
                counter += 1

            mean = mean / counter#here we got the mean
            student_list_with_according_grade.append([student_id, mean])

        return student_list_with_according_grade

    def give_assignment_to_a_student(self, student_id, assignment_id, description, deadline):
        command_list = []
        grade_value = 0
        UndoCommand = FunctionCall(self.__assignment_repository.remove_assignment, (assignment_id))
        RedoCommand = FunctionCall(self.__assignment_repository.add_assignment, *(assignment_id, description, deadline))
        UndoRedoOperation = Operation(UndoCommand, RedoCommand)
        command_list.append(UndoRedoOperation)
        self.__assignment_repository.add_assignment(assignment_id, description, deadline)
        self.__grade_repository.add_grade(assignment_id, student_id, 0)
        grades_list = self.__grade_repository.get_all_grades()
        for any_grade in grades_list:
            if str(any_grade.get_assignment_id()) == str(assignment_id):
                UndoCommand = FunctionCall(self.__grade_repository.remove_grade, *(assignment_id, student_id, grade_value))
                RedoCommand = FunctionCall(self.__grade_repository.add_grade, *(assignment_id, student_id, grade_value))
                UndoRedoOperation = Operation(UndoCommand, RedoCommand)
                command_list.append(UndoRedoOperation)

        self.UndoRedoService.record_operation(CascadedOperation(command_list))



    def add_assignments_to_a_group(self, group, assignment_id, description, deadline):
        command_list = []
        UndoCommand = FunctionCall(self.__assignment_repository.remove_assignment, (assignment_id))
        RedoCommand = FunctionCall(self.__assignment_repository.add_assignment, *(assignment_id, description, deadline))
        UndoRedoOperation = Operation(UndoCommand, RedoCommand)
        command_list.append(UndoRedoOperation)
        student_list = self.__student_repository.get_all_students()
        self.__assignment_repository.add_assignment(assignment_id, description, deadline)

        for student in student_list:
            if str(student.get_group()) == str(group):
                self.__grade_repository.add_grade(assignment_id, student.get_student_id(), 0)

        grades_list = self.__grade_repository.get_all_grades()

        for any_grade in grades_list:
            if str(any_grade.get_assignment_id()) == str(assignment_id):
                UndoCommand = FunctionCall(self.__grade_repository.remove_grade, *(assignment_id, any_grade.get_student_id(), 0))
                RedoCommand = FunctionCall(self.__grade_repository.add_grade, *(assignment_id, any_grade.get_student_id(), 0))
                UndoRedoOperation = Operation(UndoCommand, RedoCommand)
                command_list.append(UndoRedoOperation)

        self.UndoRedoService.record_operation(CascadedOperation(command_list))

    def get_all_students_with_a_given_assignment(self, assignment_id):
        list_of_student_ids_with_given_assignment_and_grade = self.__grade_repository.get_students_with_assignment(assignment_id)
        list_of_students_with_given_assignment = []
        grade = 1
        assignment_id = 1
        studentID = 0

        for student_id in list_of_student_ids_with_given_assignment_and_grade:
            student = self.__student_repository.get_student_with_given_id(student_id[studentID])
            list_of_students_with_given_assignment.append((student, student_id[assignment_id]))

        list_of_students_with_given_assignment = sorted(list_of_students_with_given_assignment, key=lambda studentGrade: studentGrade[grade], reverse=True)

        return list_of_students_with_given_assignment

    def get_students_with_best_school_situation(self):
        student_list_with_grades = self.get_best_school_situation_students()
        grade = 1
        student_list_with_grades = sorted(student_list_with_grades, key=lambda x: x[grade], reverse=True)
        return student_list_with_grades

    def get_late_students(self):
        current_date = str(date.today().day)
        list_of_students = []

        for grade in self.__grade_repository.get_all_grades():
            assignment = self.__assignment_repository.get_assignment_with_given_id(grade.get_assignment_id())
            if int(assignment.get_deadline()) < int(current_date):
                student_to_be_added = self.__student_repository.get_student_with_given_id(grade.get_student_id())
                list_of_students.append(student_to_be_added)

        return list_of_students

    def remove_grades_by_assignment_id(self, to_remove_assignment_id):
        grades = self.__grade_repository.get_all_grades()
        list_of_grades = []

        for grade in grades:
            if str(grade.get_assignment_id()) != str(to_remove_assignment_id):
                list_of_grades.append(grade)

        self.__grade_repository._grades_list = list_of_grades

    def remove_grades_by_student_id(self, student_id):
        list_of_grades = self.__grade_repository.get_all_grades()
        new_list_of_grades = []

        for grade in list_of_grades:
            if str(grade.get_student_id()) != str(student_id):
                new_list_of_grades.append(grade)

        self.__grade_repository._grades_list = new_list_of_grades

    def generate_random_grades(self):
        list_of_students = self.__student_repository.get_all_students()
        list_of_assignments = self.__assignment_repository.get_all_assignments()

        for index in range(20):
            student_id = list_of_students[index].get_student_id()
            assignment_id = list_of_assignments[index].get_assignment_id()
            random_grade = random.randint(1, 10)

            self.__grade_repository.add_grade(assignment_id, student_id, random_grade)

