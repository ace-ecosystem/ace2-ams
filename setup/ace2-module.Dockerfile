# entend module base of the same name
ARG name
FROM ace2-module-$name-base

# install ace2 lib
COPY --from=ace2-lib-ace2 / /

# get module path
ARG module

# add module source
COPY $module/module.py /opt/ace2/$module/module.py
COPY $module/condition /opt/ace2/$module/condition

# add optional config file
COPY $module/config.p[y] /opt/ace2/$module/

# make module importable
RUN touch /opt/ace2/$module/__init__.py
ENV PYTHONPATH "${PYTHONPATH}:/opt/ace2/modules"

# test
COPY $module/tests $module/tests
RUN pytest -vv $module && rm -rf modules

# uninstall testing tools
RUN pip3 uninstall -y pytest-datadir pytest

# set entrypoint to the module run function
CMD [ "module.run" ]
