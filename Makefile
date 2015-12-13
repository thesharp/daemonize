all: clean sdist wheel

clean:
	rm -rf dist daemonize.egg-info

sdist:
	python setup.py sdist

wheel:
	python setup.py bdist_wheel

upload:
	python setup.py upload
