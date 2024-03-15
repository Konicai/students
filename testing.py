import unittest
from students import StudentsConnection
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

        self.assertEqual(1, result[0][0])  # 1st record should have ID 1
        self.assertEqual(2, result[1][0])  # 2nd record should have ID 2

        self.assertEqual("John", result[0][1])
        self.assertEqual("jane.smith@example.com", result[1][3])
        self.assertEqual(datetime.date(2023, 9, 2), result[2][4])


if __name__ == '__main__':
    unittest.main()
