from datetime import datetime

from mongoengine import EmbeddedDocument, EmbeddedDocumentField, Document, SequenceField, BooleanField, IntField, DictField, StringField, ListField
from mongoengine.queryset.manager import QuerySetManager

class Testcase(EmbeddedDocument):
    hashed_input = StringField(max_length=64)
    hashed_answer = StringField(max_length=64)

class Subtask(EmbeddedDocument):
    testcases = ListField(EmbeddedDocumentField(Testcase))
    points = IntField(default=0)
    name = StringField(max_length=64)
    hidden = BooleanField()

class Template(EmbeddedDocument):
    language = StringField(max_length=64)
    content = StringField()

class Problem(Document):
    objects: QuerySetManager

    id = SequenceField(primary_key=True)
    title = StringField(max_length=255, required=True)
    statement = StringField(required=True)
    template = ListField(EmbeddedDocumentField(Template))
    judge_script = StringField()
    judge_method = StringField(max_length=255, required=True)
    ac_number = IntField(default=0)
    tags = ListField(StringField())
    submission_number = IntField(default=0)
    status = IntField(default=0)
    subtasks = ListField(EmbeddedDocumentField(Subtask))
    hidden = BooleanField(default=True)
