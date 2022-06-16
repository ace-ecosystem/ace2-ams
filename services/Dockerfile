# extend image base
ARG name
FROM ace2-services-$name-base

# install ace2 core
COPY --from=ace2 / /

# install source
ARG name
COPY services/$name/service.py ${ACE2}/services/$name/service.py

# make service importable
RUN touch ${ACE2}/services/__init__.py && echo "from .service import *" > ${ACE2}/services/$name/__init__.py

# install settings
ARG env
COPY services/$name/settings-$env.ym[l] ${ACE2}/services/$name/settings.yml

# test
COPY services/$name/tests tests
RUN pytest -vv && rm -rf tests /tmp/pytest* && find / -type d -name ".pytest_cache" -exec rm -rf {} +

# uninstall testing tools
RUN pip3 uninstall -y pytest-datadir pytest

# set entrypoint to the module run function
RUN ln -s ${ACE2}/services/$name/service.py service.py
CMD [ "service.run" ]
