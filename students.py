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
    :return: a map of student ID to the remaining attributes
    """
    id_map = {}
    for record in records:
        id_map[record[ID_INDEX]] = record[1:]  # remove ID

    return id_map


class StudentsConnection:

    def __init__(self, database_name: str, user: str, password: str, auto_commit=True):
        self.connection = psycopg.connect(f"dbname={database_name} user={user} password={password}")
        self.autocommit = auto_commit

    def disconnect(self):
        self.connection.close()

    def getAllStudents(self) -> list:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students;")
            return cursor.fetchall()

    def addStudent(self, first_name: str, last_name: str, email: str, enrollment_date: date) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO students (first_name, last_name, email, enrollment_date) 
            VALUES (%s, %s, %s, %s);
            """, (first_name, last_name, email, enrollment_date))

            if self.autocommit:
                self.connection.commit()

    def updateStudentEmail(self, student_id: int, new_email: str) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("""
            UPDATE students
            SET email = %s
            WHERE student_id=%s;
            """, (new_email, student_id))

            if self.autocommit:
                self.connection.commit()

    def deleteStudent(self, student_id: int):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            DELETE FROM students
            WHERE student_id=%s
            """, (student_id,))

            if self.autocommit:
                self.connection.commit()
