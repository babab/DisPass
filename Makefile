# Copyright (c) 2012-2016  Tom Willemse <tom@ryuslash.org>
# Copyright (c) 2011-2018  Benjamin Althues <benjamin@babab.nl>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

.PHONY: make show-all version rm_pyc doc_clean doc coverage test dist \
	install install-pip  install-src install-metafiles \
	uninstall-metafiles uninstall clean py-info

DESTDIR			= /
DESKTOP_PATH		= $(DESTDIR)/usr/share/applications
ICON_PATH		= $(DESTDIR)/usr/share/icons/hicolor
ZSH_SITE_FUNCS_PATH	= $(DESTDIR)/usr/share/zsh/site-functions
PYTHON_EXEC		= python
PIP_EXEC		= $(PYTHON_EXEC) -m pip

VERSION_CURRENT		= 0.4.0.dev0
VERSION_PREVIOUS	= 0.3.0

# Deprecated, only used to remove previous installations
MAN_PATH		= $(DESTDIR)/usr/share/man/man1
INFO_PATH		= $(DESTDIR)/usr/share/info

# Include any local configuration overrides
sinclude config.mk

_files_to_bump = setup.py dispass/dispass.py docs/en/{index,installing}.rst

make:
	@echo 'make install'
	@echo 'make uninstall'
	@echo '  Install python package, scripts and metafiles'
	@echo '  (install wheel pkg with pip and run install-metafiles)'
	@echo
	@echo 'make install-metafiles'
	@echo 'make uninstall-metafiles'
	@echo '  Install or remove Zsh completion, opendesktop spec and logos '
	@echo '  (does not install or remove python package and scripts)'
	@echo
	@echo 'make show-all'
	@echo '  Show development/packaging targets'

show-all: make
	@echo
	@echo
	@echo 'TARGETS FOR DISTRIBUTION PACKAGE(R)S'
	@echo 'make install-src    install via setup.py install --root=$$DESTDIR'
	@echo
	@echo 'Note: make install-src does not install requirements.txt and '
	@echo '      is aimed for usage in creating distribution packages'
	@echo
	@echo "DEVELOPMENT TARGETS"
	@echo "make version   Update version strings"
	@echo "make py-info   Print version and path of Python the Makefile uses"
	@echo "make test      Run unittests, check-manifest and flake8"
	@echo "make doc       Build html documentation with Sphinx"
	@echo "make dist      Build python source archive file"
	@echo "make clean     Clean program build files"
	@echo "make coverage  Run coverage with nosetests (experimental)"

version:
	sed -i 's/$(VERSION_PREVIOUS)/$(VERSION_CURRENT)/' $(_files_to_bump)
	@echo
	@echo DONE. Do not forget to update ChangeLog.rst. To view changes, run:
	@echo
	@echo '  git diff $(_files_to_bump)'

rm_pyc:
	find . -name "*.pyc" | xargs /bin/rm -f

doc_clean: rm_pyc
	cd docs/en/; make clean

doc: doc_clean
	cd docs/en/; make html
	rm -rf doc/html/$(VERSION_CURRENT)
	mkdir -p doc/html/$(VERSION_CURRENT)
	mv docs/en/_build/html doc/html/$(VERSION_CURRENT)/en
	make doc_clean
	cd doc/html/$(VERSION_CURRENT)/en; $(PYTHON_EXEC) -m http.server --bind 127.0.0.1

coverage:
	coverage erase
	coverage run .virtualenv/bin/pytest -v
	coverage report
	coverage html

test:
	pytest -v
	@echo 'DONE... All tests have passed'
	@echo
	check-manifest --ignore 'docs*'
	@echo 'DONE... Everything seems to be in the MANIFEST file'
	@echo
	flake8 dispass tests
	@echo 'DONE... All code is PEP-8 compliant'

dist: check-if-root py-info rm_pyc
	$(PIP_EXEC) install -r requirements.txt
	$(PYTHON_EXEC) setup.py sdist bdist_wheel

install: dist install-metafiles
	$(PIP_EXEC) install --upgrade dist/DisPass-$(VERSION_CURRENT)-py2.py3-none-any.whl
	make clean

install-src: py-info install-metafiles
	$(PYTHON_EXEC) setup.py install --root='$(DESTDIR)'
	make clean

install-metafiles:
	install -Dm644 zsh/_dispass $(ZSH_SITE_FUNCS_PATH)/_dispass
	install -Dm644 etc/dispass.desktop $(DESKTOP_PATH)/dispass.desktop
	for size in 24 32 64 128 256 512; do \
		install -Dm644 "logo/logo$${size}.png" \
		"$(ICON_PATH)/$${size}x$${size}/apps/dispass.png"; \
	done

uninstall-metafiles:
	rm -f $(ZSH_SITE_FUNCS_PATH)/_dispass
	rm -f $(DESKTOP_PATH)/dispass.desktop
	for size in 24 32 64 128 256 512; do \
		rm -f "$(ICON_PATH)/$${size}x$${size}/apps/dispass.png"; \
	done
	# Remove manpage and info document if installed in a previous version
	rm -f $(MAN_PATH)/dispass.1.gz
	rm -f $(INFO_PATH)/dispass.info.gz

uninstall: py-info clean uninstall-metafiles
	$(PIP_EXEC) uninstall dispass

clean:
	rm -f MANIFEST dispass.1.gz dispass.info.gz
	rm -rf build dist DisPass.egg-info

py-info:
	@echo Python environment information
	$(PYTHON_EXEC) -V
	$(PYTHON_EXEC) -c "import sys; print(sys.executable)"

check-if-root:
	# make 'dist' or 'install' should not be run as root
	test $$(whoami) != root || false

# vim: set noet ts=8 sw=8 sts=8:
