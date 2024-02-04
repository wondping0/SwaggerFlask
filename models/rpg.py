from extensions import db

class Item(db.Document):
    name = db.StringField(required=True, unique=True)
    price = db.FloatField(required=True)

class Skill(db.Document):
    name = db.StringField(required=True, unique=True)
    damage = db.FloatField(required=True)

class Gear(db.Document):
    name = db.StringField(required=True, unique=True)
    defense = db.FloatField(required=True)

class UserProfile(db.Document):
    user = db.ReferenceField('User', unique=True)
    inventory = db.ListField(db.ReferenceField('Item'))
    skills = db.ListField(db.ReferenceField('Skill'))
    gears = db.ListField(db.ReferenceField('Gear'))
    balance = db.FloatField(default=0)

class AdminProfile(db.Document):
    user = db.ReferenceField('User', unique=True)
    created_items = db.ListField(db.ReferenceField('Item'))
    sold_items = db.ListField(db.ReferenceField('Item'))
