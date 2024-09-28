from src.domain.assignment import Assignment
from src.repository.ErrorRepository import RepositoryError
import pickle

class AssignmentRepository:
    def __init__(self):
        self._assignments_list = []

    def add_assignment(self, assignment_id, description, deadline):
        new_assignment = Assignment(assignment_id, description, deadline)

        if new_assignment in self._assignments_list:
            raise RepositoryError("Assignment already exists")

        self._assignments_list.append(new_assignment)
        self._save_to_file()

    def remove_assignment(self, id_to_remove):
        new_assignments_list = []

        for assignment in self._assignments_list:
            if str(assignment.get_assignment_id()) != str(id_to_remove):
                new_assignments_list.append(assignment)

        self._assignments_list = new_assignments_list
        self._save_to_file()

    def update_assignment(self, to_update_id, new_description, deadline):
        updated_list = []
        new_assignment = Assignment(to_update_id, new_description, deadline)
        for assignment in self._assignments_list:
            if str(assignment.get_assignment_id()) == str(to_update_id):
                assignment = new_assignment
            updated_list.append(assignment)

        self._assignments_list = updated_list
        self._save_to_file()

    def get_all_assignments(self):
        return self._assignments_list

    def get_assignment_with_given_id(self, given_id) -> Assignment:
        for assignment in self._assignments_list:
            if str(assignment.get_assignment_id()) == str(given_id):
                return assignment

    def get_assignment_with_given_id_description(self, given_id) -> Assignment:
        for assignment in self._assignments_list:
            if str(assignment.get_assignment_id()) == str(given_id):
                return assignment.get_description()

    def get_assignment_with_given_id_deadline(self, given_id) -> Assignment:
        for assignment in self._assignments_list:
            if str(assignment.get_assignment_id()) == str(given_id):
                return assignment.get_deadline()

    def _save_to_file(self):
        pass

class TextFileAssignmentRepository(AssignmentRepository):
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

                assignment_id, assignment_description, assignment_deadline = line.split(",")
                read_Assignment = Assignment(assignment_id, assignment_description, assignment_deadline)
                self._assignments_list.append(read_Assignment)

    def __to_string(self):
        saved_format = ""

        for assignment in self._assignments_list:
            saved_format += (str(assignment.get_assignment_id()) + "," + str(assignment.get_description())
                             + "," + str(assignment.get_deadline()) + "\n")

        return saved_format

    def _save_to_file(self):
        with open(self.__file_path, "w") as file:
            file.truncate(0)
            file.write(self.__to_string())

class AssignmentRepositoryBinaryFile(AssignmentRepository):
    def __init__(self, file_path):
        super().__init__()
        self.__file_path = file_path
        self._save_to_file()

    def __read_from_file(self):
        file = open(self.__file_path, "rb")
        self._assignments_list = pickle.load(file)
        file.close()

    def __len__(self):
        return len(self._assignments_list)

    def _save_to_file(self):
        file = open(self.__file_path, "wb")
        pickle.dump(self._assignments_list, file)
        file.close()



