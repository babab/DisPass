MAN_PATH		= $(DESTDIR)/usr/share/man/man1
ZSH_SITE_FUNCS_PATH	= $(DESTDIR)/usr/share/zsh/site-functions
PYTHON_EXEC		= python2
PIP_EXEC		= pip2

sinclude config.mk

VERSION		= 0.3.0

make:
	@echo "make install   Build and then install via pip and move manpage"
	@echo "make uninstall Clean build files and uninstall via pip"
	@echo
	@echo "Developer commands"
	@echo "make doc       Build html documentation with Sphinx"
	@echo "make man       Build manpage with Sphinx"
	@echo "make dist      Build python source archive file"
	@echo "make clean     Clean program build files"

rm_pyc:
	find . -name "*.pyc" | xargs /bin/rm -f

doc_clean: rm_pyc
	cd docs/en/; make clean
	#cd docs/nl/; make clean

doc: doc_clean
	cd docs/en/; make html
	cd docs/nl/; make html
	rm -rf doc/html/$(VERSION)
	mkdir -p doc/html/$(VERSION)
	mv docs/en/_build/html doc/html/$(VERSION)/en
	mv docs/nl/_build/html doc/html/$(VERSION)/nl
	make doc_clean

man: rm_pyc
	cd docs/man-en/; make clean
	cd docs/man-en/; make man
	mv docs/man-en/_build/man/dispass.1 .
	cd docs/man-en/; make clean

dist: rm_pyc
	$(PYTHON_EXEC) setup.py sdist

install: dist
	$(PIP_EXEC) install --root $(DESTDIR) --upgrade dist/DisPass-$(VERSION).tar.gz
	gzip -c dispass.1 > dispass.1.gz
	mv dispass.1.gz $(MAN_PATH)
	cp zsh/_dispass $(ZSH_SITE_FUNCS_PATH)
	make clean

uninstall: clean
	$(PIP_EXEC) uninstall dispass

clean:
	rm -f MANIFEST dispass.1.gz
	rm -rf dist

# vim: set noet ts=8 sw=8 sts=8:
