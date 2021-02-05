from app import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    date_created = db.Column(
        db.DateTime,
        default=db.func.now()
    )
    date_modified = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now()
    )
