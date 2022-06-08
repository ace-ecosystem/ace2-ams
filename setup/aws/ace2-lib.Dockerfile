ARG lib
FROM ace2-base

# install deps
COPY $lib/setup.sh setup.sh
RUN bash setup.sh && rm setup.sh

# install ace2 lib
COPY --from=ace2-lib-ace2 / /

# test
COPY $lib lib
RUN pytest -vv lib && rm -rf lib

# install source
COPY $lib/src /opt/ace2/$lib
