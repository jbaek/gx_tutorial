# [TUTORIAL] Debugging and Testing Airflow


## Part 1: Debugging Airflow with pdb

In this part of the tutorial, you will debug an error in an Airflow pipeline using Python’s pdb debugger. You will learn the following:



* The code needed to start the debugger
* Learn the basic features and their commands
* See situations where the debugger is an improvement over `print()` statements
* “Break” the pipeline, then find the bug and fix it


### Prerequisites and Setup



* Python 3.7+ and Airflow (2.5.3) are installed
    * You should have a basic understanding of both (i.e. you can read the Python code and know what a DAG is and you can get one to run)
* Terminal app
* [PIpeline code](https://github.com/jbaek/gx_tutorial/blob/main/tutorial_pdb.py)
* The [pdb doc](https://docs.python.org/3/library/pdb.html) is helpful to have open to look up commands


### Pipeline: `tutorial_pdb.py`



* This is a very simple and contrived pipeline that fetches data from a url and writes a CSV locally employees.csv 
* Then the CSV file is parsed and when the Description column is “ACADEMIC FOUNDATION”, the “Leave” column is incremented by one. And the entire row is written to a new CSV file employess_filered.csv 


### Tutorial


#### Good Input

We start with the happy path to see what the pipeline is supposed to do. 



1. Run a test of the DAG with either command
    1. `python ~/airflow/dags/tutorial_pdb.py`
    2. `airflow dags test tutorial_pdb 2023-04-05`
2. View files written
    3. Input Data
        1. `more ~/airflow/files/employees.csv`
    4. Filtered Data
        2. `more ~/airflow/files/employees_filtered.csv`
        3. Only contains rows with “Description” equal to “ACADEMIC FOUNDATION” and the “Leave” value was incremented by one
    5. Bad Data
        4. `more ~/airflow/files/employees_bad.csv`
        5. File is empty


#### Bad Input

We switch to the sad path to see what might happen if the input data has an unexpected value. And we can use the debugger to find and fix our bug. 



1. Switch from GOOD_INPUT_URL to BAD_INPUT_URL
    1. Comment line 50 (`url = GOOD_INPUT_URL`) 
    2. Uncomment line 51 (`url = BAD_INPUT_URL`)
    3. Rerun test using command above
    4. You should receive a 
        1. `ValueError: invalid literal for int() with base 10: 'Zero'` 
2. Look at the stack trace to find the line of code that failed:
    5. `File "/Users/jasonbaek/airflow/dags/tutorial_pdb.py", line 32, in transform_leave_column`
    6. `return str(int(leave) + 1)`



<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image1.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image1.png "image_tooltip")




3. Add a breakpoint to `transform_leave_column()` function
    7. Uncomment line 31: `breakpoint()` 
    8. Save the change
    9. Rerun test
4. Debug!
    10. The Pdb debugger prompt appears as: `(Pdb)`
    11. It will display the next code of line to run after the breakpoint
        2. `/Users/jasonbaek/airflow/dags/tutorial_pdb.py(32)transform_leave_column()`
        3. `-> return str(int(leave) + 1)`
    12. Type `h` to see available commands
    13. Type `l` to see surrounding source code
    14. Type `a` to see arguments of current function called
    15. Type `p leave` to print its value
    16. Type `whatis leave` to see the type of the leave variable
    17. Type `w` to see the stack trace again
    18. Type `s` to run the next line of code
        4. Runs successfully
    19. Type `c` to continue
    20. Type `p leave` to print its value
    21. Repeat c and p leave until error encountered
    22. Type `u` to go up a frame in the stack
    23. Type `pp row` to view the row dictionary


#### Better Debugging

You can see if we had more lines to review before encountering this error this process would be really tedious. Or if other columns in the file had Zero values, it might be harder to find the problematic line. So we can improve the code to make debugging easier and improve the code as well. 



1. Switch `transform_leave_column()` with try-except
    1. Uncomment lines 79-83
    2. Comment line 31
    3. Comment lines 77-78
    4. Run test
    5. Type `pp row `to print its value


#### Fix the Bug

Now we know that the “Leave” column may contain a string and the code needs to handle it appropriately. We’ll do this by filtering out the bad input data and writing it to a separate file for later analysis. 



1. Comment line 83
2. Uncomment line 85
3. Run test 
4. Type `c` to continue and there will be no error.
5. View data files again
    1. `more ~/airflow/files/employees_filtered.csv`
    2. Only 3 lines now
6. Replace breakpoint with write to bad file
    3. Uncomment line 85
    4. Comment line 83
    5. Run test
    6. `more ~/airflow/files/employees_bad.csv`
        1. See the one bad row


#### Commands Covered



* h(elp): see command list
* l(ist): see source code
* a(rgs): prints argument list of current function
* p &lt;expression>: print an expression
* whatis &lt;expression>: print type of expression
* w(here): to see stack trace
* s(tep): execute next line
* c(ontinue): execute until next breakpoint
* u(p): move up the stack trace
* q(uit): quit debugger


### References


#### Airflow



* [Quick Install](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
* [Sample Pipeline Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html)


#### pdb



* p[db python doc](https://docs.python.org/3/library/pdb.html)
* [Real Python pdb Tutorial](https://realpython.com/python-debugging-pdb/)
* [Debug Airflow on the command line](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/debug.html#debugging-airflow-dags-on-the-command-line)


## Part 2: Testing Airflow DAGs

To be continued…


### References



* [Airflow: Testing a DAG](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#testing-a-dag)
    * Unit Testing
    * Staging Environment
    * Mocking Variables and Connections
