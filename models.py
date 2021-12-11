from peewee import *
import datetime


DATABASE = SqliteDatabase('workouts.sqlite')


class User(Model):
    email = CharField()
    password = CharField()
    class Meta:
        database = DATABASE


class Workout(Model):
    name = CharField()
    # user = ForeignKeyField(User, backref='workouts')
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = DATABASE


class Lift(Model):
    name = CharField()
    start_weight = CharField()
    current_weight = CharField()
    sets = CharField()
    reps = CharField()
    personal_best = CharField()
    notes = CharField()
    # workout = ForeignKeyField(Workout, backref='lifts')
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Workout, Lift, User], safe=True)
    print('Connected to DB.')
    DATABASE.close()
