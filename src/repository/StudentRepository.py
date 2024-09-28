from src.domain.student import Student
import pickle

class StudentRepository:
    def __init__(self):
        self._students_list = []

    def add_student(self, student_id, name, group):
        student = Student(student_id, name, group)
        self._students_list.append(student)
        self._save_to_file()

    def remove_student(self, to_remove_id):
        new_students_list = []

        for student in self._students_list:
            if str(student.get_student_id()) != str(to_remove_id):
                new_students_list.append(student)

        self._students_list = new_students_list
        self._save_to_file()

    def update_student(self, to_update_id, new_name, group):
        updated_student = Student(to_update_id, new_name, group)
        updated_student_list = []

        for student in self._students_list:
            if str(student.get_student_id()) == str(to_update_id):
                student = updated_student

            updated_student_list.append(student)

        self._students_list = updated_student_list
        self._save_to_file()

    def get_all_students(self):
        return self._students_list

    def get_student_group(self, student_id):
        for student in self._students_list:
            if str(student.get_student_id()) == str(student_id):
                return student.get_group()

    def get_student_name_(self, student_id):
        for student  in self._students_list:
            if str(student.get_student_id()) == str(student_id):
                return student.get_student_name()

    def get_student_with_given_id(self, given_id) -> Student:#so that the returned value is type student
        for student in self._students_list:
            if str(student.get_student_id()) == str(given_id):
                return student

    def _save_to_file(self):
        pass

class TextFileStudentRepository(StudentRepository):
    def __init__(self, file_path):
        super().__init__()
        self.__file_path = file_path
        self._save_to_file()

    def read_from_file(self):
        with open(self.__file_path, 'r') as file:
            for line in file:
                line = line.strip()

                if line == "":
                    continue

                student_id, student_name, group = line.split(",")
                read_Student = Student(student_id, student_name, group)
                self._students_list.append(read_Student)

    def __to_string(self):
        saved_format = ""

        for student in self._students_list:
            saved_format += (str(student.get_student_id()) + "," + str(student.get_student_name())
                             + "," + str(student.get_group()) + "\n")
        return saved_format

    def _save_to_file(self):
        with open(self.__file_path, "w") as file:
            file.truncate(0)
            file.write(self.__to_string())


class StudentRepositoryBinaryFile(StudentRepository):
    def __init__(self, file_path):
        super().__init__()
        self.__file_path = file_path
        self._save_to_file()

    def __read_from_file(self):
        file = open(self.__file_path, "rb")
        self._assignments_list = pickle.load(file)
        file.close()

    def __len__(self):
        return len(self._students_list)

    def _save_to_file(self):
        file = open(self.__file_path, "wb")
        pickle.dump(self._students_list, file)
        file.close()



