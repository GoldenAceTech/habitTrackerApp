from dataclasses import dataclass
from flask import Flask
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure


@dataclass
class InitDb:
    """A class to create mongodb connection, get a connection and test mongodb connection"""

    app: Flask

    def __post_init__(self) -> None:
        """Initialize mongo client connection and db"""
        mongo_uri = self.app.config["MONGO_URI"]
        self.__client = MongoClient(mongo_uri, tz_aware=True, serverSelectionTimeoutMS=5000)

    @property
    def client(self) -> MongoClient:
        """Get the mongo client

        Returns:
            MongoClient: A mongo client
        """
        return self.__client

    def get_db(self, db_str: str = None) -> Database | str:
        """Returns a database connection from the database name provided or an error message if mongo client has no server connection

        Args:
            db_str (str, optional): The database name. Defaults to None.

        Returns:
            Database | str: A Mongo Database if connection is available or error message string
        """
        client = self.client
        try:
            client.server_info()
            print("Database Server connection is available")
            db_name = db_str or self.app.config["DATABASE"]
            db = client[db_name]
            return db
        except ConnectionFailure:
            return "Server not available"
