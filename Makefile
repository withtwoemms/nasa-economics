PYTHON := python3
APP_FILE := meteor.py
TEST_FILE := meteor_test.py


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
	$(PYTHON) $(TEST_FILE)

dev:
	$(eval export FLASK_APP_ENV=dev)
	@echo "CURRENT_ENV -->" ${FLASK_APP_ENV}
	$(PYTHON)

dev-server:
	$(eval export FLASK_APP_ENV=dev)
	@echo "CURRENT_ENV -->" ${FLASK_APP_ENV}
	$(PYTHON) ${FLASK_APP}

.PHONY: all test

