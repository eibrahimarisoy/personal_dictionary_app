from flask import Flask
from config import configuration
from flask_bootstrap import Bootstrap
from flask import session, g
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder='templates')
app.config.from_object(__name__)
app.config.update(configuration.__dict__)
db = SQLAlchemy(app)
Bootstrap(app)

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.filter(User.id == session["user_id"]).first()


@app.after_request
def after_request(response):
    return response


from app.models.default import Base
from app.models.user import User
from app.models.word import Word
from app.models.definition import Definition
from app.models.synonym import Synonym
from app.models.user_dict import UserDict

db.create_all()
db.session.commit()


from app.modules.user.views import module as user
from app.modules.word.views import module as word

app.register_blueprint(user)
app.register_blueprint(word)