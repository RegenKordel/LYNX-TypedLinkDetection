"""
created at: 2018-12-11
author: Volodymyr Biryuk

<module comment>
"""
import configparser
import logging
from export import util
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure, NetworkTimeout, OperationFailure, \
    ConfigurationError
from pymongo.auth import MECHANISMS

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class MongoDBConnection:
    """A connector object for MongoDB"""

    def __init__(self, host: str, port: int, username: str = None,
                 password: str = None, auth_source: str = None,
                 auth_mechanism: str = None, connect_timeout: int = 30000):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.auth_source = auth_source
        self.auth_mechanism = auth_mechanism
        self.connect_timeout = connect_timeout
        self.client = self.__connect()

    def __connect(self) -> MongoClient:
        logger.debug(f'Connecting to database with settings:')
        logger.debug(f'{self.__dict__}')
        try:
            if self.auth_mechanism:
                client = MongoClient(host=self.host,
                                     port=self.port,
                                     username=self.username,
                                     password=self.password,
                                     authSource=self.auth_source,
                                     authMechanism=self.auth_mechanism,
                                     serverSelectionTimeoutMS=self.connect_timeout)
            else:
                client = MongoClient(host=self.host,
                                     port=self.port,
                                     serverSelectionTimeoutMS=self.connect_timeout)
            logger.debug(client.server_info())
            try:
                # Check if admin
                logger.debug(client.list_database_names())
                logger.debug(client['admin'].collection_names())
                logger.debug('Connected as admin')
            except OperationFailure:
                logger.info('Connected as user')
        except OperationFailure as e:
            logger.error(e)
            raise e
        except NetworkTimeout as e:
            logger.error(e)
            raise e
        except ServerSelectionTimeoutError as e:
            logger.error('Server selection timed out.')
            raise e
        except ConnectionFailure as e:
            logger.error(e)
            raise e
        except ConfigurationError as e:
            # when username but no password given
            logger.error(e)
            raise e
        except Exception as e:
            # Generic case if none of the above triggers
            logger.error(f"Unexpected Exception: {e}")
            raise e
        return client


def get_client():
    """Connect to the database with the predefined configurations from the config file and return the client."""
    host = config.get('DB', 'HOST')
    port = config.get('DB', 'PORT')
    user = config.get('DB', 'USER') if config.get('DB', 'USER') else None
    password = config.get('DB', 'PASSWORD') if config.get('DB', 'PASSWORD') else None
    auth_source = config.get('DB', 'AUTH_SOURCE')
    auth_mechanism = config.get('DB', 'AUTH_MECHANISM') if config.get('DB', 'AUTH_MECHANISM') else None
    client = MongoDBConnection(host=host, port=int(port),
                               username=user, password=password,
                               auth_source=auth_source, auth_mechanism=auth_mechanism).client
    return client


if __name__ == '__main__':
    pass
