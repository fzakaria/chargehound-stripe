
all: venv install

venv:
	python3 -m venv venv

.PHONY: tests
tests:  venv
	nosetests -v tests 

.PHONY: run
run: venv
	PUBLISHABLE_KEY=pk_test_WPIC5FsWhN3tZMu5Kpn9KWbT SECRET_KEY=sk_test_Rsuv0YBjzFWfgb8LYU0QNGwA FLASK_DEBUG=1 FLASK_APP=chargehound-demo.py flask run

install:
	echo "Installing packages from requirements.txt"
	venv/bin/pip install -r requirements.txt

clean:
	rm *.pyc