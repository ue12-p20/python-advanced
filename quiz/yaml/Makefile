%.yamlb: stem=$(subst .yamlb,,$@)
%.yamlb: %.yaml
	openssl base64 -in $(stem).yaml -out $@ 

%.yamloop: stem=$(subst .yamloop,,$@)
%.yamloop: %.yamlb
	openssl base64 -d -in $(stem).yamlb -out $@ 



ALL=$(shell git ls-files *.yamlb)
PLAIN=$(subst yamlb,yamloop,$(ALL))

all: $(ALL)

loop: $(PLAIN)
