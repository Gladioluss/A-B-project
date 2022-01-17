from transliterate import translit


class Employee:

    def __init__(self, fullname, password, emailAddress):
        self.__fullname = fullname
        self.__password = password
        self.__emailAddress = emailAddress

    def get_fullname(self):
        return self.__fullname

    def get_password(self):
        return self.__password

    def get_emailAddress(self):
        return self.__emailAddress

