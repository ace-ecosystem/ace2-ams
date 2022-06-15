# extend image base
ARG name
FROM ace2-services-$name-base

# install ace2 core
COPY --from=ace2 / /

# install source
ARG name
COPY services/$name/conditio[n] ${ACE2}/services/$name/condition
COPY services/$name/model.p[y] ${ACE2}/services/$name/model.py
COPY services/$name/service.py ${ACE2}/services/$name/service.py

# make service importable
RUN touch ${ACE2}/services/$name/__init__.py

# install config if one exists
ARG env
COPY services/$name/config-$env.ym[l] ${ACE2}/services/$name/config.yml

# test
COPY services/$name/tests tests
RUN pytest -vv && rm -rf tests

# uninstall testing tools
RUN pip3 uninstall -y pytest-datadir pytest

# set entrypoint to the module run function
RUN ln -s ${ACE2}/services/$name/service.py service.py
CMD [ "service.run" ]
