from app import db
from app.models.default import Base
from werkzeug.security import check_password_hash, generate_password_hash

words = db.Table('user_words', db.Column(
        'word_id',
        db.Integer,
        db.ForeignKey('word.id'),
        primary_key=True),
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True)
)


class User(Base):
    username = db.Column(
        db.String(150),
        nullable=False
    )
    password = db.Column(
        db.String(150),
        nullable=False
    )
    words = db.relationship(
        'Word',
        secondary=words,
        lazy='dynamic',
        backref=db.backref(
            'users',
            lazy=True,
            uselist=False)
    )
    can_practice = db.Column(
        db.Boolean,
        default=False
    )
    user_dict = db.relationship(
        'UserDict',
        backref="User",
        lazy=True
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username
