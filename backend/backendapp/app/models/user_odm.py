from mongoengine import Document, SequenceField, StringField, EmailField, ListField, ReferenceField, IntField
from mongoengine.queryset.manager import QuerySetManager

from .problem_odm import Problem

class User(Document):
    objects: QuerySetManager

    id = SequenceField(primary_key=True)
    name = StringField(max_length=255, required=True, unique=True)
    email = EmailField(required=True, unique=True)
    hashed_password = StringField(max_length=128, required=True)
    ac_problems = ListField(ReferenceField(Problem))
    status = IntField(default=0) # 0 -> administrator, 1 -> verified, 2 -> banned, 3 -> banned
