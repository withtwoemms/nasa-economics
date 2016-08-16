PYTHON := python3
APP_FILE := app/nasanomics.py
TEST_FILES := $(shell ls test/*_test.py)
VENV := $(CURDIR)/venv


$(eval export PYTHONPATH=${PYTHONPATH}:./)
$(eval export FLASK_APP=$(APP_FILE))
$(foreach envvar, \
     $(shell cat $(CURDIR)/.env), \
     $(eval export $(envvar)))

all: 
	@echo "FLASK APP -->" ${FLASK_APP}
	@echo "FLASK ENV -->" ${FLASK_APP_ENV}

test:
	$(eval export FLASK_APP_ENV=test)
	@echo "CURRENT_ENV -->" ${FLASK_APP_ENV}
	@echo "TEST FILES -->" ${TEST_FILES}
	for file in $(TEST_FILES); do $(PYTHON) $$file; done

shell:
	$(eval export FLASK_APP_ENV=dev)
	@echo "CURRENT_ENV -->" ${FLASK_APP_ENV}
	$(PYTHON)

dev-server:
	$(eval export FLASK_APP_ENV=dev)
	@echo "CURRENT_ENV -->" ${FLASK_APP_ENV}
	$(PYTHON) ${FLASK_APP}

clean:
	rm -rf $(VENV)
	find . -iname '*.pyc' -exec rm {} \;

venv: 
	virtualenv -p python3 $(VENV)

install: requirements.txt $(VENV)
	pip install -r requirements.txt
	

.PHONY: all test

