from .database import Database

def clean_database(settings_file, database_name):
    """
    Calls the database.clean() method on the given database. Sets all running calculations back to pending.
        
    """

    with Database(database_name) as database:

        database.clean()
