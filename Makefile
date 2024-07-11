install:
	pip install -r requirements.txt

test:
	python -m pytest -vv unit_test/test.py 

format:
	black *.py

lint:
	pylint --disable=R,C *.py 

all: install lint format test 

