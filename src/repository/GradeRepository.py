from src.domain.grade import Grade
import pickle

class GradeRepository:
    def __init__(self):
        self._grades_list = []

    def add_grade(self, assignment_id, student_id, grade_value):
        grade = Grade(assignment_id, student_id, grade_value)

        if grade in self._grades_list:
            raise ValueError("Grade already exists")

        for any_grade in self._grades_list:
            if str(any_grade.get_student_id()) == str(student_id) and str(any_grade.get_assignment_id()) == str(assignment_id):
                self._grades_list.remove(any_grade)

        self._grades_list.append(grade)
        self._save_to_file()

    def get_students_with_assignment(self, assignment_id):
        students_list = []
        for grade in self._grades_list:
            if str(grade.get_assignment_id()) == str(assignment_id):
                students_list.append((grade.get_student_id(), grade.get_grade_value()))

        return students_list

    def remove_grade_by_assignment_id(self, to_remove_assignment_id):
        new_grades_list = []
        for grade in self._grades_list:
            if str(grade.get_assignment_id) != str(to_remove_assignment_id):
                new_grades_list.append(grade)

        self._grades_list[:] = new_grades_list
        self._save_to_file()

    def remove_grade(self, assignment_id, student_id, grade_value):
        new_grade_list = []
        grade_to_be_removed = Grade(assignment_id, student_id, grade_value)

        for grade in self._grades_list:
            if grade != grade_to_be_removed:
                new_grade_list.append(grade)

        self._grades_list = new_grade_list
        self._save_to_file()

    def get_all_grades(self):
        return self._grades_list

    def _save_to_file(self):
        pass

class TextFileGradeRepository(GradeRepository):
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

                assignment_id, student_id, grade_value = line.split(",")
                read_Grade = Grade(assignment_id, student_id, grade_value)
                self._grades_list.append(read_Grade)

    def __to_string(self):
        saved_format = ""

        for grade in self._grades_list:
            saved_format += (str(grade.get_assignment_id()) + "," + str(grade.get_student_id())
                             + "," + str(grade.get_grade_value()) + "\n")
        return saved_format

    def _save_to_file(self):
        with open(self.__file_path, "w") as file:
            file.truncate(0)
            file.write(self.__to_string())


class GradeRepositoryBinaryFile(GradeRepository):
    def __init__(self, file_path):
        super().__init__()
        self.__file_path = file_path
        self._save_to_file()

    def __read_from_file(self):
        file = open(self.__file_path, "rb")
        self._assignments_list = pickle.load(file)
        file.close()

    def __len__(self):
        return len(self._grades_list)

    def _save_to_file(self):
        file = open(self.__file_path, "wb")
        pickle.dump(self._grades_list, file)
        file.close()


