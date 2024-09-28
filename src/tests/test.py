from src.services.AssignmentServices import AssignmentServices
from src.services.GradeServices import GradeServices
from src.services.StudentServices import StudentServices
from src.repository.StudentRepository import StudentRepository
from src.repository.AssignmentRepository import AssignmentRepository
from src.repository.GradeRepository import GradeRepository
from src.services.Undo_Redo_services import UndoService
from unittest import TestCase


class test(TestCase):
    def setUp(self):
        self.UndoRedoService = UndoService()
        self.__student_repository = StudentRepository()
        self.__assignment_repository = AssignmentRepository()
        self.__grade_repository = GradeRepository()
        self.__student_services = StudentServices(self.__student_repository, self.__grade_repository, self.UndoRedoService)
        self.__assignment_services = AssignmentServices(self.__student_repository, self.__assignment_repository, self.__grade_repository, self.UndoRedoService)
        self.__grade_services = GradeServices(self.__grade_repository, self.__student_repository, self.__assignment_repository, self.UndoRedoService)

    def test_add_student_to_list(self):
        self.__student_services.add_student_to_list("1", "Andrei", 914)
        self.assertEqual(len(self.__student_services.get_all_students()), 21)
        self.__student_services.add_student_to_list("2", "Mihai", 914)
        self.assertEqual(len(self.__student_services.get_all_students()), 22)

    def test_remove_student_from_list(self):
        self.__student_services.add_student_to_list("1", "Andrei", 914)
        self.__student_services.add_student_to_list("2", "Mihai", 914)
        self.__student_services.remove_student_from_list("1")
        self.assertEqual(len(self.__student_services.get_all_students()), 21)

    def test_add_assignment(self):
        self.__assignment_services.add_assignment_to_list("1", "description", 2)
        self.assertEqual(len(self.__assignment_services.get_all_assignments()), 21)
        self.__assignment_services.add_assignment_to_list("2", "description", 2)
        self.assertEqual(len(self.__assignment_services.get_all_assignments()), 22)

    def test_remove_assignment(self):
        self.__assignment_services.add_assignment_to_list("1", "description", 2)
        self.__assignment_services.add_assignment_to_list("2", "description", 2)
        self.__assignment_services.remove_assignment_from_list("1")
        self.assertEqual(len(self.__assignment_services.get_all_assignments()), 21)

    def test_undo_redo_operation(self):
        self.__assignment_services.add_assignment_to_list("124", "description", 3)
        self.UndoRedoService.undo()
        self.assertEqual(len(self.__assignment_services.get_all_assignments()), 20)
        self.UndoRedoService.redo()
        self.assertEqual(len(self.__assignment_services.get_all_assignments()), 21)


