#from src.repository.StudentRepository import StudentRepository
import random
from src.services.Undo_Redo_services import Operation, CascadedOperation, FunctionCall

class StudentServices:
    def __init__(self, student_repository, grade_repository, undo_redo_service):
        self.UndoRedoService = undo_redo_service
        self.__student_repository = student_repository
        self.__grade_repository = grade_repository
        self.generate_20_random_students()

    def generate_20_random_students(self):
        names = ["Ana", "Bogdan", "Carmen", "Dorin", "Elena", "Florin", "Gabriela", "Horia", "Iulia", "Jovan",
                          "Larisa", "Marius", "Nicoleta", "Octavian", "Paula", "Radu", "Simona", "Teodor", "Ursula",
                          "Vlad"]
        groups = ["911", "912", "913", "914"]
        counter = random.randint(1, 100)
        for i in range (20):
            student_id = (counter + random.randint(1, 50))
            counter = student_id
            student_name = random.choice(names)
            student_group = random.choice(groups)
            self.__student_repository.add_student(student_id, student_name, student_group)

    def add_student_to_list(self, student_id, student_name, student_group):
        Undo_Command = FunctionCall(self.__student_repository.remove_student, (student_id))
        Redo_Command = FunctionCall(self.__student_repository.add_student, *(student_id, student_name, student_group))
        Undo_Redo_Operation = [Operation(Undo_Command, Redo_Command)]
        self.UndoRedoService.record_operation(CascadedOperation(Undo_Redo_Operation))
        return self.__student_repository.add_student(student_id, student_name, student_group)

    def remove_student_from_list(self, to_remove_id):
        command_list = []
        Undo_Command = FunctionCall(self.__student_repository.add_student, *(to_remove_id, self.__student_repository.get_student_name_(to_remove_id),
                                                                                self.__student_repository.get_student_group(to_remove_id)))
        Redo_Command = FunctionCall(self.__student_repository.remove_student, (to_remove_id))
        Undo_Redo_Operation = Operation(Undo_Command, Redo_Command)

        command_list.append(Undo_Redo_Operation)

        self.__student_repository.remove_student(to_remove_id)
        grades_list = self.__grade_repository.get_all_grades()
        for grade in grades_list:
            if(str(grade.get_student_id()) == to_remove_id):
                Undo_Command = FunctionCall(self.__grade_repository.add_grade, *(grade.get_assignment_id(), grade.get_student_id, grade.get_grade_value()))
                Redo_Command = FunctionCall(self.__grade_repository.remove_grade, *(grade.get_assignment_id(), grade.get_student_id(), grade.get_grade_value()))
                OperationForRedoUndo = Operation(Undo_Command, Redo_Command)
                command_list.append(OperationForRedoUndo)
                self.__grade_repository.remove_grade(grade.get_assignment_id, grade.get_student_id, grade.get_grade_value)

        self.UndoRedoService.record_operation(CascadedOperation(command_list))


    def update_student_in_list(self, to_update_id, new_name, group):
        Redo_Command = FunctionCall(self.__student_repository.update_student, *(to_update_id, new_name, group))
        Undo_Command = FunctionCall(self.__student_repository.update_student, *(to_update_id, self.__student_repository.get_student_name_(to_update_id),
                                                                                self.__student_repository.get_student_group(to_update_id)))
        Undo_Redo_Operation = [Operation(Undo_Command, Redo_Command)]
        self.UndoRedoService.record_operation(CascadedOperation(Undo_Redo_Operation))
        return self.__student_repository.update_student(to_update_id, new_name, group)

    def get_all_students(self):
        return self.__student_repository.get_all_students()

    def get_student_by_group(self, student_id):
        return self.__student_repository.get_student_group(student_id)


