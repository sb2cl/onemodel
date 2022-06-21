VERSION := $(shell sed -n 's/^ *version.*=.*"\([^"]*\)".*/\1/p' pyproject.toml)
NAME := $(shell sed -n 's/^ *name.*=.*"\([^"]*\)".*/\1/p' pyproject.toml)

test:
	poetry run pytest

lint:
	poetry run nox -s lint

# Poetry does not place the NOTICE file inside the dist-info folder
# TODO: When poetry fixes this bug, we can remove the code for moving the NOTICE file.
build:
	rm -r dist
	poetry build
	cd dist; unzip $(NAME)-$(VERSION)-py3-none-any.whl
	mv dist/NOTICE dist/$(NAME)-$(VERSION).dist-info
	rm dist/$(NAME)-$(VERSION)-py3-none-any.whl
	cd dist; zip $(NAME)-$(VERSION)-py3-none-any.whl $(NAME)/* $(NAME)-$(VERSION).dist-info/*
	rm -r dist/$(NAME)
	rm -r dist/$(NAME)-$(VERSION).dist-info

clean:
	# Remove all .pyc and .pyo files as well as __pycache__ directories recursively starting from the current directory.
	find . | grep -E "(/__pycache__$$|\.pyc$$|\.pyo$$)" | xargs rm -rf

.PHONY: test lint clean build version
