from mongoengine import Document, SequenceField, StringField, ReferenceField, ListField
from mongoengine.queryset.manager import QuerySetManager

from .problem_odm import Problem

class RoadMap(Document):
    objects: QuerySetManager

    id = SequenceField(primary_key=True)
    topic = StringField(max_length=255, required=True)
    problems = ListField(ReferenceField(Problem))
    tutorials = ListField(StringField())
