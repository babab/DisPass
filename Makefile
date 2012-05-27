doc: clean
	cd sphinx-doc/en/; make html
	cd sphinx-doc/nl/; make html
	rm -rf doc
	mkdir -p doc
	mv sphinx-doc/en/_build/html doc/en
	mv sphinx-doc/nl/_build/html doc/nl
	make clean

clean:
	find . -name "*.pyc" | xargs /bin/rm -f
	cd sphinx-doc/en/; make clean
	cd sphinx-doc/nl/; make clean

# vim: set noet ts=8 sw=8 sts=8:
