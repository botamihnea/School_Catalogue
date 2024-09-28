class Grade:
    def __init__(self, assignment_id, student_id, grade_value):
        self._assignment_id = assignment_id
        self._student_id = student_id
        self._grade_value = grade_value

    def get_assignment_id(self):
        return self._assignment_id

    def get_student_id(self):
        return self._student_id

    def get_grade_value(self):
        return self._grade_value

    def __str__(self):
        return ("Assignment id:" + str(self._assignment_id) + " "
                + "\nStudent id:" + str(self._student_id) + " " + "\nGrade value:" + str(self._grade_value))

    def __eq__(self, other):
        if not isinstance(other, Grade):
            return False
        return self._assignment_id == other._assignment_id and self._student_id == other._student_id and self._grade_value == other._grade_value