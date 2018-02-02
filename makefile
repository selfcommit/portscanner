install: test
	sudo -H pip install .

clean:
	rm -rf .cache
	rm -rf .eggs
	rm -rf IPScanner.egg-info

dev:
	pip install --user .

test:
	python setup.py test

uninstall: clean
	sudo -H pip uninstall IPScanner -y