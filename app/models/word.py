from app import db
from app.models.default import Base


class Word(Base):
    title = db.Column(db.String(255))
    definitions = db.relationship(
        'Definition',
        backref='Word',
        lazy=True
    )
    user_dict = db.relationship(
        'UserDict',
        backref="Word",
        lazy=True
    )

    def __repr__(self):
        return '<Word %r>' % self.title
