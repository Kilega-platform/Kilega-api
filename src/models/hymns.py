from config import db_connection


class Hymns():
    """This class contains functionality for dealing with songs
    Attributes:
    """

    def __init__(self, lang):
        """ initialize """
        self.lang = lang

    def get_all_songs(self):
        """ get all songs from the songs collection """
        db = db_connection.connect_mongo(self.lang)
        results = list(db.hymns.find({}))
        return results
