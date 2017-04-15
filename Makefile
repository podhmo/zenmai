readme:
	rm -f README.rst
	cat misc/_README.header.rst > README.rst
	python misc/bin/readme.py >> README.rst

