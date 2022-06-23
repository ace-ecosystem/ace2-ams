# set the base image in single location
ARG base=public.ecr.aws/lambda/python:3.9


# install and test ace2 core code 
FROM $base AS ace2
    # install ace2 deps
    RUN pip3 install boto3 pydantic pytest pytest-datadir pyyaml

    # install ace2 source
    COPY ace2 ace2

    # pretty much everything will need the database service
    COPY services/database/service.py ace2/services/database.py

    # run tests
    # remove test files
    RUN mv ace2/tests tests &&\
        pytest -vv &&\
        rm -rf tests/ace2 &&\
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
    COPY services/$name ./

    # rename desired settings file
    # remove unused settings files
    # run tests
    # remove test files and dependencies
    ARG settings
    RUN mv $settings settings.yml || true &&\
        rm settings-*.yml || true &&\
        pytest -vv &&\
        rm -rf tests &&\
        rm -rf /tmp/pytest* &&\
        find / \( -name "*.pyc" -or -name ".pytest_cache" -or -name "__pycache__" \) -exec rm -rf {} + &&\
        pip3 uninstall -y pytest-datadir pytest


# squash layers into final image
FROM $base AS final
    COPY --from=service / /
    CMD [ "service.run" ]
