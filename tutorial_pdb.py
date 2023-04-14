import csv
import os
import pendulum
import requests
from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG
from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.operators.bash import BashOperator


FILE_COLUMNS = [
    "Serial Number",
    "Company Name",
    "Employee Markme",
    "Description",
    "Leave",
]

# NOTE: configure this as appropriate for your airflow environment
AIRFLOW_HOME = f"{os.environ.get('HOME')}/airflow"
FILES_DIRECTORY = f"{AIRFLOW_HOME}/files"

GOOD_INPUT_URL = "https://raw.githubusercontent.com/apache/airflow/main/docs/apache-airflow/tutorial/pipeline_example.csv"
BAD_INPUT_URL = "https://raw.githubusercontent.com/jbaek/gx_tutorial/main/employees_bad.csv"


def transform_leave_column(leave: str) -> str:
    # breakpoint()
    return str(int(leave) + 1)


@dag(
    dag_id="tutorial_pdb",
    schedule_interval="0 0 * * *",
    start_date=pendulum.datetime(2023, 4, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=timedelta(minutes=10),
)

def TutorialPdb():

    @task
    def get_data():
        data_path = f"{FILES_DIRECTORY}/employees.csv"
        os.makedirs(os.path.dirname(data_path), exist_ok=True)

        url = GOOD_INPUT_URL
        # url = BAD_INPUT_URL

        response = requests.request("GET", url)

        with open(data_path, "w") as file:
            file.write(response.text)

    @task
    def filter_and_tranform_data():
        input_data_path = f"{FILES_DIRECTORY}/employees.csv"
        output_data_path = f"{FILES_DIRECTORY}/employees_filtered.csv"
        bad_input_data_path = f"{FILES_DIRECTORY}/employees_bad.csv"

        with open(input_data_path, "r") as input_file:
            with open(output_data_path, "w") as output_file, open(bad_input_data_path, "w") as bad_input_file:
                csv_reader = csv.DictReader(input_file)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        writer = csv.DictWriter(output_file, fieldnames=FILE_COLUMNS)
                        bad_writer = csv.DictWriter(bad_input_file, fieldnames=FILE_COLUMNS)
                        print(f'Column names are {", ".join(row)}')
                        writer.writeheader()
                        bad_writer.writeheader()
                        line_count += 1
                    if row["Description"] == "ACADEMIC FOUNDATION":
                        row["Leave"] = transform_leave_column(row["Leave"]) 
                        writer.writerow(row)
                        # try: 
                        #     row["Leave"] = transform_leave_column(row["Leave"]) 
                        # #     writer.writerow(row)
                        # except:
                            # breakpoint()

                            # bad_writer.writerow(row)
                    line_count += 1
                print(f'Processed {line_count} lines.')


    get_data() >> filter_and_tranform_data()

dag = TutorialPdb()

if __name__ == "__main__":
    dag.test()
