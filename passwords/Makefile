PYTHON = python3

GENERATE = ./create_database
LOGIN = ./login
FINDPW = ./findpw
DB_DIR = db

.PHONY: generate

generate:
	mkdir -p $(DB_DIR)
	$(GENERATE) --method plain --users 10 --secrets $(DB_DIR)/demo.secrets.txt $(DB_DIR)/demo.db.json
	$(GENERATE) --method sha1-nosalt --users 1 --secrets $(DB_DIR)/part1.secrets.txt $(DB_DIR)/part1.db.json
	$(GENERATE) --method sha1-nosalt --users 1000 --secrets $(DB_DIR)/part2.secrets.txt $(DB_DIR)/part2.db.json
	$(GENERATE) --method sha1-salt4 --users 4 --secrets $(DB_DIR)/part3.secrets.txt $(DB_DIR)/part3.db.json

check:
	$(PYTHON) -m unittest test_passwords.py -v

check-setup:
	$(PYTHON) -m unittest test_passwords.py -vf -k 'test_passwords.PasswordsTest.test_plain*'

check-part1:
	$(PYTHON) -m unittest test_passwords.py -vf -k 'test_passwords.PasswordsTest.test_part1*'

check-part2:
	$(PYTHON) -m unittest test_passwords.py -vf -k 'test_passwords.PasswordsTest.test_part2*'

check-part3:
	$(PYTHON) -m unittest test_passwords.py -vf -k 'test_passwords.PasswordsTest.test_part3*'


clean-env:
	rm -rf __pycache__
	rm -rf .pytest_cache
	@echo "Environment cleared.  Run 'make setup' again to create it."

