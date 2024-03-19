from datetime import date
import psycopg


ID_INDEX = 0
FIRST_NAME_INDEX = 1
LAST_NAME_INDEX = 2
EMAIL_INDEX = 3
DATE_INDEX = 4


def students_as_map(records):
    """
    Converts a sequence of students records to a map
    :param records: a sequence of the records of the students table
    :return: a map of student ID to the remaining attributes. the attributes will no longer contain the student id,
    and as a result the index constants provided in this file will no longer be accurate (by 1).
    """
    id_map = {}
    for record in records:
        id_map[record[ID_INDEX]] = record[1:]  # remove ID

    return id_map


class StudentsConnection:
    """
    Holds a connection to the database and provides some methods to read and modify the students table.
    """

    def __init__(self, database_name: str, user: str, password: str, auto_commit=True):
        """
        :param database_name: the name of the DB to connect to
        :param user: the username to connect with
        :param password: the password to connect with
        :param auto_commit: if the changes from a method call should be automatically comitted to the DB
        """
        self.connection = psycopg.connect(f"dbname={database_name} user={user} password={password}")
        self.autocommit = auto_commit

    def disconnect(self):
        """
        Disconnects from the DB
        """
        self.connection.close()

    def getAllStudents(self) -> list:
        """
        Retrieves the whole students table.
        :return: a list of records of the students table
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students;")
            return cursor.fetchall()  # fetchall returns all records found

    def addStudent(self, first_name: str, last_name: str, email: str, enrollment_date: date) -> None:
        """
        Adds a student to the student table.
        :param first_name: the first name of the student to add
        :param last_name: the last name of the student to add
        :param email: the email of the student to add
        :param enrollment_date: their enrollment date
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO students (first_name, last_name, email, enrollment_date) 
            VALUES (%s, %s, %s, %s);
            """, (first_name, last_name, email, enrollment_date))

            if self.autocommit:
                self.connection.commit()

    def updateStudentEmail(self, student_id: int, new_email: str) -> None:
        """
        Updates an existing student's email. Does nothing if the student doesn't exist in the students table.
        :param student_id: the student to update
        :param new_email: the new email to use
        :return:
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
            UPDATE students
            SET email = %s
            WHERE student_id=%s;
            """, (new_email, student_id))

            if self.autocommit:
                self.connection.commit()

    def deleteStudent(self, student_id: int):
        """
        Removes a student from the students table
        :param student_id: the ID of the student to be removed
        """
        with self.connection.cursor() as cursor:
            cursor.execute("""
            DELETE FROM students
            WHERE student_id=%s
            """, (student_id,))

            if self.autocommit:
                self.connection.commit()
