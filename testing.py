import unittest
from students import *
import datetime


class MyTestCase(unittest.TestCase):
    students = None

    @classmethod
    def setUpClass(cls) -> None:
        # connect to database
        cls.students = StudentsConnection("assignment3", "postgres", "PASSWORD", auto_commit=False)

    @classmethod
    def tearDownClass(cls) -> None:
        # disconnect from database
        cls.students.disconnect()

    def setUp(self) -> None:
        # start a transaction for the test
        self.students.connection.transaction()

    def tearDown(self) -> None:
        # rollback the transaction (anything the test changed)
        self.students.connection.rollback()

    def test_get_all(self):
        result = self.students.getAllStudents()

        self.assertEqual(3, len(result))  # amount of records
        self.assertEqual(5, len(result[0]))  # length of records

        self.assertEqual(1, result[0][ID_INDEX])  # 1st record should have ID 1
        self.assertEqual(2, result[1][ID_INDEX])  # 2nd record should have ID 2

        self.assertEqual("John", result[0][FIRST_NAME_INDEX])
        self.assertEqual("jane.smith@example.com", result[1][EMAIL_INDEX])
        self.assertEqual(datetime.date(2023, 9, 2), result[2][DATE_INDEX])

    def test_add_student(self):
        student = ("Zane", "Labonte-Hagar", "zanelabontehagar@cmail.carleton.ca", datetime.date(2024, 3, 15))

        self.students.addStudent(student[0], student[1], student[2], student[3])

        result = self.students.getAllStudents()
        result = [s[1:] for s in result]  # remove the SERIAL student_id from each because it's unreliable for testing

        self.assertIn(student, result)

    def test_update_student_email(self):
        student_id = 1
        new_email = "john@gmail.com"

        self.students.updateStudentEmail(student_id, new_email)

        result = self.students.getAllStudents()
        # email index reduced because we converted to map
        result_email = students_as_map(result)[student_id][EMAIL_INDEX - 1]

        self.assertEqual(new_email, result_email)

    def test_update_student_email_invalid(self):
        self.students.updateStudentEmail(100, "whatever")
        size = len(self.students.getAllStudents())
        self.assertEqual(3, size)  # student doesn't exist - size should not have changed

    def test_delete_student(self):
        # email of student with student ID 0
        student_id = 1

        self.students.deleteStudent(student_id)

        result = self.students.getAllStudents()
        result_map = students_as_map(result)

        self.assertNotIn(student_id, result_map)
        self.assertEqual(2, len(result))
        pass

    def test_delete_student_invalid(self):
        # delete student that doesn't exist
        self.students.deleteStudent(100)
        size = len(self.students.getAllStudents())
        self.assertEqual(3, size)


if __name__ == '__main__':
    unittest.main()
