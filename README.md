# students

`students.py` contains a StudentsConnection instance to handle the connection and read/write to the database. `testing.py` contains `unittest` testing to automatically and independantly test methods.  
The database it connects to should be initialized with `initializer.sql`. See the table within for details.

#### Compilation and run instructions

To run all tests independantly and automatically, run the tests in `testing.py` using PyCharm (or equivalent) or by executing `testing.py`.  
Note: your own database name, username, and password must be properly specified in `testing.py` before running it.

If the results must be viewed in pgAmin, then enable `commit_changes` in `testing.py`. Otherwise, it is disabled by default, and the changes from each unit test are automatically rolled back.  
Since each unit test is based on the initial conditions of the database, the database must be reset with `initializer.sql` before each unit test (if changes are being committed) is run. I recommend running unit tests individually using PyCharm or any equivalent IDE.

Video demonstration available here: https://mediaspace.carleton.ca/media/t/1_rcdd7043
