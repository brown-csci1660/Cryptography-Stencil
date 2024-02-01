# database_helpers.py
#
# Utility functions for generating and checking password databases.
# This file is used by the support and test scripts.
#
# DO NOT MODIFY THIS FILE--it will be replaced by the autograder.
#
#

import sys
import json
import string
import secrets
import argparse

import support.crypto as crypto  # See support/crypto.py for relevant cryptographic functions
import pwdb                      # See pwdb.py for useful constants helpers, can put shared code here

MAX_USERNAME_LENGTH = 4
NUM_USERS = 10

PASSWORD_LENGTH = 4
SALT_LENGTH = 4
PASSWORD_ALPHABET = string.ascii_lowercase + string.digits

METHOD_PLAIN = "plain"
METHOD_SHA1_NO_SALT = "sha1-nosalt"
METHOD_SHA1_SALT4 = "sha1-salt4"

METHODS = [
    METHOD_PLAIN,
    METHOD_SHA1_NO_SALT,
    METHOD_SHA1_SALT4,
]


class UsernameGenerator():

    def __init__(self):
        self.names_used = set()

    def generate(self):
        username = None
        while True:
            uid = "".join(secrets.choice(string.digits)
                          for i in range(MAX_USERNAME_LENGTH))
            username = "user{:04}".format(uid)
            if username not in self.names_used:
                break

        self.names_used.add(username)
        return username


class PasswordGenerator():

    def __init__(self, length, alphabet):
        self.length = length
        self.alphabet = alphabet

    def generate(self):
        password = "".join(secrets.choice(self.alphabet)
                           for _ in range(self.length))
        return password


class PasswordDatabase():

    def __init__(self, method, output_file):
        self.method = method
        self.output_file = output_file
        self.db = {}

    def users(self):
        return list(self.db.keys())

    def add_user(self, user: str, user_info):
        d = {}
        d.update(user_info)
        self.db[user] = d

        return "ok"

    def _get_user(self, username: str):
        if username not in self.db:
            raise ValueError("No such user")

        return self.db[username]

    def login(self, username: str, pw_entered: str):
        def _get(d, k):
            if k not in d:
                raise ValueError(f"Key {k} not found in {d}")
            return d[k]

        user_info = self._get_user(username)
        pw_found = _get(user_info, "password")

        if pw_found == pw_entered:
            return True
        else:
            return False

    def write(self):
        with open(self.output_file, "w") as fd:
            db_out = {
                "method": self.method,
                "users": self.db,
            }
            json.dump(db_out, fd,
                      indent=True, sort_keys=True)

    @classmethod
    def load_from_json(cls, db_file) -> 'PasswordDatabase':
        with open(db_file, "r") as json_fd:
            json_data = json.load(json_fd)
            assert "method" in json_data
            assert "users" in json_data

            method = json_data["method"]
            users = json_data["users"]

            db = cls(method, db_file)
            db.db = users
            return db


def build_database(method, users, database_file,
                   secrets_file=None, write=False):
    db = PasswordDatabase(method, database_file)
    user_gen = UsernameGenerator()
    pw_gen = PasswordGenerator(length=PASSWORD_LENGTH,
                               alphabet=PASSWORD_ALPHABET)

    secrets: dict[str, str] = {}

    for _ in range(0, users):
        username = user_gen.generate()
        password_cleartext = pw_gen.generate()
        to_store = {}

        secrets[username] = password_cleartext

        if method == METHOD_PLAIN:
            to_store["password"] = password_cleartext
        elif method == METHOD_SHA1_NO_SALT:
            pw_bytes = crypto.hash(password_cleartext.encode(encoding="utf-8"))
            to_store["password"] = pw_bytes.hex()
        elif method == pwdb.METHOD_SHA1_SALT4:
            salt_bytes = crypto.random_bytes(SALT_LENGTH)
            pw_bytes = crypto.hash(salt_bytes + password_cleartext.encode(encoding="utf-8"))
            to_store["password"] = pw_bytes.hex()
            to_store["salt"] = salt_bytes.hex()
        else:
            raise NotImplementedError(f"Unknown password storage method {method}")

        db.add_user(username, to_store)

    if write:
        db.write()

        if secrets_file:
            with open(secrets_file, "w") as out_fd:
                for user, pw_plain in secrets.items():
                    out_fd.write(f"{user} {pw_plain}\n")

    return db, secrets
