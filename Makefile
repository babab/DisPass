DESTDIR			= /
DESKTOP_PATH		= $(DESTDIR)/usr/share/applications
ICON_PATH		= $(DESTDIR)/usr/share/icons/hicolor
MAN_PATH		= $(DESTDIR)/usr/share/man/man1
INFO_PATH		= $(DESTDIR)/usr/share/info
ZSH_SITE_FUNCS_PATH	= $(DESTDIR)/usr/share/zsh/site-functions
PYTHON_EXEC		= python2
PIP_EXEC		= pip2

sinclude config.mk

.PHONY: make rm_pyc doc_clean doc man dist install install-pip install-src install-metafiles uninstall clean

VERSION		= 0.3.0

make:
	@echo 'Installation targets'
	@echo 'make install        alias for install-pip'
	@echo 'make install-pip    install wdocker wheel pkg with pip (default)'
	@echo 'make install-src    install via setup.py install --root=$$DESTDIR'
	@echo
	@echo 'Note: make install-src does not install requirements.txt and '
	@echo '      is aimed for usage in creating distribution packages'
	@echo
	@echo "Development targets"
	@echo "make doc       Build html documentation with Sphinx"
	@echo "make man       Build manpage and info documentation with Sphinx"
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
	cd docs/en/; make info
	mv docs/en/_build/texinfo/DisPass.info ./dispass.info
	make doc_clean

dist: rm_pyc
	$(PIP_EXEC) install -r requirements.txt
	$(PYTHON_EXEC) setup.py sdist bdist_wheel

install: install-pip

install-pip: dist install-metafiles
	$(PIP_EXEC) install --upgrade dist/DisPass-$(VERSION)-py2.py3-none-any.whl
	install-info dispass.info $(INFO_PATH)/dir
	make clean

install-src: install-metafiles
	$(PYTHON_EXEC) setup.py install --root='$(DESTDIR)'
	make clean

install-metafiles:
	gzip -c dispass.1 > dispass.1.gz
	gzip -c dispass.info > dispass.info.gz
	install -Dm644 dispass.1.gz $(MAN_PATH)/dispass.1.gz
	install -Dm644 dispass.info.gz $(INFO_PATH)/dispass.info.gz
	install -Dm644 zsh/_dispass $(ZSH_SITE_FUNCS_PATH)/_dispass
	install -Dm644 etc/dispass.desktop $(DESKTOP_PATH)/dispass.desktop
	for size in 24 32 64 128 256 512; do \
		install -Dm644 "logo/logo$${size}.png" \
		"$(ICON_PATH)/$${size}x$${size}/apps/dispass.png"; \
	done

uninstall: clean
	$(PIP_EXEC) uninstall dispass

clean:
	rm -f MANIFEST dispass.1.gz dispass.info.gz
	rm -rf build dist DisPass.egg-info

# vim: set noet ts=8 sw=8 sts=8:
