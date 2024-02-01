# login_helpers.py
# Support code for login checking
#
# DO NOT MODIFY THIS FILE--it will be replaced by the autograder
#

import os
import sys
import pathlib
import argparse
import subprocess

this_path = pathlib.Path(os.path.realpath(__file__)).parent
problem_dir = (this_path / "..").resolve()

LOGIN_PROGRAM = problem_dir / "login"
LOGIN_RV_SUCCESS = 0
LOGIN_RV_FAIL = 2


def load_secrets(secrets_file) -> dict[str, str]:
    user_db = {}
    with open(secrets_file, "r") as secrets_fd:
        for line in secrets_fd:
            line = line.strip()
            if not line:
                break

            user, password = line.split(" ")
            user_db[user] = password

    return user_db


def try_login(db_file, username, password, expected_rv=LOGIN_RV_SUCCESS):
    cmd = [LOGIN_PROGRAM, db_file,
           username, password]

    proc = subprocess.run(cmd, encoding="utf-8",
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if proc.returncode != expected_rv:
        raise ValueError(f"Login attempt for user {username} failed (tried password {password}, expected return value {expected_rv}), login returned {proc.returncode}\nOutput:  {proc.stdout}")

    return proc.returncode


def check_database(db_file, secrets_file, verbose=False):

    secrets = load_secrets(secrets_file)

    ok = True
    # First, try all of the correct logins
    for username, password in secrets.items():
        rv = try_login(db_file, username, password)

        if verbose:
            print("Logging in as {} => {}"
                  .format(username, "OK" if rv == 0 else "FAIL"))

        if rv != LOGIN_RV_SUCCESS:
            ok = False
            break

    if not ok:
        return

    # Next, try some incorrect logins
    if len(secrets) == 0:
        return

    orig_user, orig_pass = list(secrets.items())[0]
    try_login(db_file, orig_user, orig_pass[::-1], expected_rv=LOGIN_RV_FAIL)
    try_login(db_file, orig_user, "", expected_rv=LOGIN_RV_FAIL)

    # Try one user with another's password
    if len(secrets) > 1:
        another_user, another_pass = list(secrets.items())[1]
        try_login(db_file, orig_user, another_pass, expected_rv=LOGIN_RV_FAIL)
