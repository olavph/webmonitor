from kafka import KafkaConsumer
import psycopg2


class DBWriter:
    def __init__(self, topic: str, db_name: str, create_table_query: str, insert_query: str):
        self.topic = topic
        self.connection = psycopg2.connect(f"dbname={db_name}")
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute(create_table_query)
        except psycopg2.errors.DuplicateTable:
            pass
        self.insert_query = insert_query

    def __del__(self):
        self.print_db()
        # self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def run(self):
        consumer = KafkaConsumer(self.topic)
        for event in consumer:
            self.cursor.execute(self.insert_query, event.value.decode("utf-8").split(","))
            print(f"Inserted: {event}")

    def print_db(self):
        self.cursor.execute("SELECT * FROM test;")
        for record in self.cursor:
            print(record)
