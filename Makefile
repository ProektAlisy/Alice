WORKDIR = ./app
MANAGE = python $(WORKDIR)/manage.py

style:
	black -S -l 79 $(WORKDIR)
	isort $(WORKDIR)
	isort ./tests
	flake8 $(WORKDIR)
	flake8 ./tests
