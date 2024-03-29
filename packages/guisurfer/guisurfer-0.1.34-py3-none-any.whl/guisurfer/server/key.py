from dataclasses import dataclass, field
from typing import List, Optional, Dict
import uuid
import time
import os
import base64
import json
import io

import paramiko
from cryptography.fernet import Fernet

from guisurfer.db.models import SSHKeyRecord
from guisurfer.db.conn import WithDB
from .models import SSHKeyModel


@dataclass
class SSHKeyPair(WithDB):
    """An SSH key"""

    name: str
    public_key: str
    private_key: str
    owner_id: str
    created: float = field(default_factory=lambda: time.time())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.private_key = self.encrypt_private_key(self.private_key)
        self.save()

    @classmethod
    def get_encryption_key(cls) -> bytes:
        return os.environ["ENCRYPTION_KEY"].encode()

    def encrypt_private_key(self, private_key: str) -> str:
        key = self.get_encryption_key()
        fernet = Fernet(key)
        encrypted_private_key = fernet.encrypt(private_key.encode())
        return base64.b64encode(encrypted_private_key).decode()

    @classmethod
    def decrypt_private_key(cls, encrypted_private_key: str) -> str:
        key = cls.get_encryption_key()
        fernet = Fernet(key)
        decrypted_private_key = fernet.decrypt(base64.b64decode(encrypted_private_key))
        return decrypted_private_key.decode()

    @classmethod
    def generate_key(
        cls,
        name: str,
        owner_id: str,
        passphrase: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> "SSHKeyPair":
        """
        Generates a new SSH key pair using Paramiko. Encrypts the private key with a passphrase if provided.
        Returns an instance of SSHKey with the encrypted private key and public key.
        """
        key = paramiko.RSAKey.generate(2048)
        private_key_io = io.StringIO()
        key.write_private_key(private_key_io, password=passphrase)
        private_key = private_key_io.getvalue()
        public_key = f"{key.get_name()} {key.get_base64()}"

        return cls(
            name=name,
            owner_id=owner_id,
            public_key=public_key,
            private_key=private_key,
            metadata=metadata or {},
        )

    def to_record(self) -> SSHKeyRecord:
        return SSHKeyRecord(
            id=self.id,
            owner_id=self.owner_id,
            name=self.name,
            public_key=self.public_key,
            private_key=self.private_key,
            created=self.created,
            metadata_=json.dumps(self.metadata),
            full_name=f"{self.owner_id}/{self.name}",
        )

    @classmethod
    def from_record(cls, record: SSHKeyRecord) -> "SSHKeyPair":
        obj = cls.__new__(cls)
        obj.id = record.id
        obj.public_key = record.public_key
        obj.private_key = record.private_key
        obj.name = record.name
        obj.created = record.created
        obj.owner_id = record.owner_id
        obj.metadata = json.loads(record.metadata_)
        return obj

    def save(self) -> None:
        for db in self.get_db():
            db.merge(self.to_record())
            db.commit()

    @classmethod
    def find(cls, **kwargs) -> List["SSHKeyPair"]:
        for db in cls.get_db():
            records = db.query(SSHKeyRecord).filter_by(**kwargs).all()
            return [cls.from_record(record) for record in records]

    @classmethod
    def delete(cls, name: str, owner_id: str) -> None:
        for db in cls.get_db():
            record = (
                db.query(SSHKeyRecord).filter_by(name=name, owner_id=owner_id).first()
            )
            if record:
                db.delete(record)
                db.commit()

    def to_schema(self) -> SSHKeyModel:
        return SSHKeyModel(
            id=self.id,
            public_key=self.public_key,
            name=self.name,
            created=self.created,
            private_key=self.decrypt_private_key(self.private_key),
        )
