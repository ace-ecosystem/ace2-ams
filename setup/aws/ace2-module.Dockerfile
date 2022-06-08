ARG name
FROM ace2-module-$name-base

# install ace2 lib
COPY --from=ace2-lib-ace2 / /

ARG module

# add module condition
COPY $module/condition /opt/ace2/$module/condition

# add module config
COPY $module/config.py /opt/ace2/etc/$module/config.py

# add module script
COPY $module/module.py /opt/ace2/$module/module.py

# test
COPY $module/tests $module/tests
RUN ln -s /opt/ace2/$module/module.py $module/tests/module.py && pytest -vv $module && rm -rf module

# uninstall testing tools
RUN pip3 uninstall -y pytest-datadir pytest

# set entrypoint to the module run function
CMD [ "module.run" ]
