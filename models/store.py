from db import db


class StoreModel(db.Model): # Extends db model

    # Telling SQLAlchemy about our tables and columns
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # Back reference to items table.
    # Relationship: many items to one store.
    # Here we got a list of ItemModels.
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    # cls = reference to the class
    @classmethod
    def find_by_name(cls, name):
        # SELECT * FROM __tablename__ WHERE name = name(method_arg) LIMIT 1
        # using SQLAlchemy query builder and filter and return ItemModel object
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()