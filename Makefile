tarball:	clean
	python setup.py sdist
	mv dist/daemonize-*.tar.gz .
	rm -rf dist daemonize.egg-info

clean:
	rm -rf daemonize-*.tar.gz
