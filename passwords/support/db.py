import json

# TODO:  Need to store the password in another way for grading
PLAINTEXT_PASSWORD_KEY = "__plaintext_for_internal_use_only"


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

    def _get_pw(self, username: str):
        user_info = self._get_user(username)
        return user_info[PLAINTEXT_PASSWORD_KEY]

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
