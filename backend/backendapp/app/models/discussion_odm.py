from mongoengine import Document, SequenceField, ReferenceField, StringField, ListField
from mongoengine.queryset.manager import QuerySetManager

from .user_odm import User
from .problem_odm import Problem

class Discussion(Document):
    objects: QuerySetManager

    id = SequenceField(primary_key=True)
    user = ReferenceField(User, required=True)
    problem = ReferenceField(Problem, required=True)
    content = StringField(required=True)
    like_by = ListField(ReferenceField(User))
