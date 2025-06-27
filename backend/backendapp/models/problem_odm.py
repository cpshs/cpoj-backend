from mongoengine import IntField, DictField

class Problem(Document):
    objects: QuerySetManager

    id = SequenceField(primary_key=True)
    title = StringField(max_length=255, required=True)
    statement = StringField(required=True)
    template = StringField()
    judge_script = StringField()
    judge_method = StringField(max_length=255, required=True)
    ac_number = IntField(default=0)
    submission_number = IntField(default=0)
	status = IntField(default=0)
