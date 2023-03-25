import psycopg2

from webevent.consumer import Consumer


class DBWriter:
    """DBWriter consumes events and writes them to a PostgreSQL database
    """

    def __init__(self, consumer: Consumer, db_name: str, table_name: str, event_type: type):
        """Initialize connection to database

        Args:
            consumer (Consumer): iterable of events
            db_name (str): name of the PostgreSQL database
            table_name (str): table to write events
            event_type (type): type of events being written, to get database fields information
        """
        self.consumer = consumer
        self._create_queries(table_name, event_type)
        self.connection = psycopg2.connect(f"dbname={db_name}")
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.print_db()
        # self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def run(self):
        """Create table in database and insert rows for each event until interrupted
        """
        self._create_table()
        for event in self.consumer:
            self.cursor.execute(self.insert_query, event.to_tuple())
            print(f"Inserted {event}")

    def print_db(self):
        """Print database table to stdout
        """
        self.cursor.execute(self.select_query)
        for record in self.cursor:
            print(record)

    def _create_queries(self, table_name: str, event_type: type):
        """Format queries that will be used in execute commands
        """
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
        """Create table in database, if not existent
        """
        try:
            self.cursor.execute(self.create_table_query)
        except psycopg2.errors.DuplicateTable:
            pass
