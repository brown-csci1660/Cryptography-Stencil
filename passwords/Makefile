PYTHON = python3

GENERATE = ./create_database
LOGIN = ./login
FINDPW = ./findpw

.PHONY: generate

generate:
	$(GENERATE) --method plain --users 10 --secrets demo.secrets.txt demo.db.json
	$(GENERATE) --method sha1-nosalt --users 1 --secrets part1.secrets.txt part1.db.json
	$(GENERATE) --method sha1-nosalt --users 100 --secrets part2.secrets.txt part2.db.json
	$(GENERATE) --method sha1-salt4 --users 4 --secrets part3.secrets.txt part3.db.json

check:
	$(PYTHON) -m unittest test_passwords.py -v

clean-env:
	rm -rf __pycache__
	rm -rf .pytest_cache
	@echo "Environment cleared.  Run 'make setup' again to create it."

