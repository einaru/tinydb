from datetime import datetime

from tinydb import TinyDB, where
from tinydb.middlewares import SerializationMiddleware
from tinydb.serialize import Serializer
from tinydb.storages import MemoryStorage


class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime
    FORMAT = '%Y-%m-%dT%H:%M:%S'

    def encode(self, obj):
        return obj.strftime(self.FORMAT)

    def decode(self, s):
        return datetime.strptime(s, self.FORMAT)


def test_serializer():
    serializer = SerializationMiddleware(MemoryStorage)
    serializer.register_serializer(DateTimeSerializer(), 'TinyDate')
    db = TinyDB(storage=serializer)

    date = datetime(2000, 1, 1, 12, 0, 0)

    db.insert({'date': date})
    assert db.count(where('date') == date) == 1