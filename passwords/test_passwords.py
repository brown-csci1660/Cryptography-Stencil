import os
import sys
import pathlib
import unittest
import subprocess

from dataclasses import dataclass

import support.database_helpers as db
import support.login_helpers as login

this_path = pathlib.Path(os.path.realpath(__file__)).parent
problem_dir = this_path.resolve()

DB_DIR = pathlib.Path(problem_dir / "db")
WORK_DIR = pathlib.Path(problem_dir / "tmp")

PWFIND_PATH = problem_dir / "pwfind"

@dataclass
class Result():
    user: str
    expected_pass: str
    found_pass: str
    ok: bool


class PasswordsTest(unittest.TestCase):

    def setUp(self):
        if not WORK_DIR.exists():
            os.mkdir(str(WORK_DIR))

    def test_demo_plain_login(self):
        """
        Try to log in using the plain method.  This is a basic setup
        test to prove the test infrastructure is working--it should
        work with no changes to the stencil.
        """
        db_file, secrets_file = self.use_db("demo")

        login.check_database(db_file, secrets_file)

    def test_demo_plain_pwfind(self):
        """
        Try to find the password using the plain method.  This is a basic setup
        test to prove the test infrastructure is working--it should
        work with no changes to the stencil.
        """
        db_file, secrets_file = self.use_db("demo")
        self.run_check_pwfind(db_file, secrets_file)

    def test_part1_sha1_nosalt_login(self):
        """
        Test login using a database created using the sha1-nosalt method
        """
        db_file, secrets_file = self.use_db("part1")
        login.check_database(db_file, secrets_file)

    def test_part1_sha1_nosalt_pwfind_single(self):
        """
        Find the password on a database with 1 user stored with the sha1-nosalt method
        """
        db_file, secrets_file = self.use_db("part1")
        self.run_check_pwfind(db_file, secrets_file)

    def test_part2_sha1_nosalt_pwfind_many(self):
        """
        Find the passwords of 1000 users in a database stored with the sha1-nosalt method

        This test should not take substantially longer than test04.
        If you find it is taking an extremely long time, you should
        rethink your strategy.
        """
        db_file, secrets_file = self.use_db("part2")
        self.run_check_pwfind(db_file, secrets_file)

    def test_part3_sha1_salt4_login(self):
        """
        Test login using a database created using the sha1-salt4 method
        """
        db_file, secrets_file = self.use_db("part3")
        login.check_database(db_file, secrets_file)

    def test_part3_sha1_salt4_pwfind(self):
        """
        Find the password on a database with 4 users stored with the sha1-salt4 method.
        This may take a few minutes, depending on the CPU speed of your system.
        """
        db_file, secrets_file = self.use_db("part3")
        self.run_check_pwfind(db_file, secrets_file)

    # ######## Utility methods for tests #########
    def _name(self):
        return self.id().split(".")[-1]

    def use_db(self, key):
        db_file = DB_DIR / "{}.db.json".format(key)
        secrets_file = DB_DIR / "{}.secrets.txt".format(key)

        def _check(filename, s):
            if not filename.exists():
                raise ValueError(f"Unable to find {s} at {filename.relative_to(problem_dir)}.  Try regenerating your databases.")

        _check(db_file, "database file")
        _check(secrets_file, "secrets file")

        return db_file, secrets_file

    def make_db(self, method, users):
        db_file = WORK_DIR / "{}.db.json".format(self._name())
        secrets_file = WORK_DIR / "{}.secrets.txt".format(self._name())
        jd, secrets = db.build_database(method, users,
                                        database_file=db_file,
                                        secrets_file=secrets_file,
                                        write=True)

    def run_pwfind(self, db_file, output_file):
        cmd = [str(PWFIND_PATH), str(db_file), str(output_file)]

        proc = subprocess.run(cmd, encoding="utf-8",
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if proc.returncode != 0:
            raise ValueError(f"pwfind exited unexpectedly with return value {proc.returncode}\nOutput:  {proc.stdout}")

        if not output_file.exists():
            raise ValueError(f"Output file {output_file} not found, make sure your results are written to file")

        try:
            pwfind_results = login.load_secrets(output_file)
        except Exception as e:
            raise ValueError(f"Error parsing pwfind output at {output_file}") from e

        return pwfind_results

    def check_pwfind(self, secrets_file, pwfind_results) -> tuple[list[Result], bool]:
        secrets = login.load_secrets(secrets_file)
        pw_results = []
        test_is_pass = True

        for expected_user, expected_password in secrets.items():
            if expected_user not in pwfind_results:
                pw_results.append(Result(expected_user, expected_password, "MISSING", False))
                test_is_pass = False

            found_password = pwfind_results[expected_user]
            ok = expected_password == found_password
            if not ok:
                test_is_pass = False

            pw_results.append(Result(expected_user, expected_password, found_password, ok))

        return pw_results, test_is_pass

    def run_check_pwfind(self, db_file, secrets_file):
        output_file = WORK_DIR / "{}.pwfind.txt".format(self._name())

        pwfind_dict = self.run_pwfind(db_file, output_file)
        pwfind_results, pwfind_results_ok = self.check_pwfind(secrets_file, pwfind_dict)
        if not pwfind_results_ok:
            print("======================================================")
            print("One or more passwords was incorrect, see results below")
            self.print_pwfind_results(pwfind_results)
            print("For the set of inputs used in this test, see the following files")
            print(f"Database file:  {db_file.relative_to(problem_dir)}")
            print(f"Secrets file (expected passwords):  {db_file.relative_to(problem_dir)}")
            print(f"pwfind output file:  {output_file.relative_to(problem_dir)}")
            print("======================================================")

        self.assertTrue(pwfind_results_ok)

    def print_pwfind_results(self, results):
        fmt = "{:>8} {:>8} {:>8} {:>4}"
        print(fmt.format("User", "Expected", "pwfind", "Result"))
        for r in results:
            print(fmt.format(r.user, r.expected_pass, r.found_pass, "OK" if r.ok else "FAIL"))


