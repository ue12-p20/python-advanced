# --------
FROM nbhosting/minimal-notebook

# NOTE
# we cannot use jupyter nbextension enable/disable
# because we provide our own nbconfig/notebook.json
# and that is where is stored the enabled/disabled extensions
RUN true \
 && pip install -U nb-courselevels \
 && jupyter nbextension enable hide_input/main \
 && pip install rise --pre \
 && pip install numpy pandas pandas \
 && apt-get install -y graphviz && pip install graphviz \
 && true
