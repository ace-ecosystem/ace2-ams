# set the base image in single location
ARG base=public.ecr.aws/lambda/python:3.9


# install and test ace2 core code 
FROM $base AS ace2
    # install ace2 deps
    RUN pip3 install boto3 pydantic pytest pytest-datadir pytz pyyaml

    # install ace2 source
    COPY ace2 ace2

    # run tests
    COPY conftest.py conftest.py
    RUN pytest -vv &&\
        rm -rf ace2/tests &&\
        rm -rf /tmp/pytest* &&\
        find / \( -name "*.pyc" -or -name ".pytest_cache" -or -name "__pycache__" \) -exec rm -rf {} +


# install service dependencies
FROM $base AS base
    DEPENDENCIES


# build service image
FROM $base AS service
    # copy everything from ace2 stage
    COPY --from=ace2 / /

    # copy everything from base stage
    COPY --from=base / /

    # install source
    ARG name
    CMD [ "services.$name.service.run" ]
    COPY services/$name services/$name

    # run tests
    # remove test files and dependencies
    RUN pytest -vv &&\
        rm -rf conftest.py &&\
        rm -rf services/$name/tests &&\
        rm -rf /tmp/pytest* &&\
        find / \( -name "*.pyc" -or -name ".pytest_cache" -or -name "__pycache__" \) -exec rm -rf {} + &&\
        pip3 uninstall -y pytest-datadir pytest


# squash layers into final image
FROM $base AS final
    COPY --from=service / /
