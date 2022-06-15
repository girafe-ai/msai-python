from datetime import datetime

import peewee
import peewee_async
from playhouse.postgres_ext import JSONField


database = peewee_async.PostgresqlDatabase('tagger_gate')


class BaseModel(peewee.Model):
    class Meta:
        database = database


class User(BaseModel):
    name = peewee.CharField()
    api_key = peewee.CharField()
    active = peewee.BooleanField(default=True)


class Query(BaseModel):
    user = peewee.ForeignKeyField(User)
    timestamp = peewee.DateTimeField(default=datetime.now)
    request = JSONField()
    response = JSONField()


database.create_tables((User, Query), safe=True)
manager = peewee_async.Manager(database)
database.set_allow_sync(False)


async def fill_with_test_data():
    user1 = await manager.create(User, name='user1', api_key='e721y87e30')
    user2 = await manager.create(User, name='user2', api_key='hd3f238u42')
    await manager.create(Query, user=user1, request={'a': 1}, response={'b': 1})
    await manager.create(Query, user=user1, request={'a': 2}, response={'b': 2})
    await manager.create(Query, user=user2, request={'a': 3}, response={'b': 3})
    await manager.create(Query, user=user2, request={'a': 4}, response={'b': 4})


def migrate():
    from peewee_migrate import Router

    with manager.allow_sync():
        router = Router(database, migrate_dir='migrations')
        router.run()


def init_db():
    migrate()
