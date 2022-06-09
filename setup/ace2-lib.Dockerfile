# extend image base
ARG name
FROM ace2-lib-$name-base

# install source
ARG name
COPY lib/$name/src ${ACE2}/lib/$name

# install config if one exists
ARG env
COPY lib/$name/config-$env.ym[l] ${ACE2}/lib/$name/config.yml

# test
COPY lib/$name/tests lib/$name/tests
RUN pytest -vv lib/$name && rm -rf lib
