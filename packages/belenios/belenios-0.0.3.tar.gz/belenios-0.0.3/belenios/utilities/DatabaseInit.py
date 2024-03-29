from sqlalchemy.orm.exc import NoResultFound

from belenios.custom_types.command_line.RoleType import RoleType
from belenios.models.command_line.UserModel import UserModel
from belenios.utilities.Utility import Utility


class DatabaseInit():
    def run(self, session):
        self._create_users(session)

    def _create_users(self, session):
        a = [
            UserModel(username='admin', password_hash=Utility.hash_sha256_as_hex('admin'.encode()), role=RoleType.ServerAdministrator),
            UserModel(username='cred', password_hash=Utility.hash_sha256_as_hex('credd'.encode()), role=RoleType.CredentialAuthority),
            UserModel(username='trustee1', password_hash=Utility.hash_sha256_as_hex('trustee1'.encode()), role=RoleType.Trustee),
            UserModel(username='trustee2', password_hash=Utility.hash_sha256_as_hex('trustee2'.encode()), role=RoleType.Trustee),
            UserModel(username='trustee3', password_hash=Utility.hash_sha256_as_hex('trustee3'.encode()), role=RoleType.Trustee),
        ]
        for u in a:
            # Check if the example account exists in the database
            try:
                existing_user = session.query(UserModel).filter_by(username=u.username).one()
            except NoResultFound:
                # If the account doesn't exist, create it
                session.add(u)
        session.commit()
