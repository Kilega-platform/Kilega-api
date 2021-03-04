from config import db_connection


class Hymns():
    """This class contains functionality for dealing with songs
    Attributes:
    """

    def __init__(self, lang):
        """ initialize """
        self.lang = lang.lower()

    def get_all_hymns(self):
        """ get all songs from the songs collection """
        db = db_connection.connect_mongo()
        query = {"lang": {"$eq": self.lang}}
        projection = {"_id": 0, "song_number": 1,
                      "verses": 1, "category": 1, "title": 1, "lang": 1}
        results = list(db.hymns.find(query, projection))
        return results
