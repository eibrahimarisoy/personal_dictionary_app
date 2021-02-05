from app import db
from app.models.default import Base


class UserDict(Base):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    search_count = db.Column(db.Integer, default=0)
    practice_point = db.Column(db.Integer, default=0)
    appearance_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User %r>' % self.username

    def appearance_count_update(self):
        self.appearance_count += 1
        db.session.add(self)
        db.session.commit()
