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
