import os


class DefaultConfig(object):
    def __init__(self):
        self.DEBUG = True
        self.SQLALCHEMY_DATABASE_URI = 'sqlite://///home/emre/Documents/calismalar/moneytolia/dict_memo_app/my_app.db' 
        self.DATABASE_CONNECT_OPTIONS = {}
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.SECRET_KEY = "flask-todo"
        self.URL = "https://wordsapiv1.p.rapidapi.com/words/"
        self.HEADERS = {
            "x-rapidapi-key" : "ea984abe36mshc37249eb762f7eep168c23jsn27f2181447c3",
            "x-rapidapi-host" : "wordsapiv1.p.rapidapi.com"
        }


ENV = os.getenv('ENVIRONMENT', 'Local')
configuration = DefaultConfig()