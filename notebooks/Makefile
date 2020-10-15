# dependencies
# (*) for the sphinx engine (readthedocs)
#     pip install ipypublish[sphinx]
# (*) fore cleaning things up (only locally for profs)
#     pip install nbstripout

NOTEBOOKS := $(shell git ls-files *.md)

all: sphinx
clean: sphinx-clean

#########################################################################
# publication
# 
# execution is done as part of sphinx-build
# there is only the need to mention the notebooks
# in index.rst
# 

#### sphinx

_build/html/index.html: index.rst conf.py $(NOTEBOOKS) 
	sphinx-build -b html . _build/html

sphinx: _build/html/index.html

sphinx-view:
	open _build/html/index.html

sphinx-clean:
	rm -rf _build

.PHONY: sphinx sphinx-view sphinx-clean
