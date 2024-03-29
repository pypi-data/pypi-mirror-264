from cement.utils import fs
from sqlalchemy.orm import sessionmaker

from belenios.config.config import AppConfig
from belenios.models.BaseModel import BaseModel
from belenios.utilities.DatabaseInit import DatabaseInit
from belenios.utilities.command_line.AppObject import AppObject

from sqlalchemy import create_engine, MetaData, Table, text


class DbSession:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.session = self._connect_sqlalchemy()

    def _connect_sqlalchemy(self):
        engine = self._get_engine()

        # Generate model to create there tables
        # from belenios.models.belenios.SignedMsgModel import SignedMsgModel
        # from belenios.models.belenios.CertModel import CertModel
        # from belenios.models.belenios.CertKeysModel import CertKeysModel
        # from belenios.models.belenios.ChannelMsgModel import ChannelMsgModel
        # from belenios.models.belenios.EncryptedMsgModel import EncryptedMsgModel
        # from belenios.models.belenios.EventModel import EventModel
        # from belenios.models.belenios.HeaderModel import HeaderModel
        # from belenios.models.belenios.TrusteePublicKeyModel import TrusteePublicKeyModel

        # Create tables
        BaseModel.metadata.create_all(engine)

        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()

        DatabaseInit().run(session)
        return session

    def _get_engine(self):
        from belenios.main import BeleniosTest
        if isinstance(AppObject().app, BeleniosTest):
            db_file = fs.abspath(AppConfig().get_test_db_file())
        else:
            db_file = fs.abspath(AppConfig().get_prod_db_file())
        # print('SQLite database file is: %s' % db_file)

        # Create engine
        if db_file == '/default/absolute/path/prod.db' or db_file == '/default/absolute/path/test.db':
            raise Exception("db_file in the class AppConfig from the file config.py is not customized")
        return create_engine('sqlite:///' + db_file)

    def drop_all_tables(self):
        engine = self._get_engine()

        # Reflect the existing database schema
        metadata = MetaData()
        metadata.reflect(bind=engine)

        # Truncate or delete data from the table
        with engine.connect() as connection:
            # Iterate over each table in the database
            for table_name, table in metadata.tables.items():
                # Create a Table object
                t = Table(table_name, metadata, autoload=True, autoload_with=engine)
                # Truncate data from the table (if you want to keep the table structure)
                # connection.execute(t.delete())

                # Alternatively, delete the table itself (if you want to remove the table as well)
                sql_statement = f"DELETE FROM {table_name}"
                result_proxy = connection.execute(text(sql_statement))

            # Commit the changes
            connection.commit()
            # # Get the row count
            # row_count = result_proxy.rowcount
            # print(table_name, row_count)

            # Fetch all rows from the result set
            # rows = result.fetchall()
            engine.dispose()
    def force_initialize(self):
        self._initialize()