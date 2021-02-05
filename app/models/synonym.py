from app import db
from app.models.default import Base


class Synonym(Base):
    title = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Synonyms %r>' % self.title
