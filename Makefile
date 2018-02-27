
all: venv install

venv:
	python3 -m venv venv

.PHONY: tests
tests:  venv
	nosetests -v tests 

.PHONY: run
run: venv
	FLASK_DEBUG=1 FLASK_APP=chargehound-demo.py flask run

install:
	echo "Installing packages from requirements.txt"
	venv/bin/pip install -r requirements.txt

clean:
	rm *.pyc