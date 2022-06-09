# extend lib base of the same name
ARG name
FROM ace2-lib-$name-base

# get lib name
ARG lib

# install source
COPY $lib/src ${ACE2}/$lib

# install config if one exists
COPY $lib/config.ym[l] ${ACE2}/$lib/

# test
COPY $lib/tests $lib/tests
RUN pytest -vv $lib && rm -rf lib
