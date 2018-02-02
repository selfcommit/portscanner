install:
	sudo -H pip install --user .

clean:
	rm -rf .cache
	rm -rf .eggs
	rm -rf IPScanner.egg-info

dev:
	pip3 install --user .

test:
	python setup.py test

uninstall: clean
	sudo -H pip uninstall IPScanner -y