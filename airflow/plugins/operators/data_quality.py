from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 sql_tests=[],
                 tests_results =[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql_tests = sql_tests
        self.tests_results = tests_results

    def execute(self, context):
        if len(self.sql_tests) != len(self.tests_results):
            self.log.info('Lenght mismatch between the number of tests provided and the number of expected results')
            raise ValueError("Lenght mismatch between the number of tests provided and the number of expected results")
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)        
        for i in range(len(self.sql_tests)):
            self.log.info('Running test')
            records = redshift_hook.get_records(self.sql_tests[i])
            if records[0][0] == self.tests_results[i]:
                self.log.info('Test passed sucessfully')
            else:
                self.log.info("Test query '{}' returned '{}' instead of the expected ouput '{}'".format(
                self.sql_tests[i],
                records[0][0],
                self.tests_results[i]))
                raise ValueError("Test results didn't match with expected output")
 
            