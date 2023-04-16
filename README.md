# ETL DAG using Airflow
This is a simple ETL (Extract, Transform, Load) DAG (Directed Acyclic Graph) using Airflow, which is an open-source platform to programmatically author, schedule and monitor workflows.

## Code
This DAG consists of three PythonOperator tasks: **extract**, **transform** and **load**.

**extract**: This task extracts the text data from a file in the local file system and pushes it to XCom, which is a tool provided by Airflow to exchange messages between tasks.

**transform**: This task counts the number of words in the text data retrieved by the extract task using XCom, and then pushes the word count to XCom.

**load**: This task loads the word count from XCom into the same file from which the data was extracted.

# Dependencies
This DAG has the following dependencies:

**datetime**: Python module for manipulating dates and times.

**pytz**: Python module for working with time zones.

**airflow**: Python module for Airflow.

# Usage
To use this DAG, you need to have Airflow installed and running.

1. Copy the code into a file named **etl_dag.py**.

2. Replace the path to the text file (**/path/to/file/etl_text.txt**) in the **extract** and **load** tasks with the actual path to the text file on your local file system.

3. Save the file in the dags folder of your Airflow installation.

4. Start the Airflow scheduler using the command **airflow scheduler**.

5. Start the Airflow web server using the command **airflow webserver**.

6. Access the Airflow web interface at **http://localhost:8080** in your web browser.

7. Navigate to the DAGs page and turn on the **etl_test** DAG.

The DAG will run every 10 minutes and extract, transform and load the data in the text file. The word count will be appended to the end of the file each time the DAG runs. You can monitor the progress of the DAG in the Airflow web interface.