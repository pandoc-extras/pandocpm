SHELL := /usr/bin/env bash

# configure engine
## LaTeX engine
### LaTeX workflow: pdf; xelatex; lualatex
latexmkEngine := pdf
### pandoc workflow: pdflatex; xelatex; lualatex
pandocEngine := pdflatex
## HTML
HTMLVersion := html5
## ePub
# ePubVersion := epub

# filter := 

CSSURL:=https://ickc.github.io/markdown-latex-css

# command line arguments
pandocArgCommon := -f markdown+autolink_bare_uris-fancy_lists --toc --normalize -S -V linkcolorblue -V citecolor=blue -V urlcolor=blue -V toccolor=blue --latex-engine=$(pandocEngine) -M date="`date "+%B %e, %Y"`"
# Workbooks
## MD
pandocArgMD := -f markdown+abbreviations+autolink_bare_uris+markdown_attribute+mmd_header_identifiers+mmd_link_attributes+mmd_title_block+tex_math_double_backslash-latex_macros-auto_identifiers -t markdown+raw_tex-native_spans-simple_tables-multiline_tables-grid_tables-latex_macros --normalize -s --wrap=none --column=999 --atx-headers --reference-location=block --file-scope
## TeX/PDF
### LaTeX workflow
latexmkArg := -$(latexmkEngine)
pandocArgFragment := $(pandocArgCommon) # --filter=$(filter)
### pandoc workflow
pandocArgStandalone := $(pandocArgFragment) --toc-depth=1 -s -N
## HTML/ePub
pandocArgHTML := $(pandocArgFragment) -t $(HTMLVersion) --toc-depth=2 -s -N -c $(CSSURL)/css/common.css -c $(CSSURL)/fonts/fonts.css
pandocArgePub := $(pandocArgHTML) -t $(ePubVersion) --epub-chapter-level=2
# GitHub README
pandocArgReadmeGitHub := $(pandocArgFragment) --toc-depth=2 -s -t markdown_github --reference-location=block
pandocArgReadmePypi := $(pandocArgFragment) -s -t rst --reference-location=block -f markdown+autolink_bare_uris-fancy_lists-implicit_header_references

# test := $(wildcard tests/*.md)
# testNative := $(patsubst %.md,%.native,$(test))
# testPdf := $(patsubst %.md,%.pdf,$(test))
# testAll := $(testNative) $(testPdf)

docs := $(wildcard docs/*.md)
# docsHtml := $(patsubst %.md,%.html,$(docs))
docsPdf := $(patsubst %.md,%.pdf,$(docs))
docsAll := $(docsPdf) docs/index.html README.md README.rst README.html # $(docsHtml)

# Main Targets ########################################################################################################################################################################################

# all: $(testAll) $(docsAll)
docs: $(docsAll)
readme: docs
test: pytest pep8 pylint
	coverage html

clean:
	rm -f .coverage README.html # $(testAll)
	rm -rf htmlcov pandocpm.egg-info build dist
	find . -type f -name "*.py[co]" -delete -or -type d -name "__pycache__" -delete
Clean:
	rm -f .coverage README.html $(docsAll) # $(testAll)
	rm -rf htmlcov pandocpm.egg-info build dist
	find . -type f -name "*.py[co]" -delete -or -type d -name "__pycache__" -delete

# Making dependancies #################################################################################################################################################################################

# %.native: %.md # $(filter)
# 	pandoc -t native -o $@ $< # -F $(filter)
%.pdf: %.md # $(filter)
	pandoc $(pandocArgStandalone) -o $@ $<
%.html: %.md # $(filter)
	pandoc $(pandocArgHTML) $< -o $@

# readme
## index.html
docs/index.html: docs/badges.markdown docs/README.md
	pandoc $(pandocArgHTML) $^ -o $@
## GitHub README
README.md: docs/badges.markdown docs/README.md
	printf "%s\n\n" "<!--This README is auto-generated from \`docs/README.md\`. Do not edit this file directly.-->" > $@
	pandoc $(pandocArgReadmeGitHub) $^ >> $@
## PyPI README
README.rst: docs/badges.markdown docs/README.md
	printf "%s\n\n" ".. This README is auto-generated from \`docs/README.md\`. Do not edit this file directly." > $@
	pandoc $(pandocArgReadmePypi) $^ >> $@
README.html: README.rst
	rst2html.py $< > $@

# maintenance #########################################################################################################################################################################################

# Deploy to PyPI
## by Travis, properly git tagged
pypi:
	git tag -a v$$(python setup.py --version) -m 'Deploy to PyPI' && git push origin v$$(python setup.py --version)
## Manually
pypiManual:
	python setup.py register -r pypitest && python setup.py sdist upload -r pypitest && python setup.py register -r pypi && python setup.py sdist upload -r pypi

# init:
# 	pip install -r requirements.txt
# 	pip install -r tests/requirements.txt

pytest: # $(testNative)
	python3 -m pytest -vv --cov=pandocpm tests
pytestLite:
	python3 -m pytest -vv --cov=pandocpm tests

# check python styles
pep8:
	pep8 . --ignore=E402,E501,E731
pep8Strict:
	pep8 .
pyflakes:
	pyflakes .
flake8:
	flake8 .
pylint:
	pylint pandocpm/__main__.py

# cleanup python
autopep8:
	autopep8 . --recursive --in-place --pep8-passes 2000 --verbose
autopep8Aggressive:
	autopep8 . --recursive --in-place --pep8-passes 2000 --verbose --aggressive --aggressive
