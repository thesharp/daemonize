all: clean upload

clean:
	rm -rf dist daemonize.egg-info

upload:
	python setup.py sdist bdist_wheel
	twine upload dist/*

docs:
	sphinx-build -b html docs docs/_build
