from unittest import TestCase
from unittest.mock import sentinel

from webevent.webevent import WebEvent


class TestStringMethods(TestCase):

    def test_webevent_eq_another(self):
        one_event = WebEvent(sentinel.url, 200, 0.1, True, "")
        other_event = WebEvent(sentinel.url, 200, 0.1, True, "")

        self.assertEqual(one_event, other_event)


    def test_webevent_not_eq_another(self):
        one_event = WebEvent(sentinel.url, 200, 0.1, True, "")

        other_event = WebEvent(sentinel.url2, 200, 0.1, True, "")
        self.assertNotEqual(one_event, other_event)

        other_event = WebEvent(sentinel.url, 300, 0.1, True, "")
        self.assertNotEqual(one_event, other_event)

        other_event = WebEvent(sentinel.url, 200, 0.2, True, "")
        self.assertNotEqual(one_event, other_event)

        other_event = WebEvent(sentinel.url, 200, 0.1, False, "")
        self.assertNotEqual(one_event, other_event)

        other_event = WebEvent(sentinel.url, 200, 0.1, True, "match")
        self.assertNotEqual(one_event, other_event)


    def test_webevent_repr_has_all_fields(self):
        fields = ("url", 200, 0.1, True, "match")
        event = WebEvent(*fields)

        event_repr = repr(event)
        for field in fields:
            self.assertIn(str(field), event_repr)


    def test_webevent_str_has_all_fields(self):
        fields = ("url", 200, 0.1, True, "match")
        event = WebEvent(*fields)

        event_str = str(event)
        for field in fields:
            self.assertIn(str(field), event_str)


    def test_webevent_to_tuple_has_all_fields(self):
        fields = ("url", 200, 0.1, True, "match")
        event = WebEvent(*fields)

        self.assertEqual(event.to_tuple(), fields)


    def test_webevent_encode_decode(self):
        event = WebEvent("url", 200, 0.1, True, "match")

        self.assertEqual(event, WebEvent.decode(event.encode()))


    def test_webevent_db_fields_has_right_size(self):
        fields = ("url", 200, 0.1, True, "match")
        event = WebEvent(*fields)

        self.assertEqual(len(WebEvent.db_fields()), len(event.to_tuple()))


    def test_webevent_db_types_has_right_size(self):
        fields = ("url", 200, 0.1, True, "match")
        event = WebEvent(*fields)

        self.assertEqual(len(WebEvent.db_types()), len(event.to_tuple()))
