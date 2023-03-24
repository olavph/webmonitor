from kafka import KafkaConsumer
import psycopg2


class DBWriter:
    def __init__(self, topic: str, db_name: str, table_name: str, event_type: type):
        self.topic = topic
        self._create_queries(table_name, event_type)
        self.decode_function = event_type.decode
        self.connection = psycopg2.connect(f"dbname={db_name}")
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.print_db()
        # self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def run(self):
        self._create_table()
        consumer = KafkaConsumer(self.topic)
        for msg in consumer:
            event = self.decode_function(msg.value)
            self.cursor.execute(self.insert_query, event.to_tuple())
            print(f"Inserted {event}")

    def print_db(self):
        self.cursor.execute(self.select_query)
        for record in self.cursor:
            print(record)

    def _create_queries(self, table_name: str, event_type: type):
        assert(len(event_type.db_fields()) == len(event_type.db_types()))

        types_str = ", ".join(map(lambda pair: " ".join(pair), zip(event_type.db_fields(), event_type.db_types())))
        self.create_table_query = f"CREATE TABLE {table_name} (id serial PRIMARY KEY, {types_str})"
        print(self.create_table_query)

        fields_str = ", ".join(event_type.db_fields())
        placeholders_str = ", ".join(["%s"] * len(event_type.db_fields()))
        self.insert_query = f"INSERT INTO {table_name} ({fields_str}) VALUES ({placeholders_str})"
        print(self.insert_query)

        self.select_query = f"SELECT * FROM {table_name}"
        print(self.select_query)

    def _create_table(self):
        try:
            self.cursor.execute(self.create_table_query)
        except psycopg2.errors.DuplicateTable:
            pass
