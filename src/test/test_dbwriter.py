from unittest import mock
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import sentinel

from webevent.dbwriter import DBWriter
from webevent.webevent import WebEvent


@patch('psycopg2.connect')
class TestDBWriter(TestCase):

    def test_dbwriter_constructor_connects(self, psycopg2_connect):
        consumer = []
        event_type = WebEvent

        writer = DBWriter(consumer, sentinel.table_name, event_type, sentinel.host, sentinel.port, sentinel.user)

        psycopg2_connect.assert_called_once()
        kwargs = psycopg2_connect.call_args.kwargs
        self.assertEquals(sentinel.host, kwargs["host"])
        self.assertEquals(sentinel.port, kwargs["port"])
        self.assertEquals(sentinel.user, kwargs["user"])


    def test_dbwriter_run_creates_table(self, psycopg2_connect):
        cursor = psycopg2_connect.return_value.cursor.return_value
        consumer = []
        event_type = WebEvent
        writer = DBWriter(consumer, sentinel.table_name, event_type, sentinel.host, sentinel.port, sentinel.user)

        writer.run()

        psycopg2_connect.assert_called_once()
        create_table_cmd = "CREATE TABLE sentinel.table_name (id serial PRIMARY KEY, url varchar, status_code integer, response_time real, match_found bool, match varchar)"
        cursor.execute.assert_called_once_with(create_table_cmd)


    def test_dbwriter_run_creates_table_before_inserting(self, psycopg2_connect):
        cursor = psycopg2_connect.return_value.cursor.return_value
        event = mock.MagicMock()
        event.to_tuple.return_value = tuple(range(5))
        consumer = [event]
        event_type = WebEvent
        writer = DBWriter(consumer, sentinel.table_name, event_type, sentinel.host, sentinel.port, sentinel.user)

        writer.run()

        psycopg2_connect.assert_called_once()
        self.assertEqual(cursor.execute.call_count, 2)
        create_table_cmd = "CREATE TABLE sentinel.table_name (id serial PRIMARY KEY, url varchar, status_code integer, response_time real, match_found bool, match varchar)"
        cursor.execute.assert_any_call(create_table_cmd)
        insert_cmd = "INSERT INTO sentinel.table_name (url, status_code, response_time, match_found, match) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute.assert_called_with(insert_cmd, tuple(range(5)))


    def test_dbwriter_run_iterates_until_exhausted(self, psycopg2_connect):
        cursor = psycopg2_connect.return_value.cursor.return_value
        event = mock.MagicMock()
        event.to_tuple.return_value = tuple(range(5))
        consumer = [event, event, event]
        event_type = WebEvent
        writer = DBWriter(consumer, sentinel.table_name, event_type, sentinel.host, sentinel.port, sentinel.user)

        writer.run()

        psycopg2_connect.assert_called_once()
        self.assertEqual(cursor.execute.call_count, 4)
        create_table_cmd = "CREATE TABLE sentinel.table_name (id serial PRIMARY KEY, url varchar, status_code integer, response_time real, match_found bool, match varchar)"
        cursor.execute.assert_any_call(create_table_cmd)
        insert_cmd = "INSERT INTO sentinel.table_name (url, status_code, response_time, match_found, match) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute.assert_called_with(insert_cmd, tuple(range(5)))
