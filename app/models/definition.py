from app import db
from app.models.default import Base


synonyms = db.Table(
    'definition_synonyms',
    db.Column(
        'synonym_id',
        db.Integer,
        db.ForeignKey('synonym.id'),
        primary_key=True
    ),
    db.Column(
        'definition_id',
        db.Integer,
        db.ForeignKey('definition.id'),
        primary_key=True
    )
)


class Definition(Base):
    content = db.Column(db.String(255))
    part_of_speech = db.Column(db.String(255))
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    synonyms = db.relationship(
        'Synonym',
        secondary=synonyms,
        lazy='subquery',
        backref=db.backref(
            'definitions',
            lazy=True
            )
    )

    def __repr__(self):
        return '<Definition %r>' % self.content
