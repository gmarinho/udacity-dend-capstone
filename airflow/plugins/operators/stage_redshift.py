from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook

class StageToRedshiftOperator(BaseOperator):
    template_fields = ['s3_key']
    
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 region= "us-west-2",
                 format_file = 'json',
                 operation = 'append',
                 copy_json = 'auto',
                 delimiter = ';',
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.region = region
        self.format_file = format_file
        self.copy_json = copy_json
        self.execution_date = kwargs.get('execution_date')
        self.operation = operation
        self.sql_query = ""
        self.delimiter = delimiter

        
    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
        if self.format_file == 'JSON':
            self.sql_query = """
                            COPY {}
                            FROM '{}'
                            ACCESS_KEY_ID '{}'
                            SECRET_ACCESS_KEY '{}'
                            REGION '{}'
                            FORMAT as JSON '{}'
                            """.format(self.table,s3_path,credentials.access_key,credentials.secret_key,self.region,self.copy_json)
        else:
            self.sql_query = """
                            COPY {}
                            FROM '{}'
                            ACCESS_KEY_ID '{}'
                            SECRET_ACCESS_KEY '{}'
                            REGION '{}'
                            DELIMITER '{}'
                            CSV
                            IGNOREHEADER 1
                            TRUNCATECOLUMNS
                            """.format(self.table,s3_path,credentials.access_key,credentials.secret_key,self.region, self.delimiter)
                
        if self.operation == 'delete':
            self.log.info("Clearing data from destination Redshift table")
            redshift.run("DELETE FROM {}".format(self.table))
        self.log.info("Copying data from S3 to Redshift")

        redshift.run(self.sql_query)
        self.log.info("Copy to Redshift table {} from S3 finished".format(self.table))





