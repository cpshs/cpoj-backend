from mongoengine import ReferenceField

class Discussion(Document):
    objects: QuerySetManager

    id = SequenceField(primary_key=True)
    user = ReferenceField(User, required=True)
    problem = ReferenceField(Problem, required=True)
    content = StringField(required=True)
    like_by = ListField(ReferenceField(User))
