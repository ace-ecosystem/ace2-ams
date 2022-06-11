# extend image base
ARG name
FROM ace2-modules-$name-base

# install ace2 core
COPY --from=ace2 / /

# install source
ARG name
COPY modules/$name/condition ${ACE2}/modules/$name/condition
COPY modules/$name/module.py ${ACE2}/modules/$name/module.py

# make module importable
RUN touch ${ACE2}/modules/$name/__init__.py

# install config if one exists
ARG env
COPY modules/$name/config-$env.ym[l] ${ACE2}/modules/$name/config.yml

# test
COPY modules/$name/tests tests
RUN pytest -vv && rm -rf tests

# uninstall testing tools
RUN pip3 uninstall -y pytest-datadir pytest

# set entrypoint to the module run function
RUN ln -s ${ACE2}/modules/$name/module.py module.py
CMD [ "module.run" ]
