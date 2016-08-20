PYTHON := python3
APP_NAME := nasanomics
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
	rm -rf ./vps/vagrant/nasanomics
	vagrant destroy -f

venv: 
	virtualenv -p python3 $(VENV)

install: requirements.txt $(VENV)
	pip3 install -r requirements.txt

dev-deploy:
	mkdir ./vps/vagrant/$(APP_NAME)
	git clone https://github.com/withtwoemms/$(APP_NAME).git ./vps/vagrant/$(APP_NAME)
	cp ./.env ./vps/vagrant/$(APP_NAME)
	vagrant up
	

.PHONY: all test venv
