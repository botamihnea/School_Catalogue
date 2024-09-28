#from src.repository.AssignmentRepository import AssignmentRepository
import random
from src.services.Undo_Redo_services import Operation, FunctionCall, CascadedOperation
#from copy import deepcopy


class AssignmentServices:
    def __init__(self, student_repository, assignment_repository, grade_repository, undo_redo_service):
        self.UndoRedoService = undo_redo_service
        self.__assignment_repository = assignment_repository
        self.__grade_repository = grade_repository
        self.__student_repository = student_repository
        self.generate_20_random_assignments()

    def generate_20_random_assignments(self):
        assignment_descriptions = ["Compute the area of a geometric shape.","Generate a unique username.","Find the maximum value in a list.",
    "Reverse the order of characters in a string.","Check if an email address is valid.","Count the number of vowels in a string.",
    "Determine if a number is prime.","Combine two lists into a single list.","Calculate the GPA from a list of grades.",
    "Capitalize the first letter of each word in a string.","Check if a word or phrase is a palindrome.","Filter out odd numbers from a list.",
    "Find the factorial of a given number.","Remove duplicate elements from a list.","Encrypt a message.","Generate a secure password.",
    "Convert temperature between different scales.","Calculate the discount on a product.","Check if two words are anagrams.","Create a histogram from a list of values."]

        deadlines = ["3", "7", "8", "12", "13", "14", "15",
                     "16", "17", "18", "19",
                     "20", "21", "22", "23",
                     "24", "25", "26", "27",
                     "28"]

        counter = random.randint(1, 50)
        for i in range (20):
            assignment_id = (counter + random.randint(1, 100))
            counter = assignment_id
            assignment_description = random.choice(assignment_descriptions)
            assignment_deadline = random.choice(deadlines)
            self.__assignment_repository.add_assignment(str(assignment_id), assignment_description, assignment_deadline)
            students = self.__student_repository.get_all_students()
            student = random.choice(students)

    def add_assignment_to_list(self, assignment_id, description, deadline):
        Undo_Command = FunctionCall(self.__assignment_repository.remove_assignment, (assignment_id))
        Redo_Command = FunctionCall(self.__assignment_repository.add_assignment, *(assignment_id, description, deadline))
        Undo_Redo_Operation = [Operation(Undo_Command, Redo_Command)]
        self.UndoRedoService.record_operation(CascadedOperation(Undo_Redo_Operation))
        return self.__assignment_repository.add_assignment(assignment_id, description, deadline)

    def remove_assignment_from_list(self, id_to_remove):
        command_list = []
        Undo_Command = FunctionCall(self.__assignment_repository.add_assignment, *(id_to_remove, self.__assignment_repository.get_assignment_with_given_id_description(id_to_remove),
                                                                   self.__assignment_repository.get_assignment_with_given_id_deadline(id_to_remove)))
        Redo_Command = FunctionCall(self.__assignment_repository.remove_assignment, (id_to_remove))
        Undo_Redo_Command = Operation(Undo_Command, Redo_Command)
        command_list.append(Undo_Redo_Command)
        self.__assignment_repository.remove_assignment(id_to_remove)
        grades_list = self.__grade_repository.get_all_grades()
        for grade in grades_list:
            if str(grade.get_assignment_id()) == str(id_to_remove):
                Undo_Command = FunctionCall(self.__grade_repository.add_grade, *(grade.get_assignment_id(), grade.get_student_id(), grade.get_grade_value()))
                Redo_Command = FunctionCall(self.__grade_repository.remove_grade, *(grade.get_assignment_id(), grade.get_student_id(), grade.get_grade_value()))
                Undo_Redo_Command = Operation(Undo_Command, Redo_Command)
                command_list.append(Undo_Redo_Command)
                self.__grade_repository.remove_grade(grade.get_assignment_id(), grade.get_student_id(), grade.get_grade_value())

        self.UndoRedoService.record_operation(CascadedOperation(command_list))


    def update_assignment_in_list(self, to_update_id, new_description, deadline):
        Redo_Command = FunctionCall(self.__assignment_repository.update_assignment, *(to_update_id, new_description, deadline))
        Undo_Command = FunctionCall(self.__assignment_repository.update_assignment, *(to_update_id, self.__assignment_repository.get_assignment_with_given_id_description(to_update_id),
                                                                      self.__assignment_repository.get_assignment_with_given_id_deadline(to_update_id)))
        Undo_Redo_Operation = [Operation(Undo_Command, Redo_Command)]
        self.UndoRedoService.record_operation(CascadedOperation(Undo_Redo_Operation))
        return self.__assignment_repository.update_assignment(to_update_id, new_description, deadline)

    def get_all_assignments(self):
        return self.__assignment_repository.get_all_assignments()

