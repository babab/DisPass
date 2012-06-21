MAN_PATH	= /usr/share/man/man1
VERSION		= 0.1a7

make:
	@echo make install
	@echo make uninstall
	@echo
	@echo make doc
	@echo make dist
	@echo make clean

rm_pyc:
	find . -name "*.pyc" | xargs /bin/rm -f

doc_clean: rm_pyc
	cd sphinx-doc/root/; make clean
	cd sphinx-doc/en/; make clean
	#cd sphinx-doc/nl/; make clean

doc: doc_clean
	cd sphinx-doc/root/; make html
	cd sphinx-doc/en/; make html
	#cd sphinx-doc/nl/; make html
	rm -rf doc/html
	mkdir -p doc
	mv sphinx-doc/root/_build/html doc/html
	mkdir -p doc/html/$(VERSION)
	mv sphinx-doc/en/_build/html doc/html/$(VERSION)/en
	#mv sphinx-doc/nl/_build/html doc/html/$(VERSION)/nl
	make doc_clean

man: rm_pyc
	cd sphinx-doc/man-en/; make clean
	cd sphinx-doc/man-en/; make man
	mv sphinx-doc/man-en/_build/man/dispass.1 .
	cd sphinx-doc/man-en/; make clean

dist: rm_pyc
	python setup.py sdist

install: dist
	pip install --upgrade dist/DisPass-$(VERSION).tar.gz
	gzip -c dispass.1 > dispass.1.gz
	mv dispass.1.gz $(MAN_PATH)/
	make clean

uninstall: clean
	pip uninstall dispass

clean: doc_clean
	rm -f MANIFEST dispass.1.gz
	rm -rf dist doc

# vim: set noet ts=8 sw=8 sts=8:
