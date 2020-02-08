CWD    = $(CURDIR)
MODULE = $(notdir $(CWD))

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

PIP = $(CWD)/bin/pip3
PY  = $(CWD)/bin/python3

.PHONY: all
all: $(PY) ./$(MODULE).py $(MODULE).ini
	$^

$(PIP) $(PY):
	python3 -m venv .
	$(CWD)/bin/pip3 install -U pip
	$(CWD)/bin/pip3 install -U ply

.PHONY: merge release zip

MERGE  = Makefile README.md .gitignore $(MODULE).*

merge:
	git checkout master
	git checkout shadow -- $(MERGE)

release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	git checkout shadow

zip:
	git archive --format zip --output $(MODULE)_src_$(NOW)_$(REL).zip HEAD
