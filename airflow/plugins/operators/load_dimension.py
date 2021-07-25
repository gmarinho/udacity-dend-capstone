from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E' 
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_query ='',
                 is_append = False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql_query = sql_query
        self.is_append = is_append
        self.table = table

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if not self.is_append:
            self.log.info(f"Deleting data from {self.table}")
            redshift.run(f"DELETE FROM {self.table}")
        sql = f"INSERT INTO {self.table} {self.sql_query}"
        self.log.info(f"Inserting data into dimension table {self.table}")
        redshift.run(sql)
        self.log.info(f"Dimension table {self.table} updated sucessfully")

