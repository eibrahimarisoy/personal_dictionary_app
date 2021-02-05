import os
basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):
    def __init__(self):
        self.DEBUG = True
        self.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'my_app.db') 
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.SECRET_KEY = "flask-todo"
        self.URL = "https://wordsapiv1.p.rapidapi.com/words/"
        self.HEADERS = {
            "x-rapidapi-key" : "YOUR_API_KEY",
            "x-rapidapi-host" : "wordsapiv1.p.rapidapi.com"
        }


ENV = os.getenv('ENVIRONMENT', 'Local')
configuration = DefaultConfig()
