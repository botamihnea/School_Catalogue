class Assignment:
    def __init__(self, assignment_id, description, deadline):
        self._assignment_id = assignment_id
        self._description = description
        self._deadline = deadline

    def get_assignment_id(self):
        return self._assignment_id

    def get_description(self):
        return self._description.lower()

    def get_deadline(self):
        return self._deadline

    def __eq__(self, other):
        if not isinstance(other, Assignment):
            return False
        return self._assignment_id == other._assignment_id and self._description == other._description and self._deadline == other._deadline

    def __str__(self):
        return ("Id of the assignment:" + str(self._assignment_id) + " "
                + "\nDescription:" + str(self._description) + " " + "\nDeadline:" + str(self._deadline))