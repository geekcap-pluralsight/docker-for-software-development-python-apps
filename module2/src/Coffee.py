from db import db

class Coffee(db.Model):
    __tablename__ = 'coffee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    version = db.Column(db.Integer, nullable=False)

    def __init__(self, id, name, version):
        self.id = id
        self.name = name
        self.version = version

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version
        }
