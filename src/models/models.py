from src.models.frequent_words import create as frequent_words_create
from src.models.paragraph import create as paragraph_words_create


def pgdb_migration(engine):
    frequent_words_create(engine)
    paragraph_words_create(engine)
