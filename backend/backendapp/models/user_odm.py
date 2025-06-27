from mongoengine import Document, SequenceField, StringField, EmailField, ListField
from mongoengine.queryset.manager import QuerySetManager

class User(Document):
    objects: QuerySetManager

    id = SequenceField(primary_key=True)
    name = StringField(max_length=255, required=True)
    email = EmailField(required=True, unique=True)
    hashed_password = StringField(max_length=128, required=True)
    ac_problems = ListField(IntField())
