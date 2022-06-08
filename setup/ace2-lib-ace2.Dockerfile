FROM ace2-base AS ace2-lib-ace2

# install deps
COPY lib/ace2/setup.sh setup.sh
RUN bash setup.sh && rm setup.sh

# install source
COPY lib/ace2/src /opt/ace2/lib/ace2

# test
COPY lib/ace2/tests lib/ace2/tests
RUN pytest -vv lib/ace2 && rm -rf lib
