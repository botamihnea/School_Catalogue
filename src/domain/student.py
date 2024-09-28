class Student:
    def __init__(self, student_id, name, group):
        self.__student_id = student_id
        self.__name = name
        self.__group = group

    def get_student_id(self):
        return self.__student_id

    def get_student_name(self):
        return self.__name.lower()

    def get_group(self):
        return self.__group

    def __str__(self):
        return ("Id of the student:" + str(self.__student_id) + " "
                + "\nName:" + str(self.__name) + " " + "\nGroup:" + str(self.__group))