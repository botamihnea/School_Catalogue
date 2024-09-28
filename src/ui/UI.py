from src.services.StudentServices import StudentServices
from src.services.AssignmentServices import AssignmentServices
from src.services.GradeServices import GradeServices
from src.services.Undo_Redo_services import UndoService
from src.PropertiesParser import ParseProperties

class UserInterface:

    def __init__(self):
        self.undo_redo_service = UndoService()
        student_repository = ParseProperties.find_student_repository()
        assignment_repository = ParseProperties.find_assignment_repository()
        grade_repository = ParseProperties.find_grade_repository()
        self.__studentServices = StudentServices(student_repository, grade_repository, self.undo_redo_service)
        self.__assignmentServices = AssignmentServices(student_repository, assignment_repository, grade_repository, self.undo_redo_service)
        self.__gradeServices = GradeServices(grade_repository, student_repository, assignment_repository, self.undo_redo_service)

    def print_elements(self, elements_list):
        print("---------------------------------------------")
        for element in elements_list:
            print(str(element))
            print("---------------------------------------------")

    def Print_Menu(self):
        manage_students = 1
        add_student = 1
        add_assignment = 1
        give_assignment_to_student = 1
        manage_assignments = 2
        remove_student = 2
        remove_assignment = 2
        give_assignment_to_group = 2
        give_assignments = 3
        update_assignment = 3
        update_student = 3
        grade_student = 4
        display_students = 4
        display_assignments = 4
        display_statistics = 5
        undo_last_operation = 6
        redo_last_operation = 7
        print("Choose your desired option:")
        print("1.Manage students:")
        print("2.Manage assignments:")
        print("3.Give assignments:")
        print("4.Grade student:")
        print("5.Display statistics:")
        print("6.Undo last operation:")
        print("7.Redo last operation:")
        chosen_option = int(input("->"))
        if chosen_option == manage_students:
            print("1.Add a student:")
            print("2.Remove a student:")
            print("3.Update a student:")
            print("4.Display all students:")
            chosen_option = int(input("->"))
            if chosen_option == add_student:
                student_id = input("Enter the id:")
                student_name = input("Enter the name of the student:")
                student_group = int(input("Enter the group of the student:"))
                self.__studentServices.add_student_to_list(student_id, student_name, student_group)
            elif chosen_option == remove_student:
                to_remove_id = input("Enter the id of the student you want to remove:")
                self.__studentServices.remove_student_from_list(to_remove_id)
                self.__gradeServices.remove_grades_by_student_id(to_remove_id)
            elif chosen_option == update_student:
                to_update_id = input("Enter the id of the student which you want to update:")
                new_name = input("Enter the new name:")
                group = int(input("Enter the new group:"))
                self.__studentServices.update_student_in_list(to_update_id, new_name, group)
            elif chosen_option == display_students:
                students_list = self.__studentServices.get_all_students()
                self.print_elements(students_list)

        elif chosen_option == manage_assignments:
            print("1.Add an assignment:")
            print("2.Remove an assignment:")
            print("3.Update an assignment:")
            print("4.Display all assignments:")
            chosen_option = int(input("->"))
            if chosen_option == add_assignment:
                assignment_id = input("Enter the id of the assignment:")
                description = input("Enter the description of the assignment:")
                deadline = input("Enter the deadline of the assignment:")
                self.__assignmentServices.add_assignment_to_list(assignment_id, description, deadline)
            elif chosen_option == remove_assignment:
                to_remove_id = input("Enter the id of the assignment you want to remove:")
                self.__assignmentServices.remove_assignment_from_list(to_remove_id)
                self.__gradeServices.remove_grades_by_assignment_id(to_remove_id)
            elif chosen_option == update_assignment:
                to_update_id = input("Enter the id of the assignment you want to update:")
                new_description = input("Enter the new description:")
                deadline = input("Enter the new deadline:")
                self.__assignmentServices.update_assignment_in_list(to_update_id, new_description, deadline)
            elif chosen_option == display_assignments:
                assignments_list = self.__assignmentServices.get_all_assignments()
                self.print_elements(assignments_list)

        elif chosen_option == give_assignments:
            print("1.Give assignment to a single student")
            print("2.Give assignment to a group of students")
            chosen_option = int(input("->"))

            if chosen_option == give_assignment_to_student:
                student_id = input("Enter the id of the student:")
                assignment_id = input("Enter the id of the assignment:")
                description = input("Enter description: ")
                deadline = input("Enter deadline: ")
                self.__gradeServices.give_assignment_to_a_student(student_id, assignment_id, description, deadline)
            elif chosen_option == give_assignment_to_group:
                group = input("Enter the group:")
                assignment_id = input("Enter the id of the assignment:")
                description = input("Enter description: ")
                deadline = input("Enter deadline: ")#must be between 1 and 30
                self.__gradeServices.add_assignments_to_a_group(group, assignment_id, description, deadline)

        elif chosen_option == grade_student:
            student_id = input("Enter the id of the student:")
            assignment_id = input("Enter the id of the assignment:")
            grade = int(input("Enter the grade:"))
            self.__gradeServices.grade_student(assignment_id, student_id, grade)

        elif chosen_option == display_statistics:
            all_students_with_given_assignments = 1
            all_late_students = 2
            students_with_best_school_situation = 3
            print("1.Display all students with a given assignment")
            print("2.Display all students who are late with an assignment")
            print("3.Display students with the best school situation")
            chosen_option = int(input("->"))
            if chosen_option == all_students_with_given_assignments:
                student = 0
                grade = 1
                assignment_id = input("Enter the id of the assignment:")
                student_list = self.__gradeServices.get_all_students_with_a_given_assignment(assignment_id)

                for student_and_grade in student_list:
                    print("--------------------------")
                    print("Id of student: " + str(student_and_grade[student].get_student_id()))
                    print("Name of student: " + str(student_and_grade[student].get_student_name()))
                    print("Group of student: " + str(student_and_grade[student].get_group()))
                    print("Grade: " + str(student_and_grade[grade]))
                    print("--------------------------")

            elif chosen_option == all_late_students:
                student_list = self.__gradeServices.get_late_students()
                self.print_elements(student_list)
            elif chosen_option == students_with_best_school_situation:
                student_list_with_grades = self.__gradeServices.get_students_with_best_school_situation()

                print("--------------------------")
                for student_and_grade in student_list_with_grades:
                    id_of_student = 0
                    grade_of_student = 1
                    print("Id of student: " + str(student_and_grade[id_of_student]))
                    print("Grade: " + str(student_and_grade[grade_of_student]))
                    print("--------------------------")
        elif chosen_option == undo_last_operation:
            self.undo_redo_service.undo()
        elif chosen_option == redo_last_operation:
            self.undo_redo_service.redo()