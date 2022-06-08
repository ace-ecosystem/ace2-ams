# extend lib base of the same name
ARG name
FROM ace2-lib-$name-base

# get lib name
ARG lib

# install config
COPY $lib/config.yml /opt/ace2/etc/$lib/config.yml

# install source
COPY $lib/src /opt/ace2/$lib

# test
COPY $lib/tests $lib/tests
RUN pytest -vv $lib && rm -rf lib
