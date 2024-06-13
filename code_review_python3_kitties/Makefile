setup-env:
	pip3 install pipenv
	pipenv install

run:
	pipenv run python -m kitties.viewer $(flags)

help:
	pipenv run python -m kitties.viewer --help

test:
	pipenv run python -m unittest $(tests)

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*~' -delete
